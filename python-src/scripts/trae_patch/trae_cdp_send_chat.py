from __future__ import annotations

import argparse
import asyncio
import contextlib
import json
import sys
from collections.abc import Mapping
from typing import Any

import aiohttp
from trae_cdp_targets import CdpTarget, fetch_targets

DEFAULT_REMOTE_DEBUGGING_HOST = "127.0.0.1"
DEFAULT_REMOTE_DEBUGGING_PORT = 9330
DEFAULT_TARGET_URL_SUBSTRING = "workbench/workbench.html"
DEFAULT_TARGET_TITLE_SUBSTRING = ""
DEFAULT_WAIT_AFTER_SEND_SECONDS = 0.5

SEND_EXPRESSION_TEMPLATE = r"""(async () => {
  const message = __MESSAGE__;

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

  function isDisabled(element) {
    if (!(element instanceof HTMLElement)) {
      return true;
    }
    if (element.hasAttribute("disabled")) {
      return true;
    }
    return element.getAttribute("aria-disabled") === "true";
  }

  function summarizeElement(element) {
    const rect = element.getBoundingClientRect();
    return {
      tag: element.tagName.toLowerCase(),
      id: element.id || "",
      role: element.getAttribute("role") || "",
      ariaLabel: element.getAttribute("aria-label") || "",
      placeholder: element.getAttribute("placeholder") || "",
      className: preview(element.className || ""),
      text: preview(element.innerText || element.textContent || ""),
      rect: {
        x: Math.round(rect.x),
        y: Math.round(rect.y),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      },
    };
  }

  function scoreInput(element) {
    let score = 0;
    const tag = element.tagName.toLowerCase();
    const role = element.getAttribute("role") || "";
    const placeholder = (element.getAttribute("placeholder") || "").toLowerCase();
    const ariaLabel = (element.getAttribute("aria-label") || "").toLowerCase();
    const className = String(element.className || "").toLowerCase();
    const haystack = `${placeholder} ${ariaLabel} ${className}`;
    const rect = element.getBoundingClientRect();

    if (tag === "textarea") {
      score += 60;
    }
    if (tag === "input") {
      score += 20;
    }
    if (element.getAttribute("contenteditable") === "true") {
      score += 50;
    }
    if (role === "textbox") {
      score += 30;
    }
    if (haystack.includes("chat") || haystack.includes("message") || haystack.includes("问题")) {
      score += 40;
    }
    score += Math.min(rect.width, 800) / 20;
    score += Math.min(rect.height, 400) / 10;
    return score;
  }

  function scoreButton(element) {
    let score = 0;
    const role = (element.getAttribute("role") || "").toLowerCase();
    const type = (element.getAttribute("type") || "").toLowerCase();
    const haystack = [
      element.innerText || "",
      element.textContent || "",
      element.getAttribute("aria-label") || "",
      element.getAttribute("title") || "",
      element.getAttribute("data-testid") || "",
      String(element.className || ""),
    ].join(" ").toLowerCase();
    const rect = element.getBoundingClientRect();

    if (role === "combobox") {
      return -1000;
    }
    if (
      haystack.includes("asr") ||
      haystack.includes("record") ||
      haystack.includes("voice") ||
      haystack.includes("audio") ||
      haystack.includes("mic") ||
      haystack.includes("microphone")
    ) {
      score -= 600;
    }
    if (
      haystack.includes("model-select") ||
      haystack.includes("model") ||
      haystack.includes("trigger")
    ) {
      score -= 200;
    }
    if (haystack.includes("send-button")) {
      score += 400;
    }
    if (type === "button") {
      score += 20;
    }
    if (
      haystack.includes("send") ||
      haystack.includes("submit") ||
      haystack.includes("发送") ||
      haystack.includes("提问") ||
      haystack.includes("chat")
    ) {
      score += 80;
    }
    if (haystack.includes("arrow") || haystack.includes("plane")) {
      score += 15;
    }
    score += Math.min(rect.width, 200) / 10;
    score += Math.min(rect.height, 100) / 10;
    return score;
  }

  function setNativeValue(element, value) {
    const prototype = Object.getPrototypeOf(element);
    const descriptor = prototype
      ? Object.getOwnPropertyDescriptor(prototype, "value")
      : null;
    if (descriptor && typeof descriptor.set === "function") {
      descriptor.set.call(element, value);
      return true;
    }
    return false;
  }

  function dispatchTextEvents(element) {
    element.dispatchEvent(new Event("input", { bubbles: true }));
    element.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function replaceContentEditableText(element, value) {
    const selection = window.getSelection();
    if (!selection) {
      return false;
    }
    const range = document.createRange();
    range.selectNodeContents(element);
    selection.removeAllRanges();
    selection.addRange(range);
    if (typeof document.execCommand === "function") {
      document.execCommand("delete", false);
      if (document.execCommand("insertText", false, value)) {
        return true;
      }
    }
    selection.removeAllRanges();
    return false;
  }

  function fillInput(element, value) {
    element.focus();

    if (element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement) {
      if (!setNativeValue(element, value)) {
        element.value = value;
      }
      dispatchTextEvents(element);
      return "value";
    }

    if (
      element.getAttribute("contenteditable") === "true" ||
      element.getAttribute("role") === "textbox"
    ) {
      element.textContent = "";
      if (replaceContentEditableText(element, value)) {
        dispatchTextEvents(element);
        return "contenteditable_execCommand";
      }
      element.textContent = value;
      element.dispatchEvent(new InputEvent("input", {
        bubbles: true,
        data: value,
        inputType: "insertText",
      }));
      element.dispatchEvent(new Event("change", { bubbles: true }));
      return "contenteditable";
    }

    return "unsupported";
  }

  function readInputValue(element) {
    if (element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement) {
      return element.value || "";
    }
    if (
      element.getAttribute("contenteditable") === "true" ||
      element.getAttribute("role") === "textbox"
    ) {
      return element.innerText || element.textContent || "";
    }
    return "";
  }

  function clickButton(element) {
    element.focus();
    element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true }));
    element.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true }));
    element.click();
  }

  function submitByKeyboard(element) {
    element.focus();
    const options = {
      key: "Enter",
      code: "Enter",
      which: 13,
      keyCode: 13,
      bubbles: true,
      cancelable: true,
      ctrlKey: false,
      metaKey: false,
      shiftKey: false,
    };
    element.dispatchEvent(new KeyboardEvent("keydown", options));
    element.dispatchEvent(new KeyboardEvent("keypress", options));
    element.dispatchEvent(new KeyboardEvent("keyup", options));
  }

  function sleep(ms) {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }

  async function submitWithRetries(input, originalMessage) {
    const attempts = [];
    const delays = [0, 80, 200, 400];
    let lastButton = null;

    for (let index = 0; index < delays.length; index += 1) {
      const delay = delays[index];
      if (delay > 0) {
        await sleep(delay);
      }

      const button = findSendButton(input);
      lastButton = button;
      const before = preview(readInputValue(input), 80);

      if (button) {
        clickButton(button);
      } else {
        submitByKeyboard(input);
      }

      await sleep(120);

      const afterRaw = readInputValue(input);
      const after = preview(afterRaw, 80);
      const cleared = afterRaw.trim() !== originalMessage.trim();
      attempts.push({
        attempt: index + 1,
        delay,
        usedButton: Boolean(button),
        before,
        after,
        cleared,
      });
      if (cleared) {
        return {
          submitMode: button ? "button_verified" : "keyboard_verified",
          attempts,
          button: lastButton,
          cleared,
          finalValue: after,
        };
      }
    }

    return {
      submitMode: lastButton ? "button_unverified" : "keyboard_unverified",
      attempts,
      button: lastButton,
      cleared: false,
      finalValue: preview(readInputValue(input), 80),
    };
  }

  function findSendButton(input) {
    const buttonSelectors = ["button", "[role='button']"];
    const containers = [];
    for (let current = input; current instanceof Element; current = current.parentElement) {
      containers.push(current);
    }
    containers.push(document.body);

    const exactSendButton = document.querySelector(
      ".chat-input-v2-send-button:not([disabled]):not([aria-disabled='true'])"
    );
    if (exactSendButton && isVisible(exactSendButton) && !isDisabled(exactSendButton)) {
      return exactSendButton;
    }

    for (const container of containers) {
      const candidates = Array.from(container.querySelectorAll(buttonSelectors.join(",")))
        .filter((element) => isVisible(element) && !isDisabled(element))
        .sort((left, right) => scoreButton(right) - scoreButton(left));
      if (candidates.length > 0 && scoreButton(candidates[0]) >= 120) {
        return candidates[0];
      }
    }
    return null;
  }

  const inputSelectors = [
    "textarea",
    "input[type='text']",
    "input:not([type])",
    "[contenteditable='true']",
    "[role='textbox']",
  ];

  const inputs = Array.from(document.querySelectorAll(inputSelectors.join(",")))
    .filter((element) => isVisible(element) && !isDisabled(element))
    .sort((left, right) => scoreInput(right) - scoreInput(left));

  const input = inputs[0];
  if (!input) {
    return { status: "no_input" };
  }

  const fillMode = fillInput(input, message);
  const submitResult = await submitWithRetries(input, message);
  const button = submitResult.button;

  return {
    status: submitResult.cleared ? "sent" : "submission_unverified",
    fillMode,
    submitMode: submitResult.submitMode,
    attempts: submitResult.attempts,
    inputCleared: submitResult.cleared,
    inputValueAfterSubmit: submitResult.finalValue,
    input: summarizeElement(input),
    button: button ? summarizeElement(button) : null,
    messagePreview: preview(message),
  };
})()"""


