# pyright: reportAttributeAccessIssue=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
from __future__ import annotations

import argparse
import ctypes
import json
import sys
import time
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .hook_candidates import AI_AGENT_DLL
from .runtime_breakpoints import (
    DEFAULT_RVAS,
    ModuleInfo,
    ModuleSnapshotFailure,
    ProcessInfo,
    collect_ai_agent_modules,
    enable_debug_privilege,
)

PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_QUERY_INFORMATION = 0x0400
THREAD_GET_CONTEXT = 0x0008
THREAD_SET_CONTEXT = 0x0010
THREAD_QUERY_INFORMATION = 0x0040

CONTEXT_AMD64 = 0x00100000
CONTEXT_CONTROL = 0x00000001
CONTEXT_INTEGER = 0x00000002
CONTEXT_FLAGS = CONTEXT_AMD64 | CONTEXT_CONTROL | CONTEXT_INTEGER
CONTEXT_BUFFER_SIZE = 0x4D0
CONTEXT_FLAGS_OFFSET = 0x30
EFLAGS_OFFSET = 0x44
RIP_OFFSET = 0xF8
U64_SIZE = 8
RUST_STRING_SIZE = 24
TUNNEL_URL_BUILDER_STACK_SIZE = 0xB0
CALL_REL32_SIZE = 5
TRAP_FLAG = 0x100
REGISTER_OFFSETS = {
    "rax": 0x78,
    "rcx": 0x80,
    "rdx": 0x88,
    "rbx": 0x90,
    "rsp": 0x98,
    "rbp": 0xA0,
    "rsi": 0xA8,
    "rdi": 0xB0,
    "r8": 0xB8,
    "r9": 0xC0,
    "r10": 0xC8,
    "r11": 0xD0,
    "r12": 0xD8,
    "r13": 0xE0,
    "r14": 0xE8,
    "r15": 0xF0,
    "rip": RIP_OFFSET,
}

