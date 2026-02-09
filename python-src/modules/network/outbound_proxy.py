from __future__ import annotations

from urllib.parse import quote

import requests

from modules.runtime.resource_manager import ResourceManager
from modules.services.config_service import ConfigStore


def _load_settings() -> dict[str, object]:
    store = ConfigStore(ResourceManager().get_user_config_file())
    return store.load_outbound_proxy_config()


def _build_proxy_url(settings: dict[str, object]) -> str | None:
    proxy_type = str(settings.get("outbound_proxy_type") or "http").lower()
    host = str(settings.get("outbound_proxy_host") or "").strip()
    port_value = settings.get("outbound_proxy_port")
    port = 0
    if isinstance(port_value, int):
        port = port_value
    elif isinstance(port_value, float):
        port = int(port_value)
    elif isinstance(port_value, str):
        try:
            port = int(port_value)
        except ValueError:
            port = 0
    if not host or port <= 0:
        return None
    username = settings.get("outbound_proxy_username") or ""
    password = settings.get("outbound_proxy_password") or ""
    auth = ""
    if isinstance(username, str) and username:
        encoded_user = quote(username, safe="")
        if isinstance(password, str) and password:
            encoded_pass = quote(password, safe="")
            auth = f"{encoded_user}:{encoded_pass}@"
        else:
            auth = f"{encoded_user}@"
    return f"{proxy_type}://{auth}{host}:{port}"


def apply_outbound_proxy(session: requests.Session) -> None:
    settings = _load_settings()
    enabled = settings.get("outbound_proxy_enabled") is True
    session.trust_env = False
    if not enabled:
        return
    proxy_url = _build_proxy_url(settings)
    if not proxy_url:
        return
    session.proxies = {"http": proxy_url, "https": proxy_url}


def create_outbound_session() -> requests.Session:
    session = requests.Session()
    apply_outbound_proxy(session)
    return session


__all__ = ["apply_outbound_proxy", "create_outbound_session"]
