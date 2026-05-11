from __future__ import annotations

import unittest

from modules.runtime.proxy_trace_store import (
    MAX_EVENT_MESSAGE_BYTES,
    ProxyTraceBodyAccumulator,
    ProxyTraceStore,
    capture_proxy_trace_body,
)


class ProxyTraceStoreTests(unittest.TestCase):
    def test_body_capture_redacts_and_truncates_sensitive_values(self) -> None:
        capture = capture_proxy_trace_body(
            {
                "model": "mapped-model",
                "api_key": "secret-key",
                "messages": [{"role": "user", "content": "x" * 80}],
            },
            max_bytes=80,
        )

        self.assertTrue(capture["redacted"])
        self.assertTrue(capture["truncated"])
        self.assertIn("<redacted>", str(capture["value"]))
        self.assertNotIn("secret-key", str(capture["value"]))

    def test_clear_keeps_active_trace_and_removes_finished_trace(self) -> None:
        store = ProxyTraceStore(max_traces=10)
        active_trace_id = store.start_trace(
            request_id="active",
            method="POST",
            request_path="/v1/chat/completions",
        )
        finished_trace_id = store.start_trace(
            request_id="finished",
            method="POST",
            request_path="/v1/chat/completions",
        )
        store.finish_trace(finished_trace_id, status="completed", status_code=200)

        result = store.clear_traces()

        self.assertEqual(result["deleted_count"], 1)
        self.assertEqual(result["kept_active_count"], 1)
        self.assertIsNotNone(store.get_trace(active_trace_id))
        self.assertIsNone(store.get_trace(finished_trace_id))

    def test_stream_accumulator_marks_truncation_without_losing_total_bytes(self) -> None:
        accumulator = ProxyTraceBodyAccumulator(max_bytes=8)

        accumulator.append("12345")
        accumulator.append("67890")
        capture = accumulator.capture()

        self.assertEqual(capture["value"], "12345678")
        self.assertEqual(capture["bytes"], 10)
        self.assertTrue(capture["truncated"])
        self.assertEqual(capture["truncated_reason"], "stream_limit")

    def test_event_message_is_trimmed_to_size_limit(self) -> None:
        store = ProxyTraceStore(max_traces=10)
        trace_id = store.start_trace(
            request_id="request",
            method="POST",
            request_path="/v1/chat/completions",
        )

        store.add_event(trace_id, kind="log", message="x" * (MAX_EVENT_MESSAGE_BYTES + 64))
        trace = store.get_trace(trace_id)

        self.assertIsNotNone(trace)
        assert trace is not None
        event_message = trace["events"][0]["message"]
        self.assertEqual(len(event_message.encode("utf-8")), MAX_EVENT_MESSAGE_BYTES)

    def test_summary_exposes_route_event_markers(self) -> None:
        store = ProxyTraceStore(max_traces=10)
        trace_id = store.start_trace(
            request_id="request",
            method="POST",
            request_path="/v1/chat/completions",
        )

        store.add_event(
            trace_id,
            kind="route_attempt",
            data={"target_id": "target-a", "attempt_index": 1},
        )
        store.add_event(
            trace_id,
            kind="target_cooldown",
            data={"target_id": "target-a", "status_code": 429},
        )
        store.add_event(
            trace_id,
            kind="route_attempt",
            data={"target_id": "target-b", "attempt_index": 2, "source": "failover"},
        )

        summary = store.list_traces()[0]

        self.assertTrue(summary["has_route_attempts"])
        self.assertTrue(summary["has_cooldown"])
        self.assertTrue(summary["has_failover"])

    def test_summary_does_not_mark_plain_route_attempt_as_failover(self) -> None:
        store = ProxyTraceStore(max_traces=10)
        trace_id = store.start_trace(
            request_id="request",
            method="POST",
            request_path="/v1/chat/completions",
        )

        store.add_event(
            trace_id,
            kind="route_attempt",
            data={"target_id": "target-a", "attempt_index": 1},
        )

        summary = store.list_traces()[0]

        self.assertTrue(summary["has_route_attempts"])
        self.assertFalse(summary["has_cooldown"])
        self.assertFalse(summary["has_failover"])

    def test_summary_does_not_mark_cooldown_without_next_attempt_as_failover(self) -> None:
        store = ProxyTraceStore(max_traces=10)
        trace_id = store.start_trace(
            request_id="request",
            method="POST",
            request_path="/v1/chat/completions",
        )

        store.add_event(
            trace_id,
            kind="route_attempt",
            data={"target_id": "target-a", "attempt_index": 1},
        )
        store.add_event(
            trace_id,
            kind="target_cooldown",
            data={"target_id": "target-a", "status_code": 429},
        )

        summary = store.list_traces()[0]

        self.assertTrue(summary["has_route_attempts"])
        self.assertTrue(summary["has_cooldown"])
        self.assertFalse(summary["has_failover"])


if __name__ == "__main__":
    unittest.main()