EXCEPTION_DEBUG_EVENT = 1
EXIT_PROCESS_DEBUG_EVENT = 5
EXCEPTION_BREAKPOINT = 0x80000003
EXCEPTION_SINGLE_STEP = 0x80000004
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
MIN_USER_POINTER = 0x10000
MAX_CANDIDATE_TEXT_LEN = 512
MAX_STRUCT_SCAN_SIZE = 0x100
MAX_STRING_CANDIDATES_PER_BASE = 8
MIN_TEXT_STRUCT_BYTES = 16
ASCII_PRINTABLE_MIN = 32
ASCII_PRINTABLE_MAX = 126
TEXT_PRINTABLE_RATIO_MIN = 0.85
TEXT_WHITESPACE_BYTES = (9, 10, 13)
MIN_QWORD_PAIR_LEN = 2
MIN_WAKER_SLOT_QWORDS = 3
INTERESTING_SSE_TEXT_MARKERS = (
    "http",
    "authorization",
    "bearer",
    "api",
    "openai",
    "modelscope",
    "localhost",
    "127.0.0.1",
    "/v1",
    "content-type",
    "server",
    "request",
    "header",
    "x-",
)
INTERESTING_ROUTE_TEXT_MARKERS = (
    "127.0.0.1",
    "api",
    "event",
    "header",
    "http",
    "openai",
    "request",
    "response",
    "rpc",
    "sse",
    "status",
    "task",
    "trace",
    "tunnel",
    "delta",
    "message",
    "content",
    "tool_call",
    "chat.",
    "completion",
    "custom",
    "model",
    "json",
    "error",
)
INTERESTING_FAILURE_TEXT_MARKERS = (
    "error",
    "failed",
    "status",
    "unauthorized",
    "unknown",
    "event",
    "progress",
    "notice",
    "sse.open",
    "opened",
    "rpc.close",
    "http",
    "json",
    "message",
    "delta",
)
REGISTER_SCAN_ORDER = (
    "rax",
    "rbx",
    "rcx",
    "rdx",
    "r8",
    "r9",
    "r12",
    "r13",
    "r14",
    "r15",
    "rsp",
    "rbp",
    "rsi",
    "rdi",
)
MODEL_DETAIL_TARGETS = {
    "current_config_info_parse",
    "detail_param_response_parse",
    "detail_param_response_data_parse",
    "config_info_list_item_parse",
    "model_config_info_parse",
}
MODEL_DETAIL_STACK_SCAN_OFFSETS = (0x30, 0x58, 0x68, 0x78, 0xB8)
MODEL_INFO_LOG_TARGETS = {
    "chat_handler_model_info_log_1",
    "chat_handler_model_info_log_2",
}
MODEL_INFO_RBP_SCAN_OFFSETS = (0xAE0, 0x1110, 0x1280, 0x1F88, 0x2030, 0x2280, 0x2450)
MODEL_INFO_POINTER_SCAN_REGISTERS = (
    "rax",
    "rbx",
    "rdx",
    "rsp",
    "rbp",
    "rsi",
    "rdi",
    "r12",
    "r14",
)
MODEL_INFO_INTERESTING_TEXT_MARKERS = (
    "127.0.0.1",
    "api.openai.com",
    "authorization",
    "base_url",
    "bearer",
    "custom",
    "gpt",
    "http://",
    "https://",
    "modelscope",
    "openai",
    "/v1",
)
MAX_USER_POINTER = 0x00007FFFFFFFFFFF
MODEL_INFO_POINTER_SCAN_SIZE = 0x500
MODEL_INFO_POINTER_SCAN_MAX_DEPTH = 3
MODEL_INFO_POINTER_SCAN_MAX_NODES = 480
MODEL_INFO_POINTER_SCAN_MAX_RESULTS = 80
CUSTOM_MODEL_DEBUG_FMT_TARGETS = {
    "custom_model_debug_fmt",
}
CUSTOM_MODEL_WRITE_TARGETS = {
    "custom_model_write_begin",
    "custom_model_write_ak_base_url",
    "custom_model_write_after_base_url",
}
CUSTOM_MODEL_PARAM_EXTRACT_TARGETS = {
    "custom_model_field_base_url_call",
    "custom_model_field_api_key_call",
}
CUSTOM_MODEL_TIMING_TARGETS = {
    "get_custom_model_timing_label",
}
CUSTOM_MODEL_COPY_TARGETS = {
    "get_custom_model_copy_step",
    "get_custom_model_copy_fields_ready",
}
CUSTOM_MODEL_CALLSITE_TARGETS = {
    "custom_model_stage_2_callsite",
    "custom_model_stage_3_callsite",
    "custom_model_stage_5_callsite",
    "custom_model_stage_23_callsite",
}
SSE_OPEN_TARGETS = {
    "sse_open_dispatch_branch_1",
    "sse_open_dispatch_branch_2",
    "sse_open_parsed_state_ready",
    "sse_open_branch2_iter_start",
    "sse_open_branch2_item_parse_call",
    "sse_open_branch2_item_parse_after",
    "sse_open_branch2_payload_decode_call",
    "sse_open_branch2_payload_decode_after",
    "sse_open_branch2_http_build_call",
    "sse_open_branch2_http_build_after",
    "sse_open_error_context_1",
    "sse_open_error_context_2",
}
OPENAI_POST_PARSE_TARGETS = {
    "post_json_parse_result_1",
    "post_json_parse_result_2",
    "post_json_parse_result_3",
    "parser_rva_0x286bf6e",
    "parser_rva_0x286bf75",
    "parser_rva_0x286bf7e",
}
CURRENT_ROUTE_TARGETS = {
    "current_route_event_build_call",
    "current_route_queue_push_call_0",
    "current_route_queue_push_call_1",
    "current_route_queue_push_call_2",
    "current_route_queue_push_call_3",
}
QUEUE_WAKER_TARGETS = {
    "queue_wake_notify",
}
QUEUE_RECEIVER_TARGETS = {
    "queue_receiver_poll_candidate",
    "queue_receiver_xref_0",
    "queue_receiver_xref_1",
}
FAILURE_ROUTE_TARGETS = {
    "failure_sse_open_error_1",
    "failure_sse_open_error_2",
    "failure_unknown_event_1",
    "failure_unknown_event_2",
    "failure_unknown_event_3",
}
CUSTOM_MODEL_PROXY_RUNTIME_TARGETS = {
    "custom_model_get_pending_failed",
}
CUSTOM_MODEL_PROXY_RUNTIME_RBP_SCAN_OFFSETS = (
    0x6C0,
    0x800,
    0x808,
    0x810,
    0x818,
    0x820,
    0x828,
    0x840,
    0x848,
    0x850,
    0x886,
    0x888,
    0x8A0,
    0x8A8,
    0x8B0,
)
CURRENT_ROUTE_TEXT_OFFSETS = (
    0x308,
    0x6C0,
    0x880,
    0x8B0,
    0x980,
    0xA38,
    0xB30,
)
CURRENT_ROUTE_STRUCT_SPECS = (
    (0x308, 0x90),
    (0x6C0, 0x90),
    (0x880, 0x30),
    (0x8B0, 0x48),
    (0x980, 0x58),
    (0xA38, 0x30),
    (0xB30, 0x48),
)
FAILURE_SSE_OPEN_BASE_OFFSETS = (
    0x1C0,
    0x260,
    0x2B0,
    0x300,
    0x6F0,
    0x980,
    0xC08,
)
FAILURE_SSE_OPEN_STRUCT_SPECS = (
    (0x1C0, 0x18),
    (0x260, 0x30),
    (0x2B0, 0x30),
    (0x300, 0x48),
    (0x6F0, 0x30),
    (0x980, 0x30),
    (0xC08, 0x30),
)
FAILURE_UNKNOWN_EVENT_BASE_OFFSETS = (
    -0x50,
    0xC8,
    0x158,
    0x1E0,
    0x290,
    0x450,
    0x670,
    0x9F0,
    0xC30,
    0xE90,
)
FAILURE_UNKNOWN_EVENT_STRUCT_SPECS = (
    (-0x50, 0x30),
    (0xC8, 0x30),
    (0x158, 0x30),
    (0x1E0, 0x30),
    (0x290, 0x48),
    (0x450, 0x30),
    (0x670, 0x30),
    (0x9F0, 0x48),
    (0xC30, 0x30),
    (0xE90, 0x30),
)
FAILURE_POINTER_SCAN_REGISTERS = REGISTER_SCAN_ORDER
FAILURE_INTERESTING_TEXT_MARKERS = (
    "api.openai.com",
    "custom model internal",
    "http status",
    "incorrect api",
    "invalid_api_key",
    "model_config",
    "progress_notice",
    "sse.open",
    "unknown event",
)
CUSTOM_MODEL_WRITE_RBP_SCAN_OFFSETS = (
    0x16C0,
    0x16D8,
    0x16F0,
    0x1708,
    0x1720,
    0x1830,
    0x2030,
    0x2430,
    0x2440,
    0x2450,
)
CUSTOM_MODEL_PARAM_RBP_SCAN_OFFSETS = (
    0x388,
    0x390,
    0x398,
    0x440,
    0x450,
    0x460,
    0x468,
    0x470,
    0x480,
    0x488,
    0x490,
    0x498,
    0x4A0,
    0x4A8,
    0x4B0,
    0x4B8,
    0x4C8,
    0x4D0,
    0x4D8,
    0x4E0,
    0x4F0,
    0x500,
    0x510,
)
SSE_OPEN_RBP_SCAN_OFFSETS = (
    0x320,
    0x3E0,
    0x460,
    0x468,
    0x470,
    0x480,
    0x4A0,
    0x4C0,
    0x4E0,
    0x500,
    0x520,
    0x540,
    0x560,
    0x580,
    0x5A0,
    0x5C0,
    0x5E0,
    0x600,
    0x620,
    0x640,
    0x650,
    0x660,
    0x680,
    0x790,
    0x7F0,
    0x8F0,
    0x900,
    0x920,
    0x928,
    0x930,
    0x938,
    0x948,
    0x980,
)
OPENAI_POST_PARSE_QWORD_OFFSETS = (
    0x138,
    0x140,
    0x148,
    0x150,
    0x158,
    0x160,
    0x168,
    0x880,
    0x8B0,
    0xBA8,
    0xBB8,
)
OPENAI_POST_PARSE_TEXT_OFFSETS = (
    0x138,
    0x140,
    0x148,
    0x150,
    0x158,
)
BREAKPOINT_PROFILES: dict[str, tuple[tuple[str, int], ...]] = {
    "llm_unknown_event_candidates": (
        ("unknown_event_1", 0x1F04E9E),
        ("unknown_event_2", 0x1F053AA),
        ("unknown_event_3", 0x23CB1CF),
    ),
    "sse_path_candidates": (
        ("aha_stream_1", 0xD5EC97),
        ("aha_stream_2", 0xD86796),
        ("aha_stream_3", 0xD99AE7),
        ("aha_stream_4", 0xDA1BA6),
        ("aha_stream_5", 0xDCDF96),
        ("aha_stream_6", 0xDD5BE9),
        ("aha_stream_7", 0xE6BEE0),
        ("aha_stream_8", 0xE73997),
        ("simulate_sse_no_event_1", 0xCF9B5A),
        ("simulate_sse_no_event_2", 0xD68351),
        ("simulate_sse_no_event_3", 0xD7A213),
        ("simulate_sse_no_event_4", 0xD8E66D),
        ("simulate_sse_no_event_5", 0xDAD057),
        ("simulate_sse_no_event_6", 0xDB882C),
        ("simulate_sse_no_event_7", 0xDE2EC6),
        ("simulate_sse_no_event_8", 0xDF01F0),
        ("simulate_sse_no_event_9", 0xDFD6F0),
        ("simulate_sse_no_event_10", 0x248E6BF),
    ),
    "openai_chat_completion_sse_candidates": (
        ("chat_completion_chunk_builder", 0x289DE2A),
        ("done_marker_match_1", 0x286BF17),
        ("done_marker_match_2", 0x28C81FE),
        ("done_marker_match_3", 0x28CAA89),
        ("done_marker_match_4", 0x2A96D9E),
        ("done_marker_match_5", 0x2A9F070),
        ("done_marker_match_6", 0x2AAFBFA),
    ),
    "openai_post_parse_candidates": (
        ("post_json_parse_result_1", 0x286BF6E),
        ("post_json_parse_result_2", 0x286BF75),
        ("post_json_parse_result_3", 0x286BF7E),
    ),
    "current_route_queue_push_candidates": (
        ("current_route_event_build_call", 0x286C4AE),
        ("current_route_queue_push_call_0", 0x286C57C),
        ("current_route_queue_push_call_1", 0x286CD18),
        ("current_route_queue_push_call_2", 0x286DCC6),
        ("current_route_queue_push_call_3", 0x286DFE2),
    ),
    "current_route_queue_consumer_candidates": (
        ("queue_wake_notify", 0x3069EFC),
        ("queue_receiver_poll_candidate", 0x289A089),
        ("queue_receiver_xref_0", 0x285C254),
        ("queue_receiver_xref_1", 0x285C513),
    ),
    "event_dispatcher_candidates": (
        ("event_dispatcher_entry", 0x2AC53CD),
        ("event_dispatcher_content_block_delta", 0x2AC5408),
        ("event_dispatcher_message_delta", 0x2AC5A21),
    ),
    "wakeup_callback_registration_candidates": (
        ("wakeup_callback_register_call_0", 0x306D398),
        ("wakeup_callback_register_call_1", 0x306DC74),
    ),
    "current_route_failure_candidates": (
        ("failure_sse_open_error_1", 0xA6CA8C),
        ("failure_sse_open_error_2", 0xA6CBC5),
        ("failure_unknown_event_1", 0x1F04E9E),
        ("failure_unknown_event_2", 0x1F053AA),
        ("failure_unknown_event_3", 0x23CB1CF),
    ),
    "failure_sse_open_error_only_candidates": (
        ("failure_sse_open_error_1", 0xA6CA8C),
        ("failure_sse_open_error_2", 0xA6CBC5),
    ),
    "llm_model_config_candidates": (
        ("model_config_match", 0x1B77632),
        ("event_name_dispatch", 0x24EA0C3),
    ),
    "model_detail_sync_candidates": (
        ("current_config_info_parse", 0x1A21137),
        ("detail_param_response_parse", 0x1A21444),
        ("detail_param_response_data_parse", 0x1A2153A),
        ("config_info_list_item_parse", 0x1A215DB),
        ("model_config_info_parse", 0x1A21663),
    ),
    "model_info_log_candidates": (
        ("chat_handler_model_info_log_1", 0xE4CA02),
        ("chat_handler_model_info_log_2", 0xE4CB36),
    ),
    "custom_model_debug_fmt_candidates": (
        ("custom_model_debug_fmt", 0xE65F54),
    ),
    "custom_model_write_candidates": (
        ("custom_model_write_begin", 0xE4C4DF),
        ("custom_model_write_ak_base_url", 0xE4C54F),
        ("custom_model_write_after_base_url", 0xE4C589),
    ),
    "custom_model_write_ak_base_url_only": (
        ("custom_model_write_ak_base_url", 0xE4C54F),
    ),
    "custom_model_write_after_base_url_only": (
        ("custom_model_write_after_base_url", 0xE4C589),
    ),
    "custom_model_param_extract_candidates": (
        ("custom_model_field_base_url_call", 0xB6994D),
        ("custom_model_field_api_key_call", 0xB69A55),
    ),
    "custom_model_timing_candidates": (
        ("get_custom_model_timing_label", 0x1F7C662),
    ),
    "custom_model_copy_candidates": (
        ("get_custom_model_copy_step", 0xD4AC85),
    ),
    "custom_model_copy_ready_candidates": (
        ("get_custom_model_copy_fields_ready", 0xD4ACC5),
    ),
    "custom_model_callsite_candidates": (
        ("custom_model_stage_2_callsite", 0xD4A533),
        ("custom_model_stage_3_callsite", 0xD4A75C),
        ("custom_model_stage_5_callsite", 0xD4AC80),
        ("custom_model_stage_23_callsite", 0xD4BE51),
    ),
    "sse_open_message_handler_candidates": (
        ("sse_open_dispatch_branch_1", 0xA4B7CC),
        ("sse_open_dispatch_branch_2", 0xA66B17),
        ("sse_open_parsed_state_ready", 0xA66B6B),
        ("sse_open_error_context_1", 0xA6CA8C),
        ("sse_open_error_context_2", 0xA6CBC5),
    ),
    "sse_open_branch2_flow_candidates": (
        ("sse_open_branch2_iter_start", 0xA66DCC),
        ("sse_open_branch2_item_parse_call", 0xA66F34),
        ("sse_open_branch2_item_parse_after", 0xA66F58),
        ("sse_open_branch2_payload_decode_call", 0xA67024),
        ("sse_open_branch2_payload_decode_after", 0xA67041),
        ("sse_open_branch2_http_build_call", 0xA67241),
        ("sse_open_branch2_http_build_after", 0xA67246),
    ),
    "sse_open_post_match_candidates": (
        ("sse_open_parsed_state_ready", 0xA66B6B),
        ("sse_open_error_context_1", 0xA6CA8C),
        ("sse_open_error_context_2", 0xA6CBC5),
    ),
    "custom_model_proxy_runtime_candidates": (
        ("custom_model_get_pending_failed", 0xA4B022),
        ("sse_open_dispatch_branch_1", 0xA4B7CC),
        ("sse_open_dispatch_branch_2", 0xA66B17),
        ("sse_open_parsed_state_ready", 0xA66B6B),
        ("sse_open_error_context_1", 0xA6CA8C),
        ("sse_open_error_context_2", 0xA6CBC5),
    ),
    "default_handler_tracing_metadata_candidates": (
        ("default_handler_metadata_xref_0", 0x5AA469),
        ("default_handler_metadata_xref_1", 0x1CA5AE0),
        ("default_handler_metadata_xref_2", 0x1D2C2C0),
        ("default_handler_metadata_xref_3", 0x1FBD2BE),
        ("default_handler_metadata_xref_4", 0x2579ED8),
        ("default_handler_metadata_xref_5", 0x2D90FCC),
        ("default_handler_metadata_xref_6", 0x2F3348E),
    ),
    "custom_model_chat_path_candidates": (
        ("custom_model_write_begin", 0xE4C4DF),
        ("custom_model_write_ak_base_url", 0xE4C54F),
        ("custom_model_write_after_base_url", 0xE4C589),
        ("chat_handler_model_info_log_1", 0xE4CA02),
        ("chat_handler_model_info_log_2", 0xE4CB36),
        ("custom_model_debug_fmt", 0xE65F54),
    ),
}


