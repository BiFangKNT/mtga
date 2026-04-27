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
DEFAULT_TARGET_WAIT_SECONDS = 20.0
DEFAULT_TARGET_POLL_SECONDS = 0.25
DEFAULT_CHAT_MODE = "ide"
DEFAULT_AGENT_NAME = "Builder"

SEND_EXPRESSION_TEMPLATE = r"""(async () => {
  const message = __MESSAGE__;
  const targetMode = __TARGET_MODE__;
  const targetAgentName = __TARGET_AGENT_NAME__;

  function preview(value, limit = 160) {
    const text = String(value ?? "").replace(/\s+/g, " ").trim();
    return text.length > limit ? `${text.slice(0, limit)}...(len=${text.length})` : text;
  }

  function normalizeLabel(value) {
    return String(value ?? "")
      .replace(/\s+/g, " ")
      .trim()
      .replace(/^@+/, "")
      .toLowerCase();
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
    const isChatInput = (
      className.includes("chat-input") ||
      Boolean(element.closest("[class*='chat-input']"))
    );
    const isEditorInput = (
      className.includes("inputarea") ||
      className.includes("monaco") ||
      ariaLabel.includes("编辑器") ||
      ariaLabel.includes("screen reader") ||
      ariaLabel.includes("现在无法访问编辑器")
    );

    if (isEditorInput) {
      score -= 500;
    }
    if (isChatInput) {
      score += 400;
    }

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

  function isChatInputElement(element) {
    if (!(element instanceof HTMLElement)) {
      return false;
    }
    const className = String(element.className || "").toLowerCase();
    const ariaLabel = (element.getAttribute("aria-label") || "").toLowerCase();
    return (
      className.includes("chat-input") ||
      Boolean(element.closest("[class*='chat-input']")) ||
      ariaLabel.includes("solo coder") ||
      ariaLabel.includes("builder") ||
      ariaLabel.includes("chat")
    );
  }

  function isEditorInputElement(element) {
    if (!(element instanceof HTMLElement)) {
      return false;
    }
    const className = String(element.className || "").toLowerCase();
    const ariaLabel = (element.getAttribute("aria-label") || "").toLowerCase();
    return (
      className.includes("inputarea") ||
      className.includes("monaco") ||
      ariaLabel.includes("编辑器") ||
      ariaLabel.includes("screen reader") ||
      ariaLabel.includes("现在无法访问编辑器")
    );
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

  function collectInputCandidates() {
    const selectors = [
      ".chat-input-v2-input-box-editable",
      "[class*='chat-input'][role='textbox']",
      "textarea",
      "input[type='text']",
      "input:not([type])",
      "[contenteditable='true']",
      "[role='textbox']",
    ];
    return Array.from(document.querySelectorAll(selectors.join(",")))
      .filter((element) => isVisible(element) && !isDisabled(element))
      .map((element) => ({
        element,
        score: scoreInput(element),
        kind: isChatInputElement(element)
          ? "chat"
          : isEditorInputElement(element)
            ? "editor"
            : "generic",
      }))
      .sort((left, right) => right.score - left.score);
  }

  function summarizeInputCandidate(candidate) {
    return {
      kind: candidate.kind,
      score: Math.round(candidate.score),
      element: summarizeElement(candidate.element),
    };
  }

  function findPrimaryInput() {
    const candidates = collectInputCandidates();
    if (candidates.length === 0) {
      return {
        input: null,
        candidates,
      };
    }
    const chatCandidate = candidates.find((candidate) => candidate.kind === "chat");
    if (chatCandidate) {
      return {
        input: chatCandidate.element,
        candidates,
      };
    }
    return {
      input: candidates[0].element,
      candidates,
    };
  }

  function clickIfVisible(element) {
    if (!(element instanceof HTMLElement) || !isVisible(element) || isDisabled(element)) {
      return false;
    }
    clickButton(element);
    return true;
  }

  function findModeTrigger(mode) {
    const selectorMap = {
      solo: [
        ".icube-mode-tab-item-solo",
        ".icube-mode-tab-item.icube-mode-tab-item-solo",
        ".icube-mode-tab-switch",
      ],
      ide: [
        ".icube-mode-tab-item-ide",
        ".icube-mode-tab-item.icube-mode-tab-item-ide",
      ],
    };
    const selectors = selectorMap[mode] || [];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element instanceof HTMLElement && isVisible(element) && !isDisabled(element)) {
        return {
          element,
          label: `click:${selector}`,
        };
      }
    }

    const allElements = Array.from(
      document.querySelectorAll("button, [role='button'], a, div, span")
    );
    const soloByText = allElements.find((element) => {
      const text = [
        element.getAttribute("aria-label") || "",
        element.getAttribute("title") || "",
        element.textContent || "",
        String(element.className || ""),
      ].join(" ").toLowerCase();
      return text.includes(mode);
    });
    if (soloByText instanceof HTMLElement && isVisible(soloByText) && !isDisabled(soloByText)) {
      return {
        element: soloByText,
        label: `click:text=${mode}`,
      };
    }
    return null;
  }

  async function switchToMode(mode) {
    const actions = [];
    if (mode === "current") {
      return actions;
    }

    const trigger = findModeTrigger(mode);
    if (trigger && clickIfVisible(trigger.element)) {
      actions.push(trigger.label);
      await sleep(1200);
      return actions;
    }

    if (mode !== "solo") {
      return actions;
    }

    const target = document.activeElement instanceof HTMLElement
      ? document.activeElement
      : document.body;
    const options = {
      key: "\\",
      code: "Backslash",
      which: 220,
      keyCode: 220,
      bubbles: true,
      cancelable: true,
      altKey: true,
      metaKey: true,
      ctrlKey: false,
      shiftKey: false,
    };
    target.dispatchEvent(new KeyboardEvent("keydown", options));
    target.dispatchEvent(new KeyboardEvent("keyup", options));
    actions.push("shortcut:Alt+Meta+Backslash");
    await sleep(1200);
    return actions;
  }

  function readSelectedAgent() {
    const element = document.querySelector(".chat-input-selected-agent-name");
    if (!(element instanceof HTMLElement)) {
      return "";
    }
    return String(element.innerText || element.textContent || "").trim();
  }

  function isExpectedAgentSelected() {
    if (!targetAgentName || targetAgentName === "current") {
      return true;
    }
    return normalizeLabel(readSelectedAgent()) === normalizeLabel(targetAgentName);
  }

  async function ensureChatInput() {
    const modeAttempts = [];
    let state = findPrimaryInput();

    for (let index = 0; index < 12; index += 1) {
      const selectedAgent = readSelectedAgent();
      state = findPrimaryInput();
      if (
        state.input &&
        isChatInputElement(state.input) &&
        isExpectedAgentSelected()
      ) {
        return {
          input: state.input,
          candidates: state.candidates,
          modeAttempts,
          selectedAgent,
          agentMatched: true,
        };
      }

      const actions = await switchToMode(targetMode);
      if (actions.length > 0) {
        modeAttempts.push(...actions);
        state = findPrimaryInput();
        if (
          state.input &&
          isChatInputElement(state.input) &&
          isExpectedAgentSelected()
        ) {
          return {
            input: state.input,
            candidates: state.candidates,
            modeAttempts,
            selectedAgent: readSelectedAgent(),
            agentMatched: true,
          };
        }
      }

      await sleep(500);
    }

    modeAttempts.push(...await switchToMode(targetMode));
    state = findPrimaryInput();
    if (state.input) {
      if (isChatInputElement(state.input) && isExpectedAgentSelected()) {
        return {
          input: state.input,
          candidates: state.candidates,
          modeAttempts,
          selectedAgent: readSelectedAgent(),
          agentMatched: true,
        };
      }
      const panelToggle = document.querySelector(
        ".icube-panel-toggle-button, .icube-panel-toggle-button-icon"
      );
      if (clickIfVisible(panelToggle)) {
        modeAttempts.push("click:panel-toggle");
        await sleep(800);
        state = findPrimaryInput();
      }
    }
    return {
      input: state.input,
      candidates: state.candidates,
      modeAttempts,
      selectedAgent: readSelectedAgent(),
      agentMatched: isExpectedAgentSelected(),
    };
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

  const ready = await ensureChatInput();
  const input = ready.input;
  if (!ready.agentMatched) {
    return {
      status: "agent_mismatch",
      modeTarget: targetMode,
      agentTarget: targetAgentName,
      selectedAgent: ready.selectedAgent,
      modeAttempts: ready.modeAttempts,
      candidates: ready.candidates.slice(0, 6).map(summarizeInputCandidate),
    };
  }
  if (!input || !isChatInputElement(input)) {
    return {
      status: "no_input",
      modeTarget: targetMode,
      agentTarget: targetAgentName,
      selectedAgent: ready.selectedAgent,
      modeAttempts: ready.modeAttempts,
      candidates: ready.candidates.slice(0, 6).map(summarizeInputCandidate),
    };
  }

  const fillMode = fillInput(input, message);
  const submitResult = await submitWithRetries(input, message);
  const button = submitResult.button;

  return {
    status: submitResult.cleared ? "sent" : "submission_unverified",
    modeTarget: targetMode,
    agentTarget: targetAgentName,
    selectedAgent: ready.selectedAgent,
    fillMode,
    submitMode: submitResult.submitMode,
    attempts: submitResult.attempts,
    inputCleared: submitResult.cleared,
    inputValueAfterSubmit: submitResult.finalValue,
    modeAttempts: ready.modeAttempts,
    candidates: ready.candidates.slice(0, 6).map(summarizeInputCandidate),
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


def _build_send_expression(
    message: str,
    *,
    mode: str,
    agent_name: str,
) -> str:
    return (
        SEND_EXPRESSION_TEMPLATE
        .replace("__MESSAGE__", json.dumps(message, ensure_ascii=False))
        .replace("__TARGET_MODE__", json.dumps(mode, ensure_ascii=False))
        .replace("__TARGET_AGENT_NAME__", json.dumps(agent_name, ensure_ascii=False))
    )


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


async def _send_message(
    target: CdpTarget,
    message: str,
    *,
    mode: str,
    agent_name: str,
) -> dict[str, Any]:
    if not target.web_socket_debugger_url:
        raise RuntimeError(f"target 缺少 websocket: {target.id}")

    async with CdpClient(target.web_socket_debugger_url) as client:
        await client.send("Runtime.enable")
        result = await client.send(
            "Runtime.evaluate",
            {
                "expression": _build_send_expression(
                    message,
                    mode=mode,
                    agent_name=agent_name,
                ),
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


async def _wait_target(
    *,
    host: str,
    port: int,
    url_substring: str,
    title_substring: str,
    timeout_seconds: float,
) -> CdpTarget:
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    last_error: Exception | None = None

    while True:
        try:
            targets = fetch_targets(host, port)
            return _pick_target(targets, url_substring, title_substring)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if asyncio.get_running_loop().time() >= deadline:
                break
            await asyncio.sleep(DEFAULT_TARGET_POLL_SECONDS)

    message = str(last_error) if last_error is not None else "page target wait failed"
    raise RuntimeError(message)


async def main_async(args: argparse.Namespace) -> dict[str, Any]:
    target = await _wait_target(
        host=args.host,
        port=args.port,
        url_substring=args.target_url_substring,
        title_substring=args.target_title_substring,
        timeout_seconds=args.target_wait_seconds,
    )
    payload = await _send_message(
        target,
        args.message,
        mode=args.mode,
        agent_name=args.agent_name,
    )
    if args.wait_after_send_seconds > 0:
        await asyncio.sleep(args.wait_after_send_seconds)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "通过 CDP 向当前 Trae chat 输入并发送一条消息。"
            "默认切到 IDE，并要求 agent 为 Builder。"
        )
    )
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
    parser.add_argument(
        "--target-wait-seconds",
        type=float,
        default=DEFAULT_TARGET_WAIT_SECONDS,
        help="等待 workbench page target 就绪的秒数",
    )
    parser.add_argument(
        "--mode",
        choices=("ide", "solo", "current"),
        default=DEFAULT_CHAT_MODE,
        help="发送前优先切换的模式，默认 ide",
    )
    parser.add_argument(
        "--agent-name",
        default=DEFAULT_AGENT_NAME,
        help="发送前要求的已选 agent 名称；传 current 可跳过校验，默认 Builder",
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
