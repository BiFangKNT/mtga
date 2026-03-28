# Trae 进程级代理模式设计方案

定版日期：2026-03-28

## 1. 目标

为 MTGA 增加一套新的代理模式，使“只有由 MTGA 启动的 Trae 进程走代理”，并保留当前旧模式以兼容现有用户。

设计目标：

- 仅影响 Trae，不修改系统 `hosts`
- 不占用本地 `443`
- 与现有配置组、鉴权、模型映射、请求改写逻辑兼容
- 与旧模式共存，可由设置项切换

## 2. 定版决策

新模式固定采用以下方案：

```text
mitmdump + MTGA addon + Trae launcher(--proxy-server)
```

具体含义：

1. MTGA 启动 `mitmdump`
2. MTGA 为 `mitmdump` 加载自定义 addon
3. MTGA 以新进程方式启动 Trae，并附带：

```text
--proxy-server=http://127.0.0.1:<port>
```

4. Trae 的 HTTP/HTTPS/WebSocket 请求经由 `mitmdump`
5. addon 在代理层接管 MTGA 现有的请求改写、鉴权、模型映射和上游转发逻辑

本方案是当前唯一推荐方案。其他路线不纳入本文设计范围。

## 3. 范围与非目标

### 3.1 支持范围

- Windows 优先
- 仅支持“由 MTGA 新启动的 Trae”走代理
- 新旧两种代理模式共存
- 新模式下一键启动跳过 `hosts`
- 新模式停止时不执行 `hosts` 删除

### 3.2 非目标

- 不支持给已运行的 Trae 补启动参数
- 不支持任意第三方进程接管
- 不引入驱动层方案
- 不将 `mitmproxy local capture` 作为首版能力

## 4. 总体架构

### 4.1 模式划分

- 旧模式：`hosts + 本地 443 + 证书 + 反代`
- 新模式：`mitmdump + addon + Trae launcher`

### 4.2 新模式组件

#### 设置层

- 在 [SettingsPanel.vue](/C:/github/mtga/app/components/panels/SettingsPanel.vue) 增加代理模式开关
- 新增 Trae 可执行文件路径配置

#### 前端状态层

- 在 [useMtgaStore.ts](/C:/github/mtga/app/composables/useMtgaStore.ts) 的 `runtimeOptions` 中新增：
  - `proxyMode`
  - `traeExecutablePath`

#### 后端编排层

- 扩展 [proxy.py](/C:/github/mtga/python-src/mtga_app/commands/proxy.py) 的启动 payload
- `proxy_start_all` 按模式分支
- `proxy_stop` 按模式分支
- 退出清理按模式分支

#### 代理进程层

- 新增 `mitmdump` 进程管理模块
- 负责启动、停止、日志转发、异常退出检测

#### Addon 适配层

- 新增 MTGA 专用 mitmproxy addon
- 在 addon 中接入：
  - 下游鉴权
  - 映射模型名
  - 请求体转换
  - 上游 provider 路由
  - 响应归一化

#### Trae 启动器层

- 新增 Trae 子进程启动模块
- 启动参数中附带 `--proxy-server`
- 记录启动命令、PID、退出状态

## 5. 新模式启动流程

### 5.1 一键启动

新模式下，“一键启动全部服务”流程固定为：

1. 校验全局配置
2. 校验当前配置组
3. 启动 `mitmdump`
4. 启动 Trae，并附带 `--proxy-server`
5. 输出启动完成日志

与旧模式的差异：

- 不执行证书生成/安装之外的 `hosts` 修改
- 不依赖本地 `443`
- 不调用现有 `modify_hosts_file_result()` 流程

### 5.2 单独启动代理

新模式下“启动代理服务器”按钮的语义调整为：

- 启动 `mitmdump`
- 不启动 Trae

是否允许“仅代理进程启动、不拉起 Trae”，保留为可选行为；首版可先与“一键启动”区别对待。

## 6. 新模式停止流程

新模式下停止流程固定为：

1. 停止 Trae 子进程或解除其托管状态
2. 停止 `mitmdump`
3. 清理状态与 PID 记录
4. 输出日志

明确不做：

- 不删除 `hosts`
- 不回滚旧模式下的 `hosts` 条目