class EXCEPTION_RECORD64(ctypes.Structure):
    _fields_ = [
        ("ExceptionCode", wintypes.DWORD),
        ("ExceptionFlags", wintypes.DWORD),
        ("ExceptionRecord", ctypes.c_uint64),
        ("ExceptionAddress", ctypes.c_uint64),
        ("NumberParameters", wintypes.DWORD),
        ("__unusedAlignment", wintypes.DWORD),
        ("ExceptionInformation", ctypes.c_uint64 * 15),
    ]


class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD64),
        ("dwFirstChance", wintypes.DWORD),
    ]


class DEBUG_EVENT_UNION(ctypes.Union):
    _fields_ = [
        ("Exception", EXCEPTION_DEBUG_INFO),
        ("raw", ctypes.c_ubyte * 1024),
    ]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [
        ("dwDebugEventCode", wintypes.DWORD),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
        ("u", DEBUG_EVENT_UNION),
    ]


kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
DebugActiveProcess = kernel32.DebugActiveProcess
DebugActiveProcess.argtypes = [wintypes.DWORD]
DebugActiveProcess.restype = wintypes.BOOL
DebugActiveProcessStop = kernel32.DebugActiveProcessStop
DebugActiveProcessStop.argtypes = [wintypes.DWORD]
DebugActiveProcessStop.restype = wintypes.BOOL
WaitForDebugEvent = kernel32.WaitForDebugEvent
WaitForDebugEvent.argtypes = [ctypes.POINTER(DEBUG_EVENT), wintypes.DWORD]
WaitForDebugEvent.restype = wintypes.BOOL
ContinueDebugEvent = kernel32.ContinueDebugEvent
ContinueDebugEvent.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]
ContinueDebugEvent.restype = wintypes.BOOL
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE
OpenThread = kernel32.OpenThread
OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenThread.restype = wintypes.HANDLE
ReadProcessMemory = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]
ReadProcessMemory.restype = wintypes.BOOL
WriteProcessMemory = kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]
WriteProcessMemory.restype = wintypes.BOOL
FlushInstructionCache = kernel32.FlushInstructionCache
FlushInstructionCache.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_size_t]
FlushInstructionCache.restype = wintypes.BOOL
GetThreadContext = kernel32.GetThreadContext
GetThreadContext.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
GetThreadContext.restype = wintypes.BOOL
SetThreadContext = kernel32.SetThreadContext
SetThreadContext.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
SetThreadContext.restype = wintypes.BOOL
CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL


@dataclass(frozen=True)
class ProbeRequest:
    target: str | None = None
    profile: str | None = None
    timeout_seconds: int = 120
    wait_for_module_seconds: int = 0
    module_base: int | None = None
    address: int | None = None
    rva: int | None = None


@dataclass(frozen=True)
class BreakpointContext:
    address: int
    original: bytes
    target_label: str
    module_base: int
    module_size: int


@dataclass(frozen=True)
class BreakpointSite:
    label: str
    address: int
    original: bytes


def _last_error(action: str) -> OSError:
    code = ctypes.get_last_error()
    return OSError(code, f"{action}: WinError {code}")


def _close(handle: wintypes.HANDLE) -> None:
    if handle:
        CloseHandle(handle)


def _read_memory(handle: wintypes.HANDLE, address: int, size: int) -> bytes:
    buffer = ctypes.create_string_buffer(size)
    read = ctypes.c_size_t()
    ok = ReadProcessMemory(
        handle,
        ctypes.c_void_p(address),
        buffer,
        size,
        ctypes.byref(read),
    )
    if not ok:
        return b""
    return buffer.raw[: read.value]


def _write_memory(handle: wintypes.HANDLE, address: int, data: bytes) -> None:
    buffer = ctypes.create_string_buffer(data)
    written = ctypes.c_size_t()
    ok = WriteProcessMemory(
        handle,
        ctypes.c_void_p(address),
        buffer,
        len(data),
        ctypes.byref(written),
    )
    if not ok or written.value != len(data):
        raise _last_error(f"WriteProcessMemory({hex(address)})")
    FlushInstructionCache(handle, ctypes.c_void_p(address), len(data))


def _read_context(thread: wintypes.HANDLE) -> bytearray:
    buffer = bytearray(CONTEXT_BUFFER_SIZE)
    buffer[CONTEXT_FLAGS_OFFSET : CONTEXT_FLAGS_OFFSET + 4] = CONTEXT_FLAGS.to_bytes(4, "little")
    raw = (ctypes.c_char * len(buffer)).from_buffer(buffer)
    if not GetThreadContext(thread, raw):
        raise _last_error("GetThreadContext")
    return buffer


def _write_context(thread: wintypes.HANDLE, buffer: bytearray) -> None:
    raw = (ctypes.c_char * len(buffer)).from_buffer(buffer)
    if not SetThreadContext(thread, raw):
        raise _last_error("SetThreadContext")


def _u64(buffer: bytearray, offset: int) -> int:
    return int.from_bytes(buffer[offset : offset + 8], "little")


def _put_u64(buffer: bytearray, offset: int, value: int) -> None:
    buffer[offset : offset + 8] = value.to_bytes(8, "little")


def _preview(data: bytes) -> dict[str, str]:
    utf8 = data.split(b"\x00", 1)[0].decode("utf-8", errors="ignore")
    utf16 = data.decode("utf-16le", errors="ignore").split("\x00", 1)[0]
    return {
        "hex": data[:64].hex(" "),
        "utf8": "".join(char for char in utf8 if char.isprintable())[:120],
        "utf16le": "".join(char for char in utf16 if char.isprintable())[:120],
    }


def _clean_text(value: str, limit: int = 240) -> str:
    return "".join(char for char in value if char.isprintable())[:limit]


def _is_probably_text(data: bytes) -> bool:
    if not data:
        return False
    if b"\x00" in data:
        return False
    printable = sum(
        1
        for byte in data
        if ASCII_PRINTABLE_MIN <= byte <= ASCII_PRINTABLE_MAX or byte in TEXT_WHITESPACE_BYTES
    )
    return printable / len(data) >= TEXT_PRINTABLE_RATIO_MIN


def _read_text_bytes(
    handle: wintypes.HANDLE,
    ptr: int,
    length: int,
    max_len: int = MAX_CANDIDATE_TEXT_LEN,
) -> bytes:
    if ptr <= MIN_USER_POINTER or length <= 0 or length > max_len:
        return b""
    data = _read_memory(handle, ptr, length)
    if len(data) != length or not _is_probably_text(data):
        return b""
    return data


def _format_snapshot_diagnostic(
    process_count: int,
    failures: list[ModuleSnapshotFailure],
    privilege: dict[str, Any],
) -> str:
    error_codes = sorted(
        {
            failure.error_code
            for failure in failures
            if getattr(failure, "error_code", None) is not None
        }
    )
    return (
        f"trae_process_count={process_count}, "
        f"debug_privilege={privilege}, "
        f"module_snapshot_error_codes={error_codes}, "
        f"module_snapshot_failure_count={len(failures)}"
    )


def _collect_matching_modules(
    pid: int | None,
    module_path: Path,
) -> tuple[list[ModuleInfo], list[ProcessInfo], list[ModuleSnapshotFailure], dict[str, Any]]:
    modules, processes, failures, privilege = collect_ai_agent_modules(module_path)
    if pid is not None:
        modules = [module for module in modules if module.pid == pid]
    return modules, processes, failures, privilege


def _wait_for_runtime_module(
    pid: int | None,
    module_path: Path,
    wait_seconds: int = 0,
) -> tuple[ModuleInfo, list[ProcessInfo], list[ModuleSnapshotFailure], dict[str, Any]]:
    started = time.monotonic()
    while True:
        modules, processes, failures, privilege = _collect_matching_modules(pid, module_path)
        if modules:
            return modules[0], processes, failures, privilege
        if wait_seconds <= 0 or time.monotonic() - started >= wait_seconds:
            diagnostic = _format_snapshot_diagnostic(len(processes), failures, privilege)
            raise RuntimeError(f"未找到已加载 ai_agent.dll 的 Trae 进程；{diagnostic}")
        time.sleep(0.5)


def _select_target(
    pid: int | None,
    module_path: Path,
    target: str,
    module_base: int | None,
    wait_for_module_seconds: int = 0,
) -> tuple[int, int]:
    if target not in DEFAULT_RVAS:
        raise ValueError(f"未知 target: {target}")
    if pid is not None and module_base is not None:
        return pid, module_base + DEFAULT_RVAS[target]

    module, _, _, _ = _wait_for_runtime_module(
        pid,
        module_path,
        wait_seconds=wait_for_module_seconds,
    )
    return module.pid, module.base_address + DEFAULT_RVAS[target]


def _resolve_runtime_module(
    pid: int | None,
    module_path: Path,
    wait_for_module_seconds: int = 0,
) -> tuple[int, int, int]:
    module, _, _, _ = _wait_for_runtime_module(
        pid,
        module_path,
        wait_seconds=wait_for_module_seconds,
    )
    return module.pid, module.base_address, module.size


def _select_custom_breakpoint(  # noqa: PLR0913
    pid: int | None,
    module_path: Path,
    module_base: int | None,
    address: int | None,
    rva: int | None,
    wait_for_module_seconds: int = 0,
) -> tuple[int, int, str]:
    if address is not None and rva is not None:
        raise ValueError("--address 与 --rva 只能二选一")
    if address is None and rva is None:
        raise ValueError("必须提供 --target 或 --address / --rva")

    if address is not None:
        if pid is None:
            raise ValueError("--address 模式必须同时提供 --pid")
        return pid, address, "custom_address"

    if rva is None:
        raise ValueError("必须提供 --rva")

    if pid is not None and module_base is not None:
        return pid, module_base + rva, "custom_rva"

    module, _, _, _ = _wait_for_runtime_module(
        pid,
        module_path,
        wait_seconds=wait_for_module_seconds,
    )
    return module.pid, module.base_address + rva, "custom_rva"


