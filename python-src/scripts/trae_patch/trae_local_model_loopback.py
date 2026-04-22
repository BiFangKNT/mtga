from __future__ import annotations

import argparse
import json
import signal
import sys
from typing import Any

from werkzeug.serving import ThreadedWSGIServer, WSGIRequestHandler

from modules.proxy.proxy_app import ProxyApp
from modules.runtime.resource_manager import ResourceManager
from modules.services.config_service import ConfigStore
from modules.services.proxy_orchestration import build_proxy_config, ensure_global_config_ready

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 18083


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="启动 Trae custom model 本地 loopback，复用现有 MTGA 代理逻辑"
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="监听地址，默认 127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="监听端口，默认 18083")
    parser.add_argument(
        "--current-config-index",
        type=int,
        help="可选：覆盖当前配置组索引；默认读取用户配置中的 current_config_index",
    )
    parser.add_argument("--debug-mode", action="store_true", help="开启详细日志")
    parser.add_argument(
        "--disable-ssl-strict-mode",
        action="store_true",
        help="关闭上游 SSL 严格校验",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 启动摘要")
    return parser


def _log(message: str) -> None:
    print(message, flush=True)


def _load_runtime_config(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    resource_manager = ResourceManager()
    config_store = ConfigStore(resource_manager.get_user_config_file())

    global_ready = ensure_global_config_ready(load_global_config=config_store.load_global_config)
    if not global_ready.ok:
        missing = "、".join(global_ready.missing_fields)
        raise RuntimeError(f"全局配置缺失: {missing}")

    config_groups, current_index = config_store.load_config_groups()
    if not config_groups:
        raise RuntimeError("没有可用的配置组")

    selected_index = (
        args.current_config_index
        if args.current_config_index is not None
        else current_index
    )
    if not (0 <= selected_index < len(config_groups)):
        raise RuntimeError(
            f"current_config_index 越界: index={selected_index}, count={len(config_groups)}"
        )

    config = dict(config_groups[selected_index])
    config["debug_mode"] = bool(args.debug_mode)
    config["disable_ssl_strict_mode"] = bool(args.disable_ssl_strict_mode)
    runtime_config = build_proxy_config(
        get_current_config=lambda: config,
        debug_mode=bool(args.debug_mode),
        disable_ssl_strict_mode=bool(args.disable_ssl_strict_mode),
        stream_mode=None,
    )
    if runtime_config is None:
        raise RuntimeError("构建代理配置失败")
    return runtime_config, resource_manager.get_user_config_file()


def _build_proxy_app(args: argparse.Namespace) -> tuple[ProxyApp, dict[str, Any], str]:
    runtime_config, config_file = _load_runtime_config(args)
    resource_manager = ResourceManager()
    app = ProxyApp(
        runtime_config,
        _log,
        resource_manager=resource_manager,
    )
    if not app.valid or app.app is None:
        raise RuntimeError("ProxyApp 初始化失败")
    return app, runtime_config, config_file


def _install_signal_handlers(server: ThreadedWSGIServer, proxy_app: ProxyApp) -> None:
    def _handle_signal(_signum: int, _frame: Any) -> None:
        _log("收到停止信号，准备关闭 loopback 服务...")
        with_server = getattr(server, "shutdown_signal", None)
        if callable(with_server):
            with_server()
        server.server_close()
        proxy_app.close()
        raise SystemExit(0)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _handle_signal)
        except Exception:
            continue


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = _build_parser().parse_args()
    proxy_app, runtime_config, config_file = _build_proxy_app(args)

    server = ThreadedWSGIServer(args.host, args.port, proxy_app.app)
    server.RequestHandlerClass = WSGIRequestHandler
    _install_signal_handlers(server, proxy_app)

    payload = {
        "host": args.host,
        "port": args.port,
        "config_file": config_file,
        "target_api_base_url": runtime_config["api_url"],
        "mapped_model_id": proxy_app.custom_model_id,
        "target_model_id": proxy_app.target_model_id,
        "inbound_route": proxy_app.inbound_route,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"[loopback] listen=http://{args.host}:{args.port}{proxy_app.inbound_route}")
        print(f"[loopback] config_file={config_file}")
        print(f"[loopback] target_api_base_url={runtime_config['api_url']}")
        print(f"[loopback] mapped_model_id={proxy_app.custom_model_id}")
        print(f"[loopback] target_model_id={proxy_app.target_model_id}")
        print("[loopback] ready")

    try:
        server.serve_forever()
    finally:
        server.server_close()
        proxy_app.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
