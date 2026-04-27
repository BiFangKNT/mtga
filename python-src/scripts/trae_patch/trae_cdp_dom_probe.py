from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

from trae_cdp_send_chat import (  # noqa: PLC2701
    DEFAULT_REMOTE_DEBUGGING_HOST,
    DEFAULT_REMOTE_DEBUGGING_PORT,
    DEFAULT_TARGET_TITLE_SUBSTRING,
    DEFAULT_TARGET_URL_SUBSTRING,
    CdpClient,
    _extract_result_value,
    _pick_target,
)
from trae_cdp_targets import fetch_targets

PROBE_EXPRESSION = r"""(() => {
  function preview(value, limit = 160) {
    const text = String(value ?? "").replace(/\s+/g, " ").trim();
    return text.length > limit ? `${text.slice(0, limit)}...(len=${text.length})` : text;
  }

  function isVisible(element) {
    if (!(element instanceof Element)) {
      return false;
    }
    const style = window.getComputedStyle(element);
    if (style.display === "none" || style.visibility === "hidden") {
      return false;
    }
    const rect = element.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  function summarize(element) {
    const rect = element.getBoundingClientRect();
    return {
      tag: element.tagName.toLowerCase(),
      role: element.getAttribute("role") || "",
      id: element.id || "",
      ariaLabel: element.getAttribute("aria-label") || "",
      title: element.getAttribute("title") || "",
      placeholder: element.getAttribute("placeholder") || "",
      className: preview(String(element.className || "")),
      text: preview(element.innerText || element.textContent || ""),
      rect: {
        x: Math.round(rect.x),
        y: Math.round(rect.y),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      },
    };
  }

  const buttonSelectors = "button, [role='button'], [role='tab'], a, summary";
  const textboxSelectors = "textarea, input, [role='textbox'], [contenteditable='true']";
  const keywordSelectors = "[class*='icube'], [class*='chat'], [class*='agent'], [class*='panel']";

  return {
    location: window.location.href,
    title: document.title,
    activeElement: document.activeElement instanceof Element
      ? summarize(document.activeElement)
      : null,
    selectedAgent: (() => {
      const element = document.querySelector(".chat-input-selected-agent-name");
      return element instanceof HTMLElement
        ? preview(element.innerText || element.textContent || "")
        : "";
    })(),
    buttons: Array.from(document.querySelectorAll(buttonSelectors))
      .filter(isVisible)
      .map(summarize)
      .slice(0, 120),
    textboxes: Array.from(document.querySelectorAll(textboxSelectors))
      .filter(isVisible)
      .map(summarize)
      .slice(0, 120),
    keywords: Array.from(document.querySelectorAll(keywordSelectors))
      .filter(isVisible)
      .map(summarize)
      .slice(0, 160),
  };
})()"""


async def _probe_dom(
    *,
    host: str,
    port: int,
    target_url_substring: str,
    target_title_substring: str,
) -> dict[str, Any]:
    targets = fetch_targets(host=host, port=port)
    target = _pick_target(targets, target_url_substring, target_title_substring)
    async with CdpClient(target.web_socket_debugger_url) as client:
        await client.send("Runtime.enable")
        result = await client.send(
            "Runtime.evaluate",
            {
                "expression": PROBE_EXPRESSION,
                "awaitPromise": True,
                "returnByValue": True,
            },
        )
    value = _extract_result_value(result)
    return {
        "target": {
            "id": target.id,
            "title": target.title,
            "url": target.url,
        },
        "probe": value if isinstance(value, dict) else {"raw": value},
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="通过 CDP 导出当前 Trae workbench 的可见 DOM 探针。"
    )
    parser.add_argument("--host", default=DEFAULT_REMOTE_DEBUGGING_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_REMOTE_DEBUGGING_PORT)
    parser.add_argument("--target-url-substring", default=DEFAULT_TARGET_URL_SUBSTRING)
    parser.add_argument("--target-title-substring", default=DEFAULT_TARGET_TITLE_SUBSTRING)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    payload = asyncio.run(
        _probe_dom(
            host=args.host,
            port=args.port,
            target_url_substring=args.target_url_substring,
            target_title_substring=args.target_title_substring,
        )
    )
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text if args.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
