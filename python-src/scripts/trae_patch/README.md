# Trae Native Route Scripts

这里只保留 Trae native 自定义模型路线接入主流程前跑通路径的复查工具，以及少量高价值辅助工具。

## 复查与维护

- `trae_native_custom_model_session.py`：接入主流程前最终跑通的真实上游会话脚本。
- `trae_macos_offline_patch_session.py`：macOS 离线 patch/clone/codesign/launch/CDP smoke 研究脚本。
  - 建议为 `--clone-app` 指定固定副本路径，并在后续复测时配合 `--reuse-clone` 复用同一份副本，避免反复复制/重建临时 app 身份。
- `trae_macos_native_symbol_report.py`：导出 macOS `libai_agent.dylib` 的关键 native 符号、反汇编、结构体偏移假设、候选 patch 点、`__TEXT,__text` 可用空洞，以及第一版离线 patch 推荐策略，供 recipe 设计使用。
- `trae_macos_url_patch_recipe.py`：基于 `trae_macos_native_symbol_report.py` 的推荐 primary site/cave，生成可直接供 `trae_macos_offline_patch_session.py` 消费的离线 patch recipe。
  - 若模块侧 `modules/trae_patch/macos/url_patch_manifest.json` 命中当前 `libai_agent.dylib` 的 sha256，优先直接复用已验证过的 site/cave，不再重新跑 symbol report 推导。
  - 当前默认 primary site 为 `default_handler_final_request_url_load @ 0x1204b3c`，它位于 `DefaultSseProxyHandler -> reqwest::Client::request` 之前，直接改写 `x3/x4` URL 对。
  - `http_request_url_to_builder @ 0x5dbd48` 仍保留为 NetBridge adapter 路径的辅助位点，但不再视为覆盖全部 custom-model 上游请求的唯一入口。
- `trae_local_model_loopback.py`：独立会话脚本复用的本地 loopback。
- `trae_native_byte_pattern.py`：验证 URL copy call 字节模式定位，便于 Trae 版本更新后复核。
- `trae_ai_agent_latest_verdict.py`：从 Trae 日志判断最近 chat 结果。

## 辅助工具

- `trae_cdp_targets.py`：枚举 Trae CDP targets，确认可附着页面。
- `trae_cdp_send_chat.py`：通过 CDP 向 Trae chat UI 发送测试消息。它只作为触发工具保留，不参与 native rewriter 主流程。
- `trae_cdp_dom_probe.py`：导出当前 workbench 的可见按钮、textbox 和 `icube/chat/agent/panel` 相关 DOM，便于校准 CDP selector。

`python-src/artifacts/` 和仓库根 `artifacts/` 是临时取证输出，不需要提交，可随时删除。
