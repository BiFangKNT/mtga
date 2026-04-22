# Trae Native Route Scripts

这里只保留 Trae native 自定义模型路线接入主流程前跑通路径的复查工具，以及少量高价值辅助工具。

## 复查与维护

- `trae_native_custom_model_session.py`：接入主流程前最终跑通的真实上游会话脚本。
- `trae_local_model_loopback.py`：独立会话脚本复用的本地 loopback。
- `trae_native_byte_pattern.py`：验证 URL copy call 字节模式定位，便于 Trae 版本更新后复核。
- `trae_ai_agent_latest_verdict.py`：从 Trae 日志判断最近 chat 结果。

## 辅助工具

- `trae_cdp_targets.py`：枚举 Trae CDP targets，确认可附着页面。
- `trae_cdp_send_chat.py`：通过 CDP 向 Trae chat UI 发送测试消息。它只作为触发工具保留，不参与 native rewriter 主流程。

`python-src/artifacts/` 和仓库根 `artifacts/` 是临时取证输出，不需要提交，可随时删除。