因此，后端需要把当前 [proxy.py](/C:/github/mtga/python-src/mtga_app/commands/proxy.py) 中与 `modify_hosts_file_result(action="remove")` 绑定的 stop/shutdown 逻辑改成按模式分支。

## 7. 配置设计

首版建议新增以下配置字段：

```yaml
proxy_mode: legacy_hosts | trae_process_proxy
trae_executable_path: "C:\\Path\\To\\Trae.exe"
```

说明：

- `proxy_mode`
  - `legacy_hosts`：旧模式
  - `trae_process_proxy`：新模式
- `trae_executable_path`
  - 仅新模式使用
  - 首版要求用户显式配置

运行时 payload 也同步增加：

```json
{
  "proxy_mode": "trae_process_proxy",
  "trae_executable_path": "C:\\Path\\To\\Trae.exe"
}
```

## 8. Addon 设计职责

MTGA addon 只负责代理逻辑，不负责 UI 或进程管理。

职责边界：

- 读取 MTGA 当前配置组
- 校验下游请求头
- 将 Trae 请求改写为上游 provider 所需格式
- 调用上游 API
- 将返回结果归一化为 MTGA 对外约定格式
- 输出结构化日志

不负责：

- 发现或启动 Trae
- 管理前端状态
- 修改 `hosts`

## 9. 证书策略

新模式不再依赖“伪造 `api.openai.com` 服务端证书 + 本地 443”这条链路。

但如果需要拦截 HTTPS 明文内容，仍需要 MITM 证书信任。

首版策略建议：

1. 优先使用 mitmproxy 自带 CA 体系
2. MTGA 只负责：
   - 检查证书是否存在
   - 提示用户安装或信任证书
   - 输出诊断日志

不建议首版就强行把 MTGA 现有 CA 体系与 mitmproxy 内部 CA 做深度合并。

## 10. 模块拆分建议

建议新增以下 Python 模块：

```text
python-src/modules/proxy_modes/
  trae_process_proxy_manager.py
  mitmproxy_process.py
  trae_launcher.py
  mtga_mitm_addon.py
```

建议职责：

- `trae_process_proxy_manager.py`
  - 新模式总编排
- `mitmproxy_process.py`
  - `mitmdump` 生命周期管理
- `trae_launcher.py`
  - Trae 启动与状态跟踪
- `mtga_mitm_addon.py`
  - 代理请求/响应改写逻辑

## 11. 分阶段实施

### 阶段 1：模式骨架

- 设置页增加模式开关
- 新增配置字段
- `proxy_start_all` / `proxy_stop` / shutdown 支持按模式分支
- 新模式先只做到“跳过 hosts”

交付结果：

- 新旧模式控制面跑通

### 阶段 2：Trae 启动器

- 启动 Trae 并附带 `--proxy-server`
- 记录 PID 和退出状态
- 完成基础日志

交付结果：

- 能确认 Trae 是否接受该启动参数

### 阶段 3：mitmdump + addon

- 启动 `mitmdump`
- 加载 MTGA addon
- 接通现有请求改写与上游转发能力

交付结果：

- 新模式完整链路可用

### 阶段 4：收敛与验证

- 完善 stop/restart/crash cleanup
- 完善错误提示
- 完善日志可观测性

交付结果：

- 首版可交付

## 12. 验收标准

### 功能验收

- 旧模式行为不变
- 新模式下一键启动跳过 `hosts`
- 新模式停止时不删除 `hosts`
- MTGA 能启动 Trae，并附带 `--proxy-server`
- Trae 请求可进入 `mitmdump`
- addon 能完成请求改写与上游转发
- 其他未走该显式代理的软件不受影响

### 稳定性验收

- Trae 首次启动成功
- Trae 重启成功
- `mitmdump` 异常退出可感知
- MTGA 退出后状态可清理
- 重复启动/停止不会遗留脏状态

### 诊断验收

- 有 Trae 启动日志
- 有代理启动日志
- 有 addon 请求日志
- 有异常退出日志

## 13. 当前执行优先级

当前建议立即推进的工作只有三项：

1. 模式开关与配置字段落地
2. 新模式下的一键启动/停止分支改造
3. Trae launcher 与 `mitmdump` 进程骨架

Addon 细节实现放在上述骨架稳定后推进。
