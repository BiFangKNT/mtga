---
name: trae-native-debug
description: Maintain, debug, and recover MTGA's Trae native custom-model route. Use when Trae native integration fails, Trae updates shift ai_agent.dll hook offsets, errors such as 4028/4054/429 appear, native rewriter or SseOpenPayload URL rewriting needs diagnosis, or Codex needs to avoid repeating prior renderer-JS/private-protocol dead ends.
---

# Trae Native Debug

## Operating Rules

- Treat the active integration point as native Rust-side URL rewriting in `ai_agent.dll`, not renderer JS.
- Prefer the existing runtime path in `python-src/modules/trae_patch/` and service glue in `python-src/modules/services/trae_native_route.py`.
- Keep `python-src/scripts/trae_patch/` for repro, CDP triggering, and maintenance probes only. Do not move runtime-required code back into scripts.
- Do not hand-roll Trae private SSE/WebSocket events unless the user explicitly asks to compare alternatives. The current goal is to reuse Trae's native parser by rewriting the outgoing request URL before `reqwest`.
- Avoid noisy foreground probes. Capture long output to files or existing JSONL logs, summarize only the relevant events, and stop background processes when done.
- Do not stage changes unless the user explicitly asks. This project has a history of large touched sets during Trae debugging.

## Workflow

1. Classify the failure before changing code.
   - `4028`: generic Trae custom-model failure. It can mean auth, unreachable local service, wrong URL, 4xx, or malformed response.
   - `4054`: usually means Trae's native/custom-model tunnel path rejected or could not consume the stream; prior private protocol hand-roll attempts hit this.
   - `429`: usually caused by repeated live upstream probes or duplicate requests; throttle and inspect request counts before blaming auth.

2. Confirm which path is under test.
   - Native route should launch Trae with CDP, start local loopback on `127.0.0.1:18083`, and run the native rewriter.
   - Legacy reverse-hosts route is separate. Shared proxy behavior such as config hot update should flow through `ProxyApp.apply_runtime_config()`.
   - If debugging a route choice or UI config, inspect settings/state first; otherwise stay native.

3. Reproduce with the smallest useful surface.
   - For module availability: `uv run python -m modules.trae_patch.trae_native_sse_open_url_rewriter --help`
   - For byte-pattern drift: run `scripts/trae_patch/trae_native_byte_pattern.py` with the known URL-copy pattern.
   - For a real custom-model session: use `scripts/trae_patch/trae_native_custom_model_session.py`.
   - For UI-triggered repro without manual clicking: use `scripts/trae_patch/trae_cdp_send_chat.py`.

4. If Trae updated or offsets moved, read `references/update-recovery.md`.

5. If unsure why a prior approach is rejected, read `references/native-route-map.md` before creating new probes.

## Known Stable Facts

- The useful native chain is: `CustomModelProxyManager` -> official custom-model WebSocket tunnel -> SSE instruction -> `reqwest` -> user `base_url`.
- The current patch avoids Trae's private tunnel protocol by rewriting the final URL used for the outgoing OpenAI-compatible request.
- Renderer/global scans for `BootConfig`, MNI channel interception, and hand-built JS/internal events were negative or higher-maintenance routes.
- The known URL-copy byte pattern is `48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00`; the call offset used by the rewriter is `0x0F`.

## Resources

- `references/native-route-map.md`: architecture, file map, and prior dead ends.
- `references/update-recovery.md`: procedure for recovering after Trae version changes or breakpoint drift.
