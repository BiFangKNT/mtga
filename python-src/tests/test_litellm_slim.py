from __future__ import annotations

import unittest
from typing import Any
from unittest.mock import patch

import httpx

import litellm
from litellm import APIConnectionError
from litellm.exceptions import BadRequestError
from litellm.gemini import _sanitize_empty_gemini_prompt_feedback


class _ConnectErrorStream:
    def __enter__(self) -> httpx.Response:
        request = httpx.Request("POST", "https://example.com/v1/chat/completions")
        raise httpx.ConnectError("connect failed", request=request)

    def __exit__(self, *args: Any) -> None:
        return None


class _ResponseStream:
    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        self.closed = False

    def __enter__(self) -> httpx.Response:
        return self.response

    def __exit__(self, *args: Any) -> None:
        self.closed = True
        self.response.close()


class LiteLLMSlimTests(unittest.TestCase):
    def test_openai_chat_completion_posts_to_chat_completions(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://example.com/v1/chat/completions"),
            json={"id": "chatcmpl_123", "choices": []},
        )

        with patch("litellm.httpx.request", return_value=response) as request_mock:
            result = litellm.completion(
                model="gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
                api_key="test-key",
                extra_body={"return_reasoning": True},
            )

        self.assertEqual(result, {"id": "chatcmpl_123", "choices": []})
        request_kwargs = request_mock.call_args.kwargs
        self.assertEqual(
            request_mock.call_args.args[:2],
            ("POST", "https://example.com/v1/chat/completions"),
        )
        self.assertEqual(request_kwargs["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(
            request_kwargs["json"],
            {
                "model": "gpt-5",
                "messages": [{"role": "user", "content": "hello"}],
                "return_reasoning": True,
            },
        )

    def test_openai_responses_converts_chat_content_part_types(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://example.com/v1/responses"),
            json={
                "id": "resp_123",
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": "ok"}],
                    }
                ],
            },
        )
        user_text_part = {"type": "text", "text": "hello"}
        assistant_text_part = {"type": "text", "text": "history"}

        with patch("litellm.httpx.request", return_value=response) as request_mock:
            result = litellm.completion(
                model="responses/gpt-5",
                messages=[
                    {"role": "system", "content": "rules"},
                    {
                        "role": "user",
                        "content": [
                            user_text_part,
                            {
                                "type": "image_url",
                                "image_url": {"url": "https://example.com/a.png"},
                            },
                        ],
                    },
                    {
                        "role": "assistant",
                        "content": [assistant_text_part],
                    },
                ],
                base_url="https://example.com/v1",
            )

        self.assertEqual(result["choices"][0]["message"]["content"], "ok")
        request_body = request_mock.call_args.kwargs["json"]
        user_content = request_body["input"][1]["content"]
        assistant_content = request_body["input"][2]["content"]
        self.assertEqual(user_content[0]["type"], "input_text")
        self.assertEqual(user_content[0]["text"], "hello")
        self.assertEqual(user_content[1]["type"], "input_image")
        self.assertEqual(user_content[1]["image_url"], "https://example.com/a.png")
        self.assertEqual(assistant_content[0]["type"], "output_text")
        self.assertEqual(user_text_part["type"], "text")
        self.assertEqual(assistant_text_part["type"], "text")

    def test_openai_responses_converts_chat_tools(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://example.com/v1/responses"),
            json={
                "id": "resp_123",
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": "ok"}],
                    }
                ],
            },
        )
        tool = {
            "type": "function",
            "function": {
                "name": "lookup",
                "description": "Lookup data",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
                "strict": True,
            },
        }
        tool_choice = {"type": "function", "function": {"name": "lookup"}}

        with patch("litellm.httpx.request", return_value=response) as request_mock:
            result = litellm.completion(
                model="responses/gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
                tools=[tool],
                tool_choice=tool_choice,
            )

        self.assertEqual(result["choices"][0]["message"]["content"], "ok")
        request_body = request_mock.call_args.kwargs["json"]
        self.assertEqual(
            request_body["tools"],
            [
                {
                    "type": "function",
                    "name": "lookup",
                    "description": "Lookup data",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"],
                    },
                    "strict": True,
                }
            ],
        )
        self.assertEqual(
            request_body["tool_choice"],
            {"type": "function", "name": "lookup"},
        )
        self.assertNotIn("function", request_body["tools"][0])
        self.assertEqual(tool["function"]["name"], "lookup")
        self.assertEqual(tool_choice["function"]["name"], "lookup")

    def test_openai_responses_maps_reasoning_to_reasoning_content(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://example.com/v1/responses"),
            json={
                "id": "resp_123",
                "status": "completed",
                "output": [
                    {
                        "type": "reasoning",
                        "summary": [
                            {"type": "summary_text", "text": "先分析"},
                        ],
                        "content": [
                            {"type": "reasoning_text", "text": "再验证"},
                        ],
                    },
                    {
                        "type": "message",
                        "content": [{"type": "output_text", "text": "答案"}],
                    },
                ],
            },
        )

        with patch("litellm.httpx.request", return_value=response):
            result = litellm.completion(
                model="responses/gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
            )

        message = result["choices"][0]["message"]
        self.assertEqual(message["reasoning_content"], "先分析再验证")
        self.assertEqual(message["content"], "答案")

    def test_openai_responses_stream_maps_reasoning_delta(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://example.com/v1/responses"),
            stream=httpx.ByteStream(
                (
                    'data: {"type":"response.reasoning_summary_text.delta",'
                    '"delta":"先想"}\n\n'
                    'data: {"type":"response.output_text.delta","delta":"答案"}\n\n'
                    'data: {"type":"response.completed"}\n\n'
                ).encode()
            ),
        )
        stream = _ResponseStream(response)

        with patch("litellm.httpx.stream", return_value=stream):
            iterator = litellm.completion(
                model="responses/gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
                stream=True,
            )

        chunks = list(iterator)
        self.assertEqual(chunks[1]["choices"][0]["delta"]["reasoning_content"], "先想")
        self.assertEqual(chunks[2]["choices"][0]["delta"]["content"], "答案")
        self.assertEqual(chunks[3]["choices"][0]["finish_reason"], "stop")
        self.assertTrue(stream.closed)

    def test_http_json_error_keeps_response_body(self) -> None:
        body = {"error": {"message": "bad request", "type": "invalid_request_error"}}
        response = httpx.Response(
            400,
            request=httpx.Request("POST", "https://example.com/v1/chat/completions"),
            json=body,
        )

        with (
            patch("litellm.httpx.request", return_value=response),
            self.assertRaises(BadRequestError) as raised,
        ):
            litellm.completion(
                model="gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
            )

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.body, body)
        self.assertIs(raised.exception.response, response)

    def test_http_text_error_keeps_response_for_raw_body_extraction(self) -> None:
        response = httpx.Response(
            400,
            request=httpx.Request("POST", "https://example.com/v1/chat/completions"),
            text="plain upstream error",
        )

        with (
            patch("litellm.httpx.request", return_value=response),
            self.assertRaises(BadRequestError) as raised,
        ):
            litellm.completion(
                model="gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
            )

        self.assertEqual(raised.exception.body, None)
        self.assertIs(raised.exception.response, response)
        self.assertEqual(raised.exception.response.text, "plain upstream error")

    def test_stream_connection_error_is_raised_before_returning_iterator(self) -> None:
        with (
            patch("litellm.httpx.stream", return_value=_ConnectErrorStream()),
            self.assertRaises(APIConnectionError),
        ):
            litellm.completion(
                model="gpt-5",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://example.com/v1",
                stream=True,
            )

    def test_gemini_stream_error_reads_body_before_raising(self) -> None:
        body = b'{"error":{"message":"gemini bad request","type":"invalid_request_error"}}'
        response = httpx.Response(
            400,
            request=httpx.Request(
                "POST",
                "https://gemini.example.com/v1beta/models/gemini-2.5-pro:streamGenerateContent",
            ),
            stream=httpx.ByteStream(body),
        )
        stream = _ResponseStream(response)

        with (
            patch("litellm.httpx.stream", return_value=stream),
            self.assertRaises(BadRequestError) as raised,
        ):
            litellm.completion(
                model="gemini/gemini-2.5-pro",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://gemini.example.com/v1beta",
                stream=True,
            )

        self.assertTrue(stream.closed)
        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(
            raised.exception.body,
            {
                "error": {
                    "message": "gemini bad request",
                    "type": "invalid_request_error",
                }
            },
        )
        self.assertIs(raised.exception.response, response)

    def test_gemini_stream_close_closes_upstream_response(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request(
                "POST",
                "https://gemini.example.com/v1beta/models/gemini-2.5-pro:streamGenerateContent",
            ),
            stream=httpx.ByteStream(
                b'data: {"candidates":[{"content":{"parts":[{"text":"hi"}]}}]}\n\n'
            ),
        )
        stream = _ResponseStream(response)

        with patch("litellm.httpx.stream", return_value=stream):
            iterator = litellm.completion(
                model="gemini/gemini-2.5-pro",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://gemini.example.com/v1beta",
                stream=True,
            )

        close = getattr(iterator, "close", None)
        self.assertTrue(callable(close))
        if callable(close):
            close()
        self.assertTrue(stream.closed)

    def test_anthropic_stream_accepts_openai_compatible_chunks(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://anthropic.example.com/v1/messages"),
            stream=httpx.ByteStream(
                b'data: {"choices":[{"index":0,"delta":{"content":"hello"},'
                b'"finish_reason":null}]}\n\n'
                b"data: [DONE]\n\n"
            ),
        )
        stream = _ResponseStream(response)

        with patch("litellm.httpx.stream", return_value=stream):
            iterator = litellm.completion(
                model="anthropic/glm-4.7-flash",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://anthropic.example.com",
                stream=True,
            )

        chunks = list(iterator)
        self.assertEqual(chunks[0]["choices"][0]["delta"]["role"], "assistant")
        self.assertEqual(chunks[1]["choices"][0]["delta"]["content"], "hello")
        self.assertEqual(chunks[-1], "[DONE]")
        self.assertTrue(stream.closed)

    def test_anthropic_stream_reads_content_block_start_text(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://anthropic.example.com/v1/messages"),
            stream=httpx.ByteStream(
                b'data: {"type":"content_block_start","content_block":'
                b'{"type":"text","text":"hello"}}\n\n'
                b'data: {"type":"message_stop"}\n\n'
            ),
        )
        stream = _ResponseStream(response)

        with patch("litellm.httpx.stream", return_value=stream):
            iterator = litellm.completion(
                model="anthropic/glm-4.7-flash",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://anthropic.example.com",
                stream=True,
            )

        chunks = list(iterator)
        self.assertEqual(chunks[0]["choices"][0]["delta"]["role"], "assistant")
        self.assertEqual(chunks[1]["choices"][0]["delta"]["content"], "hello")
        self.assertEqual(chunks[2]["choices"][0]["finish_reason"], "stop")
        self.assertTrue(stream.closed)

    def test_anthropic_stream_maps_thinking_delta_to_reasoning_content(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://anthropic.example.com/v1/messages"),
            stream=httpx.ByteStream(
                (
                    'data: {"type":"content_block_delta","delta":'
                    '{"type":"thinking_delta","thinking":"先想"}}\n\n'
                    'data: {"type":"content_block_delta","delta":'
                    '{"type":"text_delta","text":"答案"}}\n\n'
                    'data: {"type":"message_stop"}\n\n'
                ).encode()
            ),
        )
        stream = _ResponseStream(response)

        with patch("litellm.httpx.stream", return_value=stream):
            iterator = litellm.completion(
                model="anthropic/claude-3-7-sonnet-latest",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://anthropic.example.com",
                stream=True,
            )

        chunks = list(iterator)
        self.assertEqual(chunks[1]["choices"][0]["delta"]["reasoning_content"], "先想")
        self.assertEqual(chunks[2]["choices"][0]["delta"]["content"], "答案")
        self.assertEqual(chunks[3]["choices"][0]["finish_reason"], "stop")
        self.assertTrue(stream.closed)

    def test_anthropic_non_stream_maps_thinking_to_reasoning_content(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request("POST", "https://anthropic.example.com/v1/messages"),
            json={
                "id": "msg_123",
                "model": "claude-3-7-sonnet-latest",
                "stop_reason": "end_turn",
                "content": [
                    {"type": "thinking", "thinking": "先想"},
                    {"type": "text", "text": "答案"},
                ],
                "usage": {"input_tokens": 1, "output_tokens": 2},
            },
        )

        with patch("litellm.httpx.request", return_value=response):
            result = litellm.completion(
                model="anthropic/claude-3-7-sonnet-latest",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://anthropic.example.com",
            )

        message = result["choices"][0]["message"]
        self.assertEqual(message["reasoning_content"], "先想")
        self.assertEqual(message["content"], "答案")

    def test_gemini_stream_maps_thought_parts_to_reasoning_content(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request(
                "POST",
                "https://gemini.example.com/v1beta/models/gemini-2.5-pro:streamGenerateContent",
            ),
            stream=httpx.ByteStream(
                (
                    'data: {"candidates":[{"content":{"parts":['
                    '{"thought":true,"text":"先想"},'
                    '{"text":"答案"}]}}]}\n\n'
                ).encode()
            ),
        )
        stream = _ResponseStream(response)

        with patch("litellm.httpx.stream", return_value=stream):
            iterator = litellm.completion(
                model="gemini/gemini-2.5-pro",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://gemini.example.com/v1beta",
                stream=True,
            )

        chunks = list(iterator)
        self.assertEqual(chunks[1]["choices"][0]["delta"]["reasoning_content"], "先想")
        self.assertEqual(chunks[2]["choices"][0]["delta"]["content"], "答案")
        self.assertTrue(stream.closed)

    def test_gemini_non_stream_maps_thought_parts_to_reasoning_content(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request(
                "POST",
                "https://gemini.example.com/v1beta/models/gemini-2.5-pro:generateContent",
            ),
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"thought": True, "text": "先想"},
                                {"text": "答案"},
                            ]
                        }
                    }
                ]
            },
        )

        with patch("litellm.httpx.request", return_value=response):
            result = litellm.completion(
                model="gemini/gemini-2.5-pro",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://gemini.example.com/v1beta",
            )

        message = result["choices"][0]["message"]
        self.assertEqual(message["reasoning_content"], "先想")
        self.assertEqual(message["content"], "答案")

    def test_gemini_empty_prompt_feedback_block_reason_is_sanitized(self) -> None:
        payload = {
            "promptFeedback": {
                "blockReason": "",
                "blockReasonMessage": "",
            },
            "candidates": [
                {
                    "content": {
                        "role": "model",
                        "parts": [{"text": "OK"}],
                    },
                    "finishReason": "STOP",
                }
            ],
        }

        sanitized = _sanitize_empty_gemini_prompt_feedback(payload)

        self.assertNotIn("promptFeedback", sanitized)
        self.assertEqual(
            sanitized["candidates"][0]["content"]["parts"][0]["text"],
            "OK",
        )
        self.assertIn("promptFeedback", payload)

    def test_gemini_real_prompt_feedback_block_reason_is_preserved(self) -> None:
        payload = {
            "promptFeedback": {
                "blockReason": "SAFETY",
                "blockReasonMessage": "blocked",
            }
        }

        sanitized = _sanitize_empty_gemini_prompt_feedback(payload)

        self.assertEqual(
            sanitized["promptFeedback"],
            {
                "blockReason": "SAFETY",
                "blockReasonMessage": "blocked",
            },
        )

    def test_gemini_tools_drop_unsupported_json_schema_fields(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request(
                "POST",
                "https://gemini.example.com/v1beta/models/gemini-2.5-pro:generateContent",
            ),
            json={"candidates": [{"content": {"parts": [{"text": "ok"}]}}]},
        )
        tool_schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "payload": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"value": {"type": "string"}},
                }
            },
        }
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "submit",
                    "description": "Submit payload",
                    "parameters": tool_schema,
                },
            }
        ]

        with patch("litellm.httpx.request", return_value=response) as request_mock:
            result = litellm.completion(
                model="gemini/gemini-2.5-pro",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://gemini.example.com/v1beta",
                tools=tools,
            )

        self.assertEqual(result["choices"][0]["message"]["content"], "ok")
        request_body = request_mock.call_args.kwargs["json"]
        declaration = request_body["tools"][0]["functionDeclarations"][0]
        self.assertEqual(declaration["name"], "submit")
        self.assertNotIn("additionalProperties", declaration["parameters"])
        nested_payload = declaration["parameters"]["properties"]["payload"]
        self.assertNotIn("additionalProperties", nested_payload)
        self.assertIn("additionalProperties", tool_schema)
        self.assertIn("additionalProperties", tool_schema["properties"]["payload"])

    def test_gemini_sanitizes_all_function_declarations(self) -> None:
        response = httpx.Response(
            200,
            request=httpx.Request(
                "POST",
                "https://gemini.example.com/v1beta/models/gemini-2.5-pro:generateContent",
            ),
            json={"candidates": [{"content": {"parts": [{"text": "ok"}]}}]},
        )
        tools = [
            {
                "type": "function",
                "function": {
                    "name": f"tool_{index}",
                    "parameters": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "value": {
                                "type": "object",
                                "additionalProperties": False,
                            }
                        },
                    },
                },
            }
            for index in range(14)
        ]

        with patch("litellm.httpx.request", return_value=response) as request_mock:
            litellm.completion(
                model="gemini/gemini-2.5-pro",
                messages=[{"role": "user", "content": "hello"}],
                base_url="https://gemini.example.com/v1beta",
                tools=tools,
            )

        declarations = request_mock.call_args.kwargs["json"]["tools"][0][
            "functionDeclarations"
        ]
        self.assertEqual(len(declarations), 14)
        for declaration in declarations:
            parameters = declaration["parameters"]
            self.assertNotIn("additionalProperties", parameters)
            self.assertNotIn(
                "additionalProperties",
                parameters["properties"]["value"],
            )


if __name__ == "__main__":
    unittest.main()
