# Update Recovery

Use this when Trae updates, the native route starts failing after a previously working build, or the rewriter reports missing/changed breakpoint locations.

## First checks

1. Confirm no stale Trae process is running before starting native route. The route is designed to launch a clean Trae instance.
2. Confirm the loopback still answers on `127.0.0.1:18083`.
3. Confirm the rewriter module imports:
   `uv run python -m modules.trae_patch.trae_native_sse_open_url_rewriter --help`
4. Confirm Trae still loads `resources/app/modules/ai-agent/ai_agent.dll`.

## Re-locate URL-copy point

Known byte pattern:

```text
48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00
```

Expected rewriter constants:

- `URL_COPY_PATTERN`: the bytes above.
- `URL_COPY_CALL_OFFSET`: `0x0F`.
- Default old URL: `https://api.openai.com/v1/chat/completions`.
- Default new URL: `http://127.0.0.1:18083/v1/chat/completions`.

Run the byte-pattern helper from `python-src`:

```powershell
uv run python scripts/trae_patch/trae_native_byte_pattern.py --pattern "48 8b 52 08 4d 8b 46 10 48 8d 8d 20 01 00 00" --json
```

Interpretation:

- Exactly one match is the normal case.
- Zero matches means Trae changed the compiled code around URL copy; inspect nearby URL/string references in `ai_agent.dll`.
- Multiple matches means the rewriter needs a more specific anchor or an additional validation check before patching.

## Reproduce without the full app

Use the maintenance session if the main UI path is too heavy:

```powershell
uv run python scripts/trae_patch/trae_native_custom_model_session.py --duration-seconds 300
```

Use CDP to send a chat message after Trae is ready:

```powershell
uv run python scripts/trae_patch/trae_cdp_send_chat.py --message "你是谁？"
```

Prefer CDP for repeated repros; it avoids manual UI timing differences.

## What to patch

- If only the RVA/call point drifted, update the constants in `python-src/modules/trae_patch/trae_native_sse_open_url_rewriter.py`.
- If process/module discovery broke, update helpers in `python-src/modules/trae_patch/trae_native_runtime_breakpoints.py`.
- If the final URL structure changed from Rust string layout, update the memory read/write helpers in `python-src/modules/trae_patch/trae_native_breakpoint_probe.py`.
- If shared proxy behavior regresses, fix `ProxyApp` or `TraeNativeRouteManager` instead of adding native-only branches.

## Validation

- Run `pnpm py:check` after Python changes.
- Run the rewriter `--help` command to catch broken module imports.
- For real behavior, validate with a clean Trae process launched by MTGA native route.
- Summarize only relevant events: armed breakpoint, patch count, request URL, MTGA request receipt, upstream stream start/end, and Trae UI result.
