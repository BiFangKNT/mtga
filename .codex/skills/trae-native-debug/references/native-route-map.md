# Trae Native Route Map

## Runtime files

- `python-src/modules/services/trae_native_route.py`: starts/stops native route, loopback, Trae, and the native rewriter subprocess.
- `python-src/modules/trae_patch/trae_native_sse_open_url_rewriter.py`: runtime entry point that attaches to `ai_agent.dll` and rewrites the outgoing request URL.
- `python-src/modules/trae_patch/trae_native_breakpoint_probe.py`: Windows debug/breakpoint primitives reused by the rewriter.
- `python-src/modules/trae_patch/trae_native_runtime_breakpoints.py`: process/module enumeration and debug privilege helpers.
- `python-src/modules/trae_patch/trae_native_string_offsets.py`: PE/RVA and byte-pattern helpers.
- `python-src/modules/trae_patch/trae_native_hook_candidates.py`: shared `ai_agent.dll` path and candidate search helpers.
- `python-src/scripts/trae_patch/`: maintenance and repro scripts only; not runtime dependencies.

## Current working route

1. MTGA starts local loopback at `http://127.0.0.1:18083/v1/chat/completions`.
2. MTGA launches Trae with `--remote-debugging-port=9330`.
3. Rewriter waits for a Trae process with `ai_agent.dll` loaded.
4. Rewriter locates the URL-copy call using the known byte pattern.
5. When Trae's native custom-model client prepares an OpenAI-compatible request, the rewriter replaces the URL with the MTGA loopback URL.
6. Trae still owns the native parser and downstream UI state. MTGA only serves the OpenAI-compatible HTTP/SSE endpoint.

## Important chain learned from debugging

- Custom model path goes through `CustomModelProxyManager`.
- It connects to the official custom-model WebSocket tunnel, observed around `wss://...trae.ai/custom_model`.
- Tunnel delivers native SSE/open instructions.
- Native code eventually builds a `reqwest` request to the user configured `base_url`.
- The maintainable intercept point is the final URL copy/build step before `reqwest`, not the private tunnel frames.

## Prior dead ends

- Renderer JS patching of chat stream events can make data arrive but does not match Trae's real state machine and is brittle.
- Hand-building private tunnel events produced 4028/4054-style failures and requires maintaining Trae private protocol structures.
- Switching to `/v1/responses` was wrong for this route; Trae custom model calls `/v1/chat/completions`.
- Renderer global object scans for `BootConfig`, `getBootConfig`, `onDidBootConfigChanged`, and similar objects did not find a stable patchable entry.
- MNI/channel probing at the renderer boundary saw many unrelated calls but did not expose the native boot config mutation path.
- Patching official WS domain or forcing a local tunnel at the boundary still leaves private protocol maintenance.

## Log reading heuristics

- A log line showing `model_info.base_url: Some("http://127.0.0.1:18083/v1")` confirms Trae accepted the patched custom model base URL at the model-info layer, but it does not prove the final native request reached MTGA.
- A local MTGA log showing upstream stream returned does not prove Trae consumed it; compare with UI error timing.
- If Trae errors before upstream stream establishment, investigate local reachability and native tunnel/rewriter timing.
- If Trae errors after MTGA streams, inspect response shape, stream termination, and whether duplicate requests were triggered.