def _resolve_probe_breakpoint(
    pid: int | None,
    module_path: Path,
    request: ProbeRequest,
) -> tuple[int, int, str]:
    if request.address is not None or request.rva is not None:
        return _select_custom_breakpoint(
            pid,
            module_path,
            request.module_base,
            request.address,
            request.rva,
            request.wait_for_module_seconds,
        )

    resolved_target = request.target or "update_boot_config_log_anchor"
    target_pid, address = _select_target(
        pid,
        module_path,
        resolved_target,
        request.module_base,
        request.wait_for_module_seconds,
    )
    return target_pid, address, resolved_target


def _resolve_profile_breakpoints(
    pid: int | None,
    module_path: Path,
    request: ProbeRequest,
) -> tuple[int, list[tuple[str, int]]]:
    if request.profile not in BREAKPOINT_PROFILES:
        raise ValueError(f"未知 profile: {request.profile}")
    if request.module_base is not None and pid is None:
        raise ValueError("--module-base 需要与 --pid 一起使用")

    if pid is not None and request.module_base is not None:
        target_pid = pid
        module_base = request.module_base
    else:
        target_pid, module_base, _ = _resolve_runtime_module(
            pid,
            module_path,
            wait_for_module_seconds=request.wait_for_module_seconds,
        )

    resolved_sites = [
        (label, module_base + rva)
        for label, rva in BREAKPOINT_PROFILES[request.profile]
    ]
    return target_pid, resolved_sites


def _resolve_probe_sites(
    pid: int | None,
    module_path: Path,
    request: ProbeRequest,
) -> tuple[int, list[tuple[str, int]]]:
    if request.profile is not None:
        if request.target is not None or request.address is not None or request.rva is not None:
            raise ValueError("--profile 与 --target/--address/--rva 不能混用")
        return _resolve_profile_breakpoints(pid, module_path, request)

    target_pid, address, target_label = _resolve_probe_breakpoint(
        pid,
        module_path,
        request,
    )
    return target_pid, [(target_label, address)]


def _resolve_module_context(pid: int, module_path: Path) -> tuple[int, int]:
    _, module_base, module_size = _resolve_runtime_module(pid, module_path)
    return module_base, module_size


def _open_process(pid: int) -> wintypes.HANDLE:
    access = PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION
    handle = OpenProcess(access, False, pid)
    if not handle:
        raise _last_error(f"OpenProcess({pid})")
    return handle


def _open_thread(thread_id: int) -> wintypes.HANDLE:
    access = THREAD_GET_CONTEXT | THREAD_SET_CONTEXT
    handle = OpenThread(access, False, thread_id)
    if not handle:
        raise _last_error(f"OpenThread({thread_id})")
    return handle


def _registers(context: bytearray) -> dict[str, str]:
    return {
        name: hex(_u64(context, offset))
        for name, offset in REGISTER_OFFSETS.items()
    }


