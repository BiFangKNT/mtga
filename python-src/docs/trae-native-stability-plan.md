# Trae Native 路线稳定性层方案

## 目标

Trae native 自定义模型路线当前依赖 `ai_agent.dll` 中 `SseOpenPayload` URL copy 点，将原始 OpenAI Chat Completions SSE 请求改写到 MTGA loopback。稳定性层的目标不是继续扩大 hook 面，而是确保版本更新、路径变更、断点异常和运行中退出都不会静默变成 4028/4054。

必须满足：

- 不误挂：无法唯一定位 URL copy 点时直接阻断 native 路线。
- 不静默：rewriter 提前退出、未 armed、运行中异常都要有明确日志和事件文件。
- 可复查：Trae 更新后能用固定脚本判断“可用、未知但结构兼容、阻断”。
- 不回退到 JS 私有协议：CDP 只作为触发 chat 的辅助工具，不参与 native rewriter 主流程。

## 当前锚点

- 路线入口：`modules/services/trae_native_route.py`
- 平台后端入口：`modules/trae_patch/backends.py`
- Windows 运行时代码：`modules/trae_patch/windows/`
- Windows 主流程模块：`modules/trae_patch/windows/sse_open_url_rewriter.py`
- 维护脚本目录：`scripts/trae_patch/`，只用于复查、CDP 触发、一次性诊断；不得被主流程依赖。
- URL copy 字节模式：`48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00`
- call 偏移：`0x0f`
- 原 URL：`https://api.openai.com/v1/chat/completions`
- 新 URL：`http://127.0.0.1:18083/v1/chat/completions`

rewriter 只在运行时读到的 URL 等于原 URL 时改写；如果读到其他 URL，只记录 `unexpected_url`，不强行写入。

## 分层设计

### L1 静态兼容性门禁

在启动 rewriter 前生成兼容性报告：

- 读取 `ai_agent.dll` 的路径、大小、mtime、sha256。
- 搜索 URL copy 字节模式，要求命中数等于 1。
- 将 file offset 转成 RVA，要求 RVA 可解析。
- 可选：检查原 URL 字符串是否存在，作为辅助信号，不作为唯一阻断条件。

状态定义：

- `supported`：sha256 命中 manifest，且结构检查通过。
- `compatible_unknown`：sha256 未命中，但结构检查通过；默认允许启动，但日志提示 Trae 版本未知。
- `blocked`：DLL 不存在、pattern 命中数不是 1、RVA 无法解析或读文件失败。

权限不足、进程 attach 失败、Trae 未加载 `ai_agent.dll` 等运行态问题不属于 L1；这些问题在 L2 armed 阶段处理，并必须带 rewriter log tail 返回。

阻断条件必须返回 `OperationResult.failure`，不要继续拉起 rewriter。

### L2 运行前 armed 门禁

主流程已经等待 rewriter 写出 `kind=armed`。稳定性层需要把 armed 事件结构固定下来：

```json
{
  "kind": "armed",
  "pid": 1234,
  "dll_sha256": "...",
  "breakpoint_rva": "0xa67241",
  "breakpoint": "0x...",
  "old_url": "https://api.openai.com/v1/chat/completions",
  "new_url": "http://127.0.0.1:18083/v1/chat/completions"
}
```

MTGA 只有在读到 `armed` 后才显示 native 路线就绪。若 rewriter 提前退出或超时，日志必须包含 rewriter log tail。

### L3 首次请求确认

ready 只表示断点挂好，不表示 chat 已走到 URL copy 点。运行中需要继续读取 JSONL 事件：

- `patched`：成功把 Trae 请求改写到 loopback。
- `already_patched`：读到的 URL 已是新 URL，通常表示重复触发或上次状态残留。
- `unexpected_url`：读到非目标 URL，必须记录原文预览，便于判断 Trae 是否改接口。

建议在启动后设置一个轻量 watcher：

- rewriter 任务退出时，立即标记 native 路线失效并提示用户重启。
- 第一次 chat 后如果长时间没有 `patched`，不强行报错，但在日志中提示“尚未观察到 native URL rewrite 命中”。

### L4 清理与恢复

停止 native 路线时必须：

- 写 stop file，让 rewriter 自行恢复断点原字节。
- 等待 rewriter 正常退出；超时后不得尝试 terminate/kill 线程，而是保留停止状态、标记 native 路线未完全停止，并提示用户重启 MTGA/Trae。
- 关闭 loopback。
- 不主动关闭 Trae 客户端进程。

后续可补充一个停止后校验：读取 rewriter summary，确认 `status` 不是 `error`，并记录是否恢复断点、是否已 detach debug target。

### L5 版本指纹 manifest

新增 manifest 作为“已验证 Trae 版本”的白名单，但不要把未知版本全部阻断：

```json
{
  "schema_version": 1,
  "entries": [
    {
      "trae_version": "unknown",
      "ai_agent_sha256": "...",
      "ai_agent_size": 103456789,
      "url_copy_pattern": "48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00",
      "url_copy_call_offset": 15,
      "url_copy_call_rva": "0xa67241",
      "verified_at": "2026-04-21",
      "verified_by": "manual-chat-smoke"
    }
  ]
}
```

策略：

- sha 命中且结构检查通过：`supported`。
- sha 未命中但 pattern 唯一：`compatible_unknown`，允许启动并提示。
- pattern 不唯一或缺失：`blocked`。

## 落地顺序

1. 固化运行时边界：主流程只通过 `modules/trae_patch/backends.py` 选择平台后端；`scripts/trae_patch/` 只能作为维护工具，不能放运行时依赖。
2. 新增 `modules/trae_patch/windows/compatibility.py`，复用 `modules/trae_patch/windows/string_offsets.py` 输出静态兼容性报告。
3. 在 `TraeNativeRouteManager._start_rewriter_locked()` 前调用兼容性检查，阻断 `blocked`。
4. 扩展 rewriter 的 `armed` / summary JSON，写入 dll sha、pattern count、RVA、恢复状态。
5. 增加 route watcher，监控 rewriter 运行中退出和首个 `patched` 事件。
6. 加入 manifest，并在 README 中记录“Trae 更新后复核命令”。

## 验收标准

- 已验证版本：启动 native 路线后日志出现 `supported` 或 `compatible_unknown`，随后出现 `native rewriter 已就绪`。
- Trae 更新但 pattern 仍唯一：允许启动，日志明确提示未知版本。
- pattern 缺失或多命中：启动失败，错误信息包含 pattern count 和 ai_agent.dll sha。
- rewriter 提前退出：MTGA 不显示就绪，日志包含 `ThreadManager` 状态、错误摘要和 log tail。
- 运行中 rewriter 退出：MTGA 日志提示 native 路线失效。
- 停止 native 路线：loopback 停止，rewriter 退出，不关闭 Trae。

## 复查命令

以下命令都属于维护/复查脚本，不参与主流程。主流程只能使用 `modules/trae_patch/` 中的运行时代码。

在 `python-src/` 下运行：

```powershell
uv run python scripts/trae_patch/trae_native_byte_pattern.py --pattern "48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00" --json
```

真实上游会话复查：

```powershell
uv run python scripts/trae_patch/trae_native_custom_model_session.py --duration-seconds 300
```

CDP 触发 chat 仅用于辅助测试：

```powershell
uv run python scripts/trae_patch/trae_cdp_send_chat.py --message "你是谁？"
```