class CdpClient:
    def __init__(self, websocket_url: str) -> None:
        self._websocket_url = websocket_url
        self._session: aiohttp.ClientSession | None = None
        self._socket: aiohttp.ClientWebSocketResponse | None = None
        self._reader_task: asyncio.Task[None] | None = None
        self._command_id = 0
        self._pending: dict[int, asyncio.Future[dict[str, Any]]] = {}

    async def __aenter__(self) -> CdpClient:
        self._session = aiohttp.ClientSession()
        self._socket = await self._session.ws_connect(self._websocket_url, heartbeat=30)
        self._reader_task = asyncio.create_task(self._reader_loop())
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        reader_task = self._reader_task
        self._reader_task = None
        if reader_task is not None:
            reader_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await reader_task

        socket = self._socket
        self._socket = None
        if socket is not None:
            await socket.close()

        session = self._session
        self._session = None
        if session is not None:
            await session.close()

    async def send(self, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        socket = self._socket
        if socket is None:
            raise RuntimeError("CDP websocket 尚未连接")

        self._command_id += 1
        command_id = self._command_id
        future: asyncio.Future[dict[str, Any]] = asyncio.get_running_loop().create_future()
        self._pending[command_id] = future
        payload: dict[str, Any] = {"id": command_id, "method": method}
        if params:
            payload["params"] = dict(params)
        await socket.send_json(payload)
        response = await future
        if "error" in response:
            raise RuntimeError(f"CDP {method} 失败: {response['error']}")
        result = response.get("result", {})
        return result if isinstance(result, dict) else {}

    async def _reader_loop(self) -> None:
        socket = self._socket
        if socket is None:
            return

        async for message in socket:
            if message.type != aiohttp.WSMsgType.TEXT:
                continue
            payload = json.loads(message.data)
            response_id = payload.get("id")
            if not isinstance(response_id, int):
                continue
            future = self._pending.pop(response_id, None)
            if future is not None and not future.done():
                future.set_result(payload)


def _extract_result_value(result: Mapping[str, Any]) -> Any:
    inner = result.get("result")
    if not isinstance(inner, Mapping):
        return None
    if inner.get("type") == "undefined":
        return None
    if "value" in inner:
        return inner["value"]
    return inner


def _build_send_expression(message: str) -> str:
    return SEND_EXPRESSION_TEMPLATE.replace("__MESSAGE__", json.dumps(message, ensure_ascii=False))


def _pick_target(
    targets: list[CdpTarget],
    url_substring: str,
    title_substring: str = DEFAULT_TARGET_TITLE_SUBSTRING,
) -> CdpTarget:
    candidates = [
        target
        for target in targets
        if target.type == "page" and url_substring in target.url
    ]
    if title_substring:
        for target in candidates:
            if title_substring in target.title:
                return target
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise RuntimeError(
            "未找到 page target，"
            f"url_substring={url_substring!r}, title_substring={title_substring!r}"
        )
    raise RuntimeError(
        "page target 匹配到多个候选，请补充 --target-title-substring："
        + json.dumps(
            [
                {
                    "id": target.id,
                    "title": target.title,
                    "url": target.url,
                }
                for target in candidates
            ],
            ensure_ascii=False,
        )
    )


async def _send_message(target: CdpTarget, message: str) -> dict[str, Any]:
    if not target.web_socket_debugger_url:
        raise RuntimeError(f"target 缺少 websocket: {target.id}")

    async with CdpClient(target.web_socket_debugger_url) as client:
        await client.send("Runtime.enable")
        result = await client.send(
            "Runtime.evaluate",
            {
                "expression": _build_send_expression(message),
                "awaitPromise": True,
                "returnByValue": True,
            },
        )

    value = _extract_result_value(result)
    if not isinstance(value, dict):
        raise RuntimeError("CDP send 返回格式无效")
    return {
        "target": {
            "id": target.id,
            "title": target.title,
            "url": target.url,
        },
        "send_result": value,
    }


async def main_async(args: argparse.Namespace) -> dict[str, Any]:
    targets = fetch_targets(args.host, args.port)
    target = _pick_target(
        targets,
        args.target_url_substring,
        args.target_title_substring,
    )
    payload = await _send_message(target, args.message)
    if args.wait_after_send_seconds > 0:
      await asyncio.sleep(args.wait_after_send_seconds)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="通过 CDP 向当前 Trae chat 输入并发送一条消息。")
    parser.add_argument("--message", required=True, help="要发送的消息")
    parser.add_argument("--host", default=DEFAULT_REMOTE_DEBUGGING_HOST, help="CDP host")
    parser.add_argument("--port", type=int, default=DEFAULT_REMOTE_DEBUGGING_PORT, help="CDP port")
    parser.add_argument(
        "--target-url-substring",
        default=DEFAULT_TARGET_URL_SUBSTRING,
        help="目标 page URL 子串",
    )
    parser.add_argument(
        "--target-title-substring",
        default=DEFAULT_TARGET_TITLE_SUBSTRING,
        help="可选：目标 page 标题子串",
    )
    parser.add_argument(
        "--wait-after-send-seconds",
        type=float,
        default=DEFAULT_WAIT_AFTER_SEND_SECONDS,
        help="发送后额外等待秒数",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    try:
        payload = asyncio.run(main_async(args))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