def _pointer_previews(handle: wintypes.HANDLE, registers: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in REGISTER_SCAN_ORDER:
        address = int(registers[name], 16)
        if address > MIN_USER_POINTER:
            result[name] = _preview(_read_memory(handle, address, 256))
    return result


def _scan_string_candidates(
    handle: wintypes.HANDLE,
    base_address: int,
    scan_size: int = MAX_STRUCT_SCAN_SIZE,
    limit: int = MAX_STRING_CANDIDATES_PER_BASE,
) -> list[dict[str, Any]]:
    if base_address <= MIN_USER_POINTER:
        return []

    data = _read_memory(handle, base_address, scan_size)
    if len(data) < MIN_TEXT_STRUCT_BYTES:
        return []

    results: list[dict[str, Any]] = []
    seen: set[tuple[int, int, int]] = set()

    for offset in range(0, len(data) - 16 + 1, 8):
        ptr = int.from_bytes(data[offset : offset + 8], "little")
        length = int.from_bytes(data[offset + 8 : offset + 16], "little")
        if ptr <= MIN_USER_POINTER or length <= 0 or length > MAX_CANDIDATE_TEXT_LEN:
            continue

        text_bytes = _read_text_bytes(handle, ptr, length)
        if not text_bytes:
            continue

        key = (ptr, length, offset)
        if key in seen:
            continue
        seen.add(key)

        item: dict[str, Any] = {
            "base_address": hex(base_address),
            "field_offset": hex(offset),
            "ptr": hex(ptr),
            "len": length,
            "utf8": _clean_text(text_bytes.decode("utf-8", errors="replace")),
            "hex": text_bytes[:96].hex(" "),
            "kind": "&str_like",
        }

        if offset + 24 <= len(data):
            capacity = int.from_bytes(data[offset + 16 : offset + 24], "little")
            if length <= capacity <= MAX_CANDIDATE_TEXT_LEN:
                item["kind"] = "String_like"
                item["cap"] = capacity

        results.append(item)
        if len(results) >= limit:
            break

    return results


def _collect_register_string_candidates(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for name in REGISTER_SCAN_ORDER:
        address = int(registers[name], 16)
        candidates = _scan_string_candidates(handle, address)
        if candidates:
            result[name] = candidates
    return result


def _read_stack_qwords(
    handle: wintypes.HANDLE,
    stack_pointer: int,
    module_base: int,
    module_size: int,
    count: int = 64,
) -> list[dict[str, Any]]:
    data = _read_memory(handle, stack_pointer, count * 8)
    result: list[dict[str, Any]] = []
    for index in range(0, len(data), 8):
        if index + 8 > len(data):
            break
        value = int.from_bytes(data[index : index + 8], "little")
        item: dict[str, Any] = {
            "slot": index // 8,
            "address": hex(stack_pointer + index),
            "value": hex(value),
        }
        if module_base <= value < module_base + module_size:
            item["in_ai_agent"] = True
            item["ai_agent_rva"] = hex(value - module_base)
        result.append(item)
    return result


def _extract_ai_agent_stack_frames(
    stack_qwords: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "slot": item["slot"],
            "address": item["address"],
            "value": item["value"],
            "ai_agent_rva": item["ai_agent_rva"],
        }
        for item in stack_qwords
        if item.get("in_ai_agent")
    ]


def _summarize_stack_frames(
    frames: list[dict[str, Any]],
    limit: int = 16,
) -> list[str]:
    return [str(frame["ai_agent_rva"]) for frame in frames[:limit]]


def _read_u64_from_process(handle: wintypes.HANDLE, address: int) -> int | None:
    data = _read_memory(handle, address, U64_SIZE)
    if len(data) != U64_SIZE:
        return None
    return int.from_bytes(data, "little")


def _read_rust_string(
    handle: wintypes.HANDLE,
    struct_address: int,
    max_len: int = 4096,
) -> dict[str, Any] | None:
    data = _read_memory(handle, struct_address, RUST_STRING_SIZE)
    if len(data) != RUST_STRING_SIZE:
        return None

    ptr = int.from_bytes(data[0:8], "little")
    length = int.from_bytes(data[8:16], "little")
    capacity = int.from_bytes(data[16:24], "little")
    if ptr <= MIN_USER_POINTER or length > max_len or capacity > max_len or length > capacity:
        return {
            "struct_address": hex(struct_address),
            "ptr": hex(ptr),
            "len": length,
            "cap": capacity,
            "valid": False,
        }

    content = _read_memory(handle, ptr, length)
    return {
        "struct_address": hex(struct_address),
        "ptr": hex(ptr),
        "len": length,
        "cap": capacity,
        "valid": True,
        "hex": content[:256].hex(" "),
        "utf8": content.decode("utf-8", errors="replace"),
    }


def _scan_local_candidate_map(
    handle: wintypes.HANDLE,
    base_address: int,
    offsets: tuple[int, ...],
    *,
    scan_size: int,
    limit: int,
) -> dict[str, Any]:
    if base_address <= MIN_USER_POINTER:
        return {}
    result: dict[str, Any] = {}
    for offset in offsets:
        address = base_address + offset
        candidates = _scan_string_candidates(handle, address, scan_size=scan_size, limit=limit)
        if candidates:
            result[hex(offset)] = {
                "base_address": hex(address),
                "candidates": candidates,
            }
    return result


def _is_user_pointer(value: int) -> bool:
    return MIN_USER_POINTER < value <= MAX_USER_POINTER


def _is_ai_agent_module_pointer(value: int, module_base: int, module_size: int) -> bool:
    return module_base <= value < module_base + module_size


def _candidate_has_marker(
    candidate: dict[str, Any],
    markers: tuple[str, ...],
) -> bool:
    text = str(candidate.get("utf8", "")).lower()
    return any(marker in text for marker in markers)


def _append_unique_text_candidate(
    results: list[dict[str, Any]],
    seen: set[tuple[int, int, str]],
    context: tuple[str, int, str],
    candidate: dict[str, Any],
) -> None:
    root, depth, path = context
    ptr = int(str(candidate["ptr"]), 16)
    length = int(candidate["len"])
    text = str(candidate.get("utf8", ""))
    key = (ptr, length, text)
    if key in seen:
        return
    seen.add(key)
    item = dict(candidate)
    item["root"] = root
    item["depth"] = depth
    item["path"] = path
    results.append(item)


def _collect_pointer_roots(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    *,
    register_names: tuple[str, ...] = MODEL_INFO_POINTER_SCAN_REGISTERS,
    stack_scan_size: int = 0x380,
) -> list[tuple[str, int]]:
    roots: list[tuple[str, int]] = []
    seen: set[int] = set()

    def append(label: str, value: int) -> None:
        if not _is_user_pointer(value) or value in seen:
            return
        seen.add(value)
        roots.append((label, value))

    for name in register_names:
        append(name, int(registers[name], 16))

    for base_name in ("rsp", "rbp"):
        base = int(registers[base_name], 16)
        data = _read_memory(handle, base, stack_scan_size)
        for offset in range(0, len(data) - U64_SIZE + 1, U64_SIZE):
            value = int.from_bytes(data[offset : offset + U64_SIZE], "little")
            append(f"{base_name}+{offset:#x}", value)

    return roots


def _scan_pointer_tree_for_text(
    handle: wintypes.HANDLE,
    roots: list[tuple[str, int]],
    module_base: int,
    module_size: int,
    markers: tuple[str, ...],
) -> dict[str, Any]:
    queue: list[tuple[str, int, int, str]] = [
        (label, address, 0, label)
        for label, address in roots
    ]
    visited: set[int] = set()
    seen_candidates: set[tuple[int, int, str]] = set()
    results: list[dict[str, Any]] = []
    visited_count = 0

    while (
        queue
        and visited_count < MODEL_INFO_POINTER_SCAN_MAX_NODES
        and len(results) < MODEL_INFO_POINTER_SCAN_MAX_RESULTS
    ):
        root, address, depth, path = queue.pop(0)
        if not _is_user_pointer(address) or address in visited:
            continue
        visited.add(address)
        visited_count += 1

        candidates = _scan_string_candidates(
            handle,
            address,
            scan_size=MODEL_INFO_POINTER_SCAN_SIZE,
            limit=64,
        )
        for candidate in candidates:
            if not _candidate_has_marker(candidate, markers):
                continue
            _append_unique_text_candidate(
                results,
                seen_candidates,
                context=(root, depth, path),
                candidate=candidate,
            )
            if len(results) >= MODEL_INFO_POINTER_SCAN_MAX_RESULTS:
                break

        if depth >= MODEL_INFO_POINTER_SCAN_MAX_DEPTH or _is_ai_agent_module_pointer(
            address,
            module_base,
            module_size,
        ):
            continue

        data = _read_memory(handle, address, MODEL_INFO_POINTER_SCAN_SIZE)
        for offset in range(0, len(data) - U64_SIZE + 1, U64_SIZE):
            value = int.from_bytes(data[offset : offset + U64_SIZE], "little")
            if not _is_user_pointer(value) or value in visited:
                continue
            queue.append((root, value, depth + 1, f"{path}->+{offset:#x}"))

    return {
        "root_count": len(roots),
        "visited_count": visited_count,
        "truncated": (
            bool(queue)
            or visited_count >= MODEL_INFO_POINTER_SCAN_MAX_NODES
            or len(results) >= MODEL_INFO_POINTER_SCAN_MAX_RESULTS
        ),
        "candidates": results,
    }


def _collect_model_info_pointer_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    roots = _collect_pointer_roots(handle, registers)
    scan = _scan_pointer_tree_for_text(
        handle,
        roots,
        module_base,
        module_size,
        MODEL_INFO_INTERESTING_TEXT_MARKERS,
    )
    return {
        "pointer_roots": [
            {"label": label, "address": hex(address)}
            for label, address in roots[:80]
        ],
        "text_scan": scan,
    }


def _collect_failure_pointer_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    roots = _collect_pointer_roots(
        handle,
        registers,
        register_names=FAILURE_POINTER_SCAN_REGISTERS,
        stack_scan_size=0x700,
    )
    scan = _scan_pointer_tree_for_text(
        handle,
        roots,
        module_base,
        module_size,
        FAILURE_INTERESTING_TEXT_MARKERS,
    )
    return {
        "pointer_roots": [
            {"label": label, "address": hex(address)}
            for label, address in roots[:120]
        ],
        "text_scan": scan,
    }


def _read_rust_str_like(
    handle: wintypes.HANDLE,
    struct_address: int,
    max_len: int = 4096,
) -> dict[str, Any] | None:
    pair_size = U64_SIZE * 2
    data = _read_memory(handle, struct_address, pair_size)
    if len(data) != pair_size:
        return None

    ptr = int.from_bytes(data[0:8], "little")
    length = int.from_bytes(data[8:16], "little")
    if ptr <= MIN_USER_POINTER or length <= 0 or length > max_len:
        return {
            "struct_address": hex(struct_address),
            "ptr": hex(ptr),
            "len": length,
            "valid": False,
        }

    content = _read_memory(handle, ptr, length)
    if len(content) != length:
        return {
            "struct_address": hex(struct_address),
            "ptr": hex(ptr),
            "len": length,
            "valid": False,
            "reason": "short_read",
        }

    return {
        "struct_address": hex(struct_address),
        "ptr": hex(ptr),
        "len": length,
        "valid": True,
        "hex": content[:256].hex(" "),
        "utf8": content.decode("utf-8", errors="replace"),
    }


def _read_exact_local_text_candidates(
    handle: wintypes.HANDLE,
    base_address: int,
    offsets: tuple[int, ...],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for offset in offsets:
        address = base_address + offset
        raw = _read_memory(handle, address, RUST_STRING_SIZE)
        if len(raw) != RUST_STRING_SIZE:
            continue
        result[hex(offset)] = {
            "address": hex(address),
            "raw_qwords": [
                hex(int.from_bytes(raw[index : index + 8], "little"))
                for index in range(0, len(raw), 8)
            ],
            "as_string": _read_rust_string(handle, address),
            "as_str": _read_rust_str_like(handle, address),
        }
    return result


def _read_exact_register_text_candidates(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    register_names: tuple[str, ...],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in register_names:
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        result[name] = {
            "address": hex(address),
            "as_string": _read_rust_string(handle, address),
            "as_str": _read_rust_str_like(handle, address),
            "candidates": _scan_string_candidates(
                handle,
                address,
                scan_size=0x100,
                limit=8,
            ),
        }
    return result


def _collect_tunnel_target_state(
    handle: wintypes.HANDLE,
    target: str,
    rbp: int,
    rsp: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}

    if target == "tunnel_url_builder_result_ready_anchor" and rbp > MIN_USER_POINTER:
        extra["builder_result_string"] = _read_rust_string(handle, rbp + 0x10)

    if target == "tunnel_url_builder_http_fallback_anchor" and rbp > MIN_USER_POINTER:
        extra["builder_stack_local_pre_call"] = _read_rust_string(handle, rbp + 0x10)
        tunnel_id_len = _read_u64_from_process(handle, rbp + 0x18)
        if tunnel_id_len is not None:
            extra["builder_stack_local_len_field"] = tunnel_id_len

    if target.startswith("tunnel_url_builder_") and rsp > MIN_USER_POINTER:
        return_address = _read_u64_from_process(handle, rsp + TUNNEL_URL_BUILDER_STACK_SIZE)
        if return_address is not None:
            extra["caller_return_address"] = hex(return_address)
            if return_address >= CALL_REL32_SIZE:
                extra["caller_callsite_guess"] = hex(return_address - CALL_REL32_SIZE)

    return extra


def _collect_custom_model_param_extract_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    rbp: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    rbp_locals = _scan_local_candidate_map(
        handle,
        rbp,
        CUSTOM_MODEL_PARAM_RBP_SCAN_OFFSETS,
        scan_size=0x100,
        limit=12,
    )
    if rbp_locals:
        extra["custom_model_param_rbp_locals"] = rbp_locals

    exact_locals = _read_exact_local_text_candidates(
        handle,
        rbp,
        CUSTOM_MODEL_PARAM_RBP_SCAN_OFFSETS,
    )
    if exact_locals:
        extra["custom_model_param_exact_locals"] = exact_locals

    register_text = _read_exact_register_text_candidates(
        handle,
        registers,
        ("rcx", "rdx", "rsi", "r13"),
    )
    if register_text:
        extra["custom_model_param_register_text"] = register_text

    return extra


def _collect_custom_model_timing_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    for name in ("r14", "rbx", "rsi"):
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        candidates = _scan_string_candidates(
            handle,
            address,
            scan_size=0x900,
            limit=96,
        )
        if candidates:
            extra[f"{name}_deep_scan"] = {
                "base_address": hex(address),
                "candidates": candidates,
            }
    return extra


def _collect_custom_model_copy_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    for name in ("r14", "rbx", "rsi"):
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        candidates = _scan_string_candidates(
            handle,
            address,
            scan_size=0x900,
            limit=128,
        )
        if candidates:
            extra[f"{name}_deep_scan"] = {
                "base_address": hex(address),
                "candidates": candidates,
            }
    return extra


def _collect_custom_model_callsite_state(  # noqa: PLR0912
    handle: wintypes.HANDLE,
    registers: dict[str, str],
) -> dict[str, Any]:
    extra: dict[str, Any] = {
        "callsite_stage_byte": int(registers["rcx"], 16) & 0xFF,
    }

    rbx = int(registers["rbx"], 16)
    if rbx <= MIN_USER_POINTER:
        return extra

    context_ptr = _read_u64_from_process(handle, rbx + 0xC0)
    if context_ptr is None or context_ptr <= MIN_USER_POINTER:
        return extra

    extra["rbx_context_ptr"] = hex(context_ptr)
    context_fields: dict[str, Any] = {}
    for name, offset in (
        ("config_name", 0x1E8),
        ("provider", 0x230),
        ("model_name", 0x248),
        ("api_key", 0x260),
        ("base_url", 0x278),
        ("trace_parent", 0x730),
        ("active_file_name", 0x848),
    ):
        field = _read_rust_str_like(handle, context_ptr + offset)
        if field and field.get("valid"):
            context_fields[name] = field["utf8"]
    if context_fields:
        extra["context_fields"] = context_fields

    chain_summary: dict[str, Any] = {}
    for name, offset in (
        ("ctx_0x140", 0x140),
        ("ctx_0x148", 0x148),
        ("ctx_0x150", 0x150),
        ("ctx_0x160", 0x160),
        ("ctx_0x168", 0x168),
    ):
        outer_ptr = _read_u64_from_process(handle, context_ptr + offset)
        if outer_ptr is None or outer_ptr <= MIN_USER_POINTER:
            continue
        entry: dict[str, Any] = {"outer_ptr": hex(outer_ptr)}
        inner_ptr = _read_u64_from_process(handle, outer_ptr)
        if inner_ptr is not None and inner_ptr > MIN_USER_POINTER:
            entry["inner_ptr"] = hex(inner_ptr)
        chain_summary[name] = entry
    if chain_summary:
        extra["context_pointer_chains"] = chain_summary

    model_outer_ptr = _read_u64_from_process(handle, context_ptr + 0x160)
    if model_outer_ptr is None or model_outer_ptr <= MIN_USER_POINTER:
        return extra

    model_inner_ptr = _read_u64_from_process(handle, model_outer_ptr)
    if model_inner_ptr is None or model_inner_ptr <= MIN_USER_POINTER:
        return extra

    extra["resolved_model_ptr_chain"] = {
        "outer_ptr": hex(model_outer_ptr),
        "inner_ptr": hex(model_inner_ptr),
    }

    model_fields: dict[str, Any] = {}
    owned_config_name = _read_rust_string(handle, model_inner_ptr + 0x3F8)
    if owned_config_name and owned_config_name.get("valid"):
        model_fields["config_name_owned"] = owned_config_name["utf8"]

    for name, offset in (
        ("config_name", 0x410),
        ("provider", 0x440),
        ("model_name", 0x458),
        ("api_key", 0x470),
        ("base_url", 0x488),
    ):
        field = _read_rust_str_like(handle, model_inner_ptr + offset)
        if field and field.get("valid"):
            model_fields[name] = field["utf8"]
    if model_fields:
        extra["resolved_model_fields"] = model_fields

    return extra


def _collect_custom_model_proxy_runtime_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    rbp: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}

    register_text = _read_exact_register_text_candidates(
        handle,
        registers,
        ("rcx", "rdx", "r8", "r9", "r14", "r15"),
    )
    if register_text:
        extra["custom_model_proxy_register_text"] = register_text

    if rbp > MIN_USER_POINTER:
        rbp_locals = _scan_local_candidate_map(
            handle,
            rbp,
            CUSTOM_MODEL_PROXY_RUNTIME_RBP_SCAN_OFFSETS,
            scan_size=0x180,
            limit=16,
        )
        if rbp_locals:
            extra["custom_model_proxy_rbp_locals"] = rbp_locals

        exact_locals = _read_exact_local_text_candidates(
            handle,
            rbp,
            CUSTOM_MODEL_PROXY_RUNTIME_RBP_SCAN_OFFSETS,
        )
        if exact_locals:
            extra["custom_model_proxy_exact_locals"] = exact_locals

    for name in ("rcx", "rdx", "r14", "r15"):
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        candidates = _scan_string_candidates(
            handle,
            address,
            scan_size=0x700,
            limit=64,
        )
        if candidates:
            extra[f"{name}_deep_scan"] = {
                "base_address": hex(address),
                "candidates": candidates,
            }

    return extra


def _filter_interesting_sse_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for candidate in candidates:
        text = str(candidate.get("utf8", "")).lower()
        if any(marker in text for marker in INTERESTING_SSE_TEXT_MARKERS):
            result.append(candidate)
    return result


def _filter_interesting_route_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for candidate in candidates:
        text = str(candidate.get("utf8", "")).lower()
        if any(marker in text for marker in INTERESTING_ROUTE_TEXT_MARKERS):
            result.append(candidate)
    return result


def _filter_interesting_failure_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for candidate in candidates:
        text = str(candidate.get("utf8", "")).lower()
        if any(marker in text for marker in INTERESTING_FAILURE_TEXT_MARKERS):
            result.append(candidate)
    return result


def _read_qword_window(
    handle: wintypes.HANDLE,
    address: int,
    size: int,
) -> list[str]:
    raw = _read_memory(handle, address, size)
    result: list[str] = []
    for index in range(0, len(raw), U64_SIZE):
        chunk = raw[index : index + U64_SIZE]
        if len(chunk) != U64_SIZE:
            break
        result.append(hex(int.from_bytes(chunk, "little")))
    return result


def _collect_struct_snapshot(
    handle: wintypes.HANDLE,
    address: int,
    size: int,
) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "address": hex(address),
        "size": hex(size),
        "qwords": _read_qword_window(handle, address, size),
    }
    pointer_candidates: dict[str, Any] = {}
    for index, qword in enumerate(snapshot["qwords"]):
        value = int(str(qword), 16)
        if value <= MIN_USER_POINTER:
            continue
        candidates = _filter_interesting_route_candidates(
            _scan_string_candidates(
                handle,
                value,
                scan_size=0x120,
                limit=6,
            )
        )
        if candidates:
            pointer_candidates[hex(index * 8)] = {
                "pointer": hex(value),
                "candidates": candidates,
            }
    if pointer_candidates:
        snapshot["pointer_candidates"] = pointer_candidates
    return snapshot


def _collect_based_struct_snapshots(
    handle: wintypes.HANDLE,
    base_address: int,
    specs: tuple[tuple[int, int], ...],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if base_address <= MIN_USER_POINTER:
        return result
    for offset, size in specs:
        result[hex(offset)] = _collect_struct_snapshot(
            handle,
            base_address + offset,
            size,
        )
    return result


def _collect_current_route_wakeup_callback(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    rdx = int(registers["rdx"], 16)
    if rdx <= MIN_USER_POINTER:
        return {}
    queue_holder_qwords = _read_qword_window(handle, rdx, 0x20)
    if not queue_holder_qwords:
        return {}

    wakeup_slot_payload: dict[str, Any] = {
        "queue_holder_address": hex(rdx),
        "queue_holder_qwords": queue_holder_qwords,
        "queue_holder_snapshot": _collect_struct_snapshot(handle, rdx, 0x80),
    }
    queue_owner = int(queue_holder_qwords[0], 16)
    if queue_owner <= MIN_USER_POINTER:
        return {"current_route_wakeup_callback": wakeup_slot_payload}

    wakeup_slot_address = queue_owner + 0x100
    wakeup_slot = _collect_struct_snapshot(handle, wakeup_slot_address, 0x20)
    wakeup_slot_payload["queue_owner"] = hex(queue_owner)
    wakeup_slot_payload["queue_owner_snapshot"] = _collect_struct_snapshot(
        handle,
        queue_owner,
        0x180,
    )
    queue_owner_candidates = _filter_interesting_route_candidates(
        _scan_string_candidates(
            handle,
            queue_owner,
            scan_size=0x300,
            limit=32,
        )
    )
    if queue_owner_candidates:
        wakeup_slot_payload["queue_owner_text_candidates"] = queue_owner_candidates
    wakeup_slot_payload["wakeup_slot"] = wakeup_slot
    raw_wakeup_qwords = wakeup_slot.get("qwords")
    wakeup_qwords = (
        cast(list[str], raw_wakeup_qwords) if isinstance(raw_wakeup_qwords, list) else []
    )
    if len(wakeup_qwords) < MIN_QWORD_PAIR_LEN:
        return {"current_route_wakeup_callback": wakeup_slot_payload}

    callback_object = int(str(wakeup_qwords[0]), 16)
    callback_context = int(str(wakeup_qwords[1]), 16)
    callback_summary: dict[str, Any] = {
        "object": hex(callback_object),
        "context": hex(callback_context),
    }
    wakeup_slot_payload["callback"] = callback_summary
    if callback_object <= MIN_USER_POINTER:
        return {"current_route_wakeup_callback": wakeup_slot_payload}

    callback_object_snapshot = _collect_struct_snapshot(handle, callback_object, 0x20)
    wakeup_slot_payload["callback_object_snapshot"] = callback_object_snapshot
    raw_callback_object_qwords = callback_object_snapshot.get("qwords")
    callback_object_qwords = (
        cast(list[str], raw_callback_object_qwords)
        if isinstance(raw_callback_object_qwords, list)
        else []
    )
    if len(callback_object_qwords) >= MIN_QWORD_PAIR_LEN:
        callback_code = int(str(callback_object_qwords[1]), 16)
        callback_summary["code_ptr"] = hex(callback_code)
        if module_base <= callback_code < module_base + module_size:
            callback_summary["ai_agent_rva"] = hex(callback_code - module_base)

    return {"current_route_wakeup_callback": wakeup_slot_payload}


def _collect_current_route_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    rbp: int,
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    if rbp <= MIN_USER_POINTER:
        return extra

    rbp_locals = _scan_local_candidate_map(
        handle,
        rbp,
        CURRENT_ROUTE_TEXT_OFFSETS,
        scan_size=0x180,
        limit=12,
    )
    filtered_locals: dict[str, Any] = {}
    for offset, item in rbp_locals.items():
        if not isinstance(item, dict):
            continue
        item_map = cast(dict[str, Any], item)
        raw_candidates = item_map.get("candidates", [])
        candidates = _filter_interesting_route_candidates(
            cast(list[dict[str, Any]], raw_candidates)
            if isinstance(raw_candidates, list)
            else []
        )
        if candidates:
            filtered_locals[offset] = {
                "base_address": item_map["base_address"],
                "candidates": candidates,
            }
    if filtered_locals:
        extra["current_route_rbp_locals"] = filtered_locals

    exact_locals = _read_exact_local_text_candidates(
        handle,
        rbp,
        CURRENT_ROUTE_TEXT_OFFSETS,
    )
    if exact_locals:
        extra["current_route_exact_locals"] = exact_locals

    struct_snapshots: dict[str, Any] = {}
    for offset, size in CURRENT_ROUTE_STRUCT_SPECS:
        struct_snapshots[hex(offset)] = _collect_struct_snapshot(
            handle,
            rbp + offset,
            size,
        )
    if struct_snapshots:
        extra["current_route_structs"] = struct_snapshots

    register_structs: dict[str, Any] = {}
    for name in ("rcx", "rdx", "r8", "r9", "r14", "r15"):
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        register_structs[name] = _collect_struct_snapshot(handle, address, 0x60)
    if register_structs:
        extra["current_route_register_structs"] = register_structs

    register_text = _read_exact_register_text_candidates(
        handle,
        registers,
        ("rcx", "rdx", "r8", "r9", "r14", "r15"),
    )
    if register_text:
        extra["current_route_register_text"] = register_text

    extra.update(
        _collect_current_route_wakeup_callback(
            handle,
            registers,
            module_base,
            module_size,
        )
    )

    return extra


def _collect_queue_waker_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    rcx = int(registers["rcx"], 16)
    if rcx <= MIN_USER_POINTER:
        return {}

    snapshot = _collect_struct_snapshot(handle, rcx, 0x40)
    raw_qwords = snapshot.get("qwords")
    qwords = cast(list[str], raw_qwords) if isinstance(raw_qwords, list) else []
    payload: dict[str, Any] = {
        "waker_slot_address": hex(rcx),
        "waker_slot_snapshot": snapshot,
    }
    if len(qwords) < MIN_WAKER_SLOT_QWORDS:
        return {"queue_waker_state": payload}

    waker_object = int(str(qwords[0]), 16)
    waker_context = int(str(qwords[1]), 16)
    waker_state = int(str(qwords[2]), 16)
    payload["waker_fields"] = {
        "object": hex(waker_object),
        "context": hex(waker_context),
        "state": hex(waker_state),
    }
    if waker_object > MIN_USER_POINTER:
        object_snapshot = _collect_struct_snapshot(handle, waker_object, 0x30)
        payload["waker_object_snapshot"] = object_snapshot
        raw_object_qwords = object_snapshot.get("qwords")
        object_qwords = (
            cast(list[str], raw_object_qwords) if isinstance(raw_object_qwords, list) else []
        )
        if len(object_qwords) >= MIN_QWORD_PAIR_LEN:
            code_ptr = int(str(object_qwords[1]), 16)
            if module_base <= code_ptr < module_base + module_size:
                payload["waker_fields"]["object_code_rva"] = hex(
                    code_ptr - module_base
                )

    return {"queue_waker_state": payload}


def _collect_queue_receiver_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in ("rcx", "rdx", "r8", "r9", "rsi", "rdi"):
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        result[name] = {
            "address": hex(address),
            "snapshot": _collect_struct_snapshot(handle, address, 0x100),
            "text_candidates": _filter_interesting_route_candidates(
                _scan_string_candidates(
                    handle,
                    address,
                    scan_size=0x240,
                    limit=16,
                )
            ),
        }
    if not result:
        return {}
    return {"queue_receiver_registers": result}


def _collect_failure_route_state(
    handle: wintypes.HANDLE,
    target: str,
    registers: dict[str, str],
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}

    if target in {"failure_sse_open_error_1", "failure_sse_open_error_2"}:
        base = int(registers["rbx"], 16)
        base_label = "rbx"
        scan_offsets = FAILURE_SSE_OPEN_BASE_OFFSETS
        specs = FAILURE_SSE_OPEN_STRUCT_SPECS
    else:
        base = int(registers["rbp"], 16)
        base_label = "rbp"
        scan_offsets = FAILURE_UNKNOWN_EVENT_BASE_OFFSETS
        specs = FAILURE_UNKNOWN_EVENT_STRUCT_SPECS

    if base <= MIN_USER_POINTER:
        return extra

    extra["failure_base_register"] = base_label
    extra["failure_base_address"] = hex(base)

    locals_map = _scan_local_candidate_map(
        handle,
        base,
        scan_offsets,
        scan_size=0x180,
        limit=12,
    )
    filtered_locals: dict[str, Any] = {}
    for offset, item in locals_map.items():
        if not isinstance(item, dict):
            continue
        item_map = cast(dict[str, Any], item)
        raw_candidates = item_map.get("candidates", [])
        candidates = _filter_interesting_failure_candidates(
            cast(list[dict[str, Any]], raw_candidates)
            if isinstance(raw_candidates, list)
            else []
        )
        if candidates:
            filtered_locals[offset] = {
                "base_address": item_map["base_address"],
                "candidates": candidates,
            }
    if filtered_locals:
        extra["failure_locals"] = filtered_locals

    exact_locals = _read_exact_local_text_candidates(
        handle,
        base,
        scan_offsets,
    )
    if exact_locals:
        extra["failure_exact_locals"] = exact_locals

    structs = _collect_based_struct_snapshots(handle, base, specs)
    if structs:
        extra["failure_structs"] = structs

    register_text = _read_exact_register_text_candidates(
        handle,
        registers,
        ("rbx", "rbp", "rcx", "rdx", "r8", "r9", "r14", "r15", "rdi", "rsi"),
    )
    if register_text:
        extra["failure_register_text"] = register_text

    pointer_state = _collect_failure_pointer_state(
        handle,
        registers,
        module_base,
        module_size,
    )
    if pointer_state["text_scan"]["candidates"]:
        extra["failure_pointer_state"] = pointer_state

    return extra


def _collect_sse_open_state(  # noqa: PLR0912
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    rbp: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}

    register_text = _read_exact_register_text_candidates(
        handle,
        registers,
        ("rcx", "rdx", "r8", "r14", "r15", "rsi", "rdi"),
    )
    if register_text:
        extra["sse_open_register_text"] = register_text

    deep_register_scans: dict[str, Any] = {}
    for name in ("rcx", "rdx", "r8", "r14", "r15", "rsi", "rdi"):
        address = int(registers[name], 16)
        if address <= MIN_USER_POINTER:
            continue
        candidates = _filter_interesting_sse_candidates(
            _scan_string_candidates(
                handle,
                address,
                scan_size=0x900,
                limit=128,
            )
        )
        if candidates:
            deep_register_scans[name] = {
                "base_address": hex(address),
                "candidates": candidates,
            }
    if deep_register_scans:
        extra["sse_open_register_deep_scans"] = deep_register_scans

    if rbp <= MIN_USER_POINTER:
        return extra

    rbp_locals = _scan_local_candidate_map(
        handle,
        rbp,
        SSE_OPEN_RBP_SCAN_OFFSETS,
        scan_size=0x300,
        limit=24,
    )
    filtered_rbp_locals: dict[str, Any] = {}
    for offset, item in rbp_locals.items():
        if not isinstance(item, dict):
            continue
        item_map = cast(dict[str, Any], item)
        raw_candidates = item_map.get("candidates", [])
        candidates = _filter_interesting_sse_candidates(
            cast(list[dict[str, Any]], raw_candidates)
            if isinstance(raw_candidates, list)
            else []
        )
        if candidates:
            filtered_rbp_locals[offset] = {
                "base_address": item_map["base_address"],
                "candidates": candidates,
            }
    if filtered_rbp_locals:
        extra["sse_open_rbp_locals"] = filtered_rbp_locals

    exact_locals = _read_exact_local_text_candidates(
        handle,
        rbp,
        SSE_OPEN_RBP_SCAN_OFFSETS,
    )
    if exact_locals:
        extra["sse_open_exact_locals"] = exact_locals

    local_deep_scans: dict[str, Any] = {}
    for offset in SSE_OPEN_RBP_SCAN_OFFSETS:
        address = rbp + offset
        candidates = _filter_interesting_sse_candidates(
            _scan_string_candidates(
                handle,
                address,
                scan_size=0x900,
                limit=64,
            )
        )
        if candidates:
            local_deep_scans[hex(offset)] = {
                "base_address": hex(address),
                "candidates": candidates,
            }
    if local_deep_scans:
        extra["sse_open_local_deep_scans"] = local_deep_scans

    return extra


def _collect_openai_post_parse_state(
    handle: wintypes.HANDLE,
    registers: dict[str, str],
    rbp: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    if rbp <= MIN_USER_POINTER:
        return extra

    qwords: dict[str, str] = {}
    pointer_scans: dict[str, Any] = {}
    for offset in OPENAI_POST_PARSE_QWORD_OFFSETS:
        address = rbp + offset
        value = _read_u64_from_process(handle, address)
        if value is None:
            continue
        qwords[hex(offset)] = hex(value)
        if value > MIN_USER_POINTER:
            candidates = _scan_string_candidates(
                handle,
                value,
                scan_size=0x120,
                limit=8,
            )
            if candidates:
                pointer_scans[hex(offset)] = {
                    "pointer": hex(value),
                    "candidates": candidates,
                }
    if qwords:
        extra["openai_post_parse_qwords"] = qwords
    if pointer_scans:
        extra["openai_post_parse_pointer_scans"] = pointer_scans

    exact_locals = _read_exact_local_text_candidates(
        handle,
        rbp,
        OPENAI_POST_PARSE_TEXT_OFFSETS,
    )
    if exact_locals:
        extra["openai_post_parse_exact_locals"] = exact_locals

    rbp_locals = _scan_local_candidate_map(
        handle,
        rbp,
        OPENAI_POST_PARSE_TEXT_OFFSETS,
        scan_size=0x180,
        limit=12,
    )
    if rbp_locals:
        extra["openai_post_parse_rbp_locals"] = rbp_locals

    exact_registers = _read_exact_register_text_candidates(
        handle,
        registers,
        ("r14", "rsi", "rdi"),
    )
    if exact_registers:
        extra["openai_post_parse_registers"] = exact_registers

    return extra


def _target_specific_state(  # noqa: PLR0912, PLR0915
    handle: wintypes.HANDLE,
    target: str,
    registers: dict[str, str],
    module_base: int,
    module_size: int,
) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    rbp = int(registers["rbp"], 16)
    rsp = int(registers["rsp"], 16)
    extra.update(_collect_tunnel_target_state(handle, target, rbp, rsp))

    if target in MODEL_DETAIL_TARGETS and rsp > MIN_USER_POINTER:
        stack_locals = _scan_local_candidate_map(
            handle,
            rsp,
            MODEL_DETAIL_STACK_SCAN_OFFSETS,
            scan_size=0x120,
            limit=12,
        )
        if stack_locals:
            extra["model_detail_stack_locals"] = stack_locals

    if target in MODEL_INFO_LOG_TARGETS and rbp > MIN_USER_POINTER:
        rbp_locals = _scan_local_candidate_map(
            handle,
            rbp,
            MODEL_INFO_RBP_SCAN_OFFSETS,
            scan_size=0x180,
            limit=12,
        )
        if rbp_locals:
            extra["model_info_rbp_locals"] = rbp_locals
        extra["model_info_pointer_state"] = _collect_model_info_pointer_state(
            handle,
            registers,
            module_base,
            module_size,
        )

    if target in CUSTOM_MODEL_DEBUG_FMT_TARGETS:
        rcx = int(registers["rcx"], 16)
        custom_model_candidates = _scan_string_candidates(
            handle,
            rcx,
            scan_size=0x700,
            limit=64,
        )
        if custom_model_candidates:
            extra["custom_model_rcx_scan"] = {
                "base_address": hex(rcx),
                "candidates": custom_model_candidates,
            }

    if target in CUSTOM_MODEL_WRITE_TARGETS and rbp > MIN_USER_POINTER:
        rbp_locals = _scan_local_candidate_map(
            handle,
            rbp,
            CUSTOM_MODEL_WRITE_RBP_SCAN_OFFSETS,
            scan_size=0x180,
            limit=16,
        )
        if rbp_locals:
            extra["custom_model_write_rbp_locals"] = rbp_locals

        exact_locals = _read_exact_local_text_candidates(
            handle,
            rbp,
            (0x16C0, 0x16D8, 0x16F0),
        )
        if exact_locals:
            extra["custom_model_write_exact_locals"] = exact_locals

        r8 = int(registers["r8"], 16)
        if r8 > MIN_USER_POINTER:
            custom_model_candidates = _scan_string_candidates(
                handle,
                r8,
                scan_size=0x1600,
                limit=64,
            )
            if custom_model_candidates:
                extra["custom_model_write_dest_scan"] = {
                    "base_address": hex(r8),
                    "candidates": custom_model_candidates,
                }

    if target in CUSTOM_MODEL_PARAM_EXTRACT_TARGETS and rbp > MIN_USER_POINTER:
        extra.update(_collect_custom_model_param_extract_state(handle, registers, rbp))

    if target in CUSTOM_MODEL_TIMING_TARGETS:
        extra.update(_collect_custom_model_timing_state(handle, registers))

    if target in CUSTOM_MODEL_COPY_TARGETS:
        extra.update(_collect_custom_model_copy_state(handle, registers))

    if target in CUSTOM_MODEL_CALLSITE_TARGETS:
        extra.update(_collect_custom_model_callsite_state(handle, registers))

    if target in CUSTOM_MODEL_PROXY_RUNTIME_TARGETS:
        extra.update(_collect_custom_model_proxy_runtime_state(handle, registers, rbp))

    if target in SSE_OPEN_TARGETS:
        extra.update(_collect_sse_open_state(handle, registers, rbp))

    if target in OPENAI_POST_PARSE_TARGETS:
        extra.update(_collect_openai_post_parse_state(handle, registers, rbp))

    if target in CURRENT_ROUTE_TARGETS:
        extra.update(
            _collect_current_route_state(
                handle,
                registers,
                rbp,
                module_base,
                module_size,
            )
        )

    if target in QUEUE_WAKER_TARGETS:
        extra.update(
            _collect_queue_waker_state(
                handle,
                registers,
                module_base,
                module_size,
            )
        )

    if target in QUEUE_RECEIVER_TARGETS:
        extra.update(_collect_queue_receiver_state(handle, registers))

    if target in FAILURE_ROUTE_TARGETS:
        extra.update(
            _collect_failure_route_state(
                handle,
                target,
                registers,
                module_base,
                module_size,
            )
        )

    return extra


def _handle_breakpoint_hit(
    process: wintypes.HANDLE,
    thread_id: int,
    context_info: BreakpointContext,
) -> dict[str, Any]:
    thread = _open_thread(thread_id)
    try:
        context = _read_context(thread)
        _put_u64(context, RIP_OFFSET, context_info.address)
        regs = _registers(context)
        previews = _pointer_previews(process, regs)
        register_string_candidates = _collect_register_string_candidates(process, regs)
        stack_pointer = int(regs["rsp"], 16)
        stack_qwords = _read_stack_qwords(
            process,
            stack_pointer,
            context_info.module_base,
            context_info.module_size,
        )
        stack_string_candidates = _scan_string_candidates(process, stack_pointer, scan_size=0x180)
        ai_agent_stack_frames = _extract_ai_agent_stack_frames(stack_qwords)
        extra = _target_specific_state(
            process,
            context_info.target_label,
            regs,
            context_info.module_base,
            context_info.module_size,
        )
        _write_memory(process, context_info.address, context_info.original)
        _write_context(thread, context)
    finally:
        _close(thread)

    return {
        "thread_id": thread_id,
        "registers": regs,
        "pointer_previews": previews,
        "register_string_candidates": register_string_candidates,
        "module_base": hex(context_info.module_base),
        "module_size": hex(context_info.module_size),
        "ai_agent_stack_frames": ai_agent_stack_frames,
        "ai_agent_stack_rvas": _summarize_stack_frames(ai_agent_stack_frames),
        "stack_qwords": stack_qwords,
        "stack_string_candidates": stack_string_candidates,
        "target_specific": extra,
    }


def run_probe(
    pid: int | None,
    module_path: Path,
    request: ProbeRequest,
) -> dict[str, Any]:
    target_pid, resolved_sites = _resolve_probe_sites(
        pid,
        module_path,
        request,
    )
    module_base, module_size = _resolve_module_context(target_pid, module_path)
    privilege = enable_debug_privilege()
    if not DebugActiveProcess(target_pid):
        error = _last_error(f"DebugActiveProcess({target_pid})")
        error.add_note(f"debug_privilege={privilege}")
        raise error

    process = _open_process(target_pid)
    sites: list[BreakpointSite] = []
    for label, address in resolved_sites:
        original = _read_memory(process, address, 1)
        if len(original) != 1:
            raise RuntimeError(f"读取断点原字节失败: {hex(address)}")
        sites.append(
            BreakpointSite(
                label=label,
                address=address,
                original=original,
            )
        )
    site_by_address = {site.address: site for site in sites}

    started = time.monotonic()
    try:
        print(
            json.dumps(
                {
                    "probe_attach": {
                        "pid": target_pid,
                        "module_base": hex(module_base),
                        "module_size": hex(module_size),
                        "breakpoints": {site.label: hex(site.address) for site in sites},
                    }
                },
                ensure_ascii=False,
                indent=2,
            ),
            flush=True,
        )
        for site in sites:
            _write_memory(process, site.address, b"\xCC")
        while True:
            if request.timeout_seconds > 0 and time.monotonic() - started > request.timeout_seconds:
                return {
                    "pid": target_pid,
                    "status": "timeout",
                    "breakpoints": {site.label: hex(site.address) for site in sites},
                }

            event = DEBUG_EVENT()
            if not WaitForDebugEvent(ctypes.byref(event), 1000):
                continue

            status = DBG_CONTINUE
            if event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                record = event.u.Exception.ExceptionRecord
                exception_address = int(record.ExceptionAddress)
                matched_site = site_by_address.get(exception_address)
                if record.ExceptionCode == EXCEPTION_BREAKPOINT and matched_site is not None:
                    hit_payload = _handle_breakpoint_hit(
                        process,
                        int(event.dwThreadId),
                        BreakpointContext(
                            address=matched_site.address,
                            original=matched_site.original,
                            target_label=matched_site.label,
                            module_base=module_base,
                            module_size=module_size,
                        ),
                    )
                    ContinueDebugEvent(event.dwProcessId, event.dwThreadId, DBG_CONTINUE)
                    return {
                        "pid": target_pid,
                        "status": "hit",
                        "target": matched_site.label,
                        "breakpoint": hex(matched_site.address),
                        "armed_breakpoints": {site.label: hex(site.address) for site in sites},
                        **hit_payload,
                    }
                status = DBG_EXCEPTION_NOT_HANDLED
            elif event.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT:
                return {"pid": target_pid, "status": "process_exited"}

            ContinueDebugEvent(event.dwProcessId, event.dwThreadId, status)
    finally:
        for site in sites:
            _write_memory(process, site.address, site.original)
        DebugActiveProcessStop(target_pid)
        _close(process)


def _format_timeout_at(seconds: int) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + seconds))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="attach ai_agent.dll 并等待一个 native 锚点命中。")
    parser.add_argument("--pid", type=int, help="目标 PID；默认自动选择")
    parser.add_argument(
        "--module-base",
        type=lambda value: int(value, 0),
        help="已知 ai_agent.dll 运行时基址；与 --pid 一起使用可跳过模块枚举",
    )
    parser.add_argument("--module-path", type=Path, default=AI_AGENT_DLL, help="目标模块")
    parser.add_argument(
        "--target",
        choices=tuple(DEFAULT_RVAS),
        help="要打的 native 锚点",
    )
    parser.add_argument(
        "--profile",
        choices=tuple(BREAKPOINT_PROFILES),
        help="预设的一组断点；命中任意一个即返回",
    )
    parser.add_argument("--rva", type=lambda value: int(value, 0), help="直接指定模块内 RVA")
    parser.add_argument("--address", type=lambda value: int(value, 0), help="直接指定绝对 VA")
    parser.add_argument("--timeout-seconds", type=int, default=120, help="等待秒数")
    parser.add_argument(
        "--wait-for-module-seconds",
        type=int,
        default=0,
        help="如果 ai_agent.dll 尚未加载，最多等待多少秒后再开始挂断点",
    )
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        cast(Any, sys.stdout).reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    request = ProbeRequest(
        target=args.target,
        profile=args.profile,
        timeout_seconds=args.timeout_seconds,
        wait_for_module_seconds=args.wait_for_module_seconds,
        module_base=args.module_base,
        address=args.address,
        rva=args.rva,
    )
    print(
        f"[probe] timeout_at={_format_timeout_at(request.timeout_seconds)} "
        f"timeout_seconds={request.timeout_seconds}",
        flush=True,
    )
    payload = run_probe(
        args.pid,
        args.module_path,
        request,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)
    return 0


close_process_handle = _close
format_timeout_at = _format_timeout_at
last_windows_error = _last_error
open_process_handle = _open_process
open_thread_handle = _open_thread
put_u64 = _put_u64
read_thread_context = _read_context
read_process_memory = _read_memory
format_registers = _registers
resolve_runtime_module = _resolve_runtime_module
write_thread_context = _write_context
write_process_memory = _write_memory


if __name__ == "__main__":
    raise SystemExit(main())
