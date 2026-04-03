from __future__ import annotations

import hashlib
import re
import threading
from dataclasses import dataclass
from typing import Any, Literal, cast

from modules.proxy.param_self_heal_signal import (
    extract_litellm_unsupported_params_from_message,
)

TEMPORARY_SELF_HEAL_WARNING_PREFIX = "⚠️ [临时兼容]"
NON_RETRYABLE_INTERNAL_CALL_KWARGS: frozenset[str] = frozenset(
    {
        "messages",
        "model",
        "api_base",
        "base_url",
        "api_key",
        "custom_llm_provider",
        "ssl_verify",
        "max_retries",
        "num_retries",
        "allowed_openai_params",
        "extra_headers",
    }
)

type SelfHealCacheKey = tuple[str, str, str, str, str]


@dataclass(frozen=True)
class UnsupportedParamRule:
    location: Literal["top_level", "extra_body"]
    path: tuple[str, ...]

    @property
    def label(self) -> str:
        path_label = ".".join(self.path)
        if self.location == "extra_body":
            return f"extra_body.{path_label}"
        return path_label


@dataclass(frozen=True)
class UnsupportedParamSelection:
    rule: UnsupportedParamRule
    cacheable: bool


@dataclass(frozen=True)
class ParamHint:
    value: str
    unsupported: bool


class UpstreamParamSelfHealController:
    """临时的上游参数自愈逻辑，后续由参数覆盖机制替换。"""

    def __init__(self) -> None:
        self._cache: dict[SelfHealCacheKey, set[UnsupportedParamRule]] = {}
        self._cache_lock = threading.Lock()

    @staticmethod
    def build_cache_key(
        *,
        provider: str,
        request_api: str,
        base_url: str,
        model: str,
        api_key: str,
    ) -> SelfHealCacheKey:
        return (
            provider,
            request_api,
            base_url,
            model,
            UpstreamParamSelfHealController._build_auth_fingerprint(api_key),
        )

    def apply_cached_rules(
        self,
        *,
        cache_key: SelfHealCacheKey,
        call_kwargs: dict[str, Any],
    ) -> tuple[dict[str, Any], list[UnsupportedParamRule]]:
        with self._cache_lock:
            cached_rules = sorted(
                self._cache.get(cache_key, set()),
                key=lambda rule: rule.label,
            )

        updated_call_kwargs = call_kwargs
        applied_rules: list[UnsupportedParamRule] = []
        for rule in cached_rules:
            next_call_kwargs, changed = self.apply_rule(
                call_kwargs=updated_call_kwargs,
                rule=rule,
            )
            if not changed:
                continue
            updated_call_kwargs = next_call_kwargs
            applied_rules.append(rule)
        return updated_call_kwargs, applied_rules

    def remember_rules(
        self,
        *,
        cache_key: SelfHealCacheKey,
        rules: set[UnsupportedParamRule],
    ) -> None:
        if not rules:
            return
        with self._cache_lock:
            existing_rules = self._cache.setdefault(cache_key, set())
            existing_rules.update(rules)

    @classmethod
    def select_rule(
        cls,
        *,
        call_kwargs: dict[str, Any],
        message: str | None,
        param: str | None,
        skipped_rules: set[UnsupportedParamRule],
    ) -> UnsupportedParamSelection | None:
        hints = cls._extract_param_hints(
            message=message,
            param=param,
        )
        for hint in hints:
            selection = cls._select_rule_from_hint(
                hint=hint.value,
                call_kwargs=call_kwargs,
                unsupported_hint=hint.unsupported,
            )
            if selection is None:
                continue
            if selection.rule in skipped_rules:
                continue
            return selection
        return None

    @staticmethod
    def apply_rule(
        *,
        call_kwargs: dict[str, Any],
        rule: UnsupportedParamRule,
    ) -> tuple[dict[str, Any], bool]:
        updated_call_kwargs = dict(call_kwargs)
        if rule.location == "extra_body":
            extra_body_obj = updated_call_kwargs.get("extra_body")
            if not isinstance(extra_body_obj, dict):
                return call_kwargs, False
            extra_body = dict(cast(dict[str, Any], extra_body_obj))
            changed = UpstreamParamSelfHealController._remove_path_from_mapping(
                extra_body,
                rule.path,
            )
            if not changed:
                return call_kwargs, False
            if extra_body:
                updated_call_kwargs["extra_body"] = extra_body
            else:
                updated_call_kwargs.pop("extra_body", None)
            return updated_call_kwargs, True

        changed = UpstreamParamSelfHealController._remove_path_from_mapping(
            updated_call_kwargs,
            rule.path,
        )
        if not changed:
            return call_kwargs, False
        return updated_call_kwargs, True

    @staticmethod
    def _mapping_has_path(
        mapping: dict[str, Any],
        path: tuple[str, ...],
    ) -> bool:
        if not path:
            return False

        current: Any = mapping
        for segment in path:
            if not isinstance(current, dict):
                return False
            current_mapping = cast(dict[str, Any], current)
            if segment not in current_mapping:
                return False
            current = current_mapping[segment]
        return True

    @staticmethod
    def _find_exact_param_rules(
        call_kwargs: dict[str, Any],
        segments: tuple[str, ...],
    ) -> list[UnsupportedParamRule]:
        if not segments:
            return []

        rules: list[UnsupportedParamRule] = []
        extra_body_obj = call_kwargs.get("extra_body")
        extra_body = (
            cast(dict[str, Any], extra_body_obj)
            if isinstance(extra_body_obj, dict)
            else None
        )

        if segments[0] == "extra_body":
            nested_path = segments[1:]
            if (
                extra_body is not None
                and nested_path
                and UpstreamParamSelfHealController._mapping_has_path(
                    extra_body,
                    nested_path,
                )
            ):
                rules.append(
                    UnsupportedParamRule(location="extra_body", path=nested_path)
                )
            return rules

        if (
            segments[0] not in NON_RETRYABLE_INTERNAL_CALL_KWARGS
            and UpstreamParamSelfHealController._mapping_has_path(call_kwargs, segments)
        ):
            rules.append(UnsupportedParamRule(location="top_level", path=segments))

        if extra_body is not None and UpstreamParamSelfHealController._mapping_has_path(
            extra_body,
            segments,
        ):
            rules.append(UnsupportedParamRule(location="extra_body", path=segments))
        return rules

    @staticmethod
    def _find_inferred_nested_param_rules(
        call_kwargs: dict[str, Any],
        leaf_key: str,
    ) -> list[UnsupportedParamRule]:
        rules: list[UnsupportedParamRule] = []
        for key, value in call_kwargs.items():
            if key in NON_RETRYABLE_INTERNAL_CALL_KWARGS:
                continue
            if key == "extra_body":
                if not isinstance(value, dict):
                    continue
                extra_body = cast(dict[str, Any], value)
                for extra_key, extra_value in extra_body.items():
                    if not isinstance(extra_value, dict):
                        continue
                    nested_mapping = cast(dict[str, Any], extra_value)
                    if leaf_key in nested_mapping:
                        rules.append(
                            UnsupportedParamRule(
                                location="extra_body",
                                path=(extra_key, leaf_key),
                            )
                        )
                continue
            if not isinstance(value, dict):
                continue
            nested_mapping = cast(dict[str, Any], value)
            if leaf_key in nested_mapping:
                rules.append(
                    UnsupportedParamRule(
                        location="top_level",
                        path=(key, leaf_key),
                    )
                )
        return rules

    @staticmethod
    def _extract_param_hints(
        *,
        message: str | None,
        param: str | None,
    ) -> list[ParamHint]:
        hint_candidates: list[tuple[str, int, bool, int]] = []
        next_order = 0

        if param:
            normalized_param = param.strip()
            if normalized_param:
                hint_candidates.append((normalized_param, 1, False, next_order))
                next_order += 1

        if not message:
            return UpstreamParamSelfHealController._rank_param_hints(hint_candidates)

        patterns: tuple[tuple[re.Pattern[str], bool], ...] = (
            (
                re.compile(
                    r"(?:unknown|unsupported|unrecognized)\s+"
                    r"(?:parameter|field|argument)[^\"'`]*[\"'`]([A-Za-z0-9_.-]+)[\"'`]",
                    re.IGNORECASE,
                ),
                True,
            ),
            (
                re.compile(
                    r"[\"'`]([A-Za-z0-9_.-]+)[\"'`]\s+is\s+not\s+"
                    r"(?:supported|allowed)",
                    re.IGNORECASE,
                ),
                True,
            ),
            (
                re.compile(
                    r"invalid\s+(?:value|type)\s+for\s+[\"'`]([A-Za-z0-9_.-]+)[\"'`]",
                    re.IGNORECASE,
                ),
                False,
            ),
            (
                re.compile(
                    r"[\"'`]([A-Za-z0-9_.-]+)[\"'`]\s+must\b",
                    re.IGNORECASE,
                ),
                False,
            ),
        )

        for pattern, marks_unsupported in patterns:
            for matched_hint in pattern.findall(message):
                normalized_hint = matched_hint.strip()
                if not normalized_hint:
                    continue
                hint_candidates.append(
                    (normalized_hint, 0, marks_unsupported, next_order)
                )
                next_order += 1

        for listed_hint in extract_litellm_unsupported_params_from_message(message):
            hint_candidates.append((listed_hint, 0, True, next_order))
            next_order += 1
        return UpstreamParamSelfHealController._rank_param_hints(hint_candidates)

    @staticmethod
    def _rank_param_hints(
        hint_candidates: list[tuple[str, int, bool, int]],
    ) -> list[ParamHint]:
        ranked_candidates = sorted(
            hint_candidates,
            key=lambda item: (
                -len(UpstreamParamSelfHealController._split_hint_segments(item[0])),
                item[1],
                -len(item[0]),
                item[3],
            ),
        )

        ranked_hints: list[ParamHint] = []
        hint_index_by_value: dict[str, int] = {}
        for hint_value, _source_priority, unsupported, _order in ranked_candidates:
            existing_index = hint_index_by_value.get(hint_value)
            if existing_index is None:
                hint_index_by_value[hint_value] = len(ranked_hints)
                ranked_hints.append(
                    ParamHint(value=hint_value, unsupported=unsupported)
                )
                continue
            if unsupported and not ranked_hints[existing_index].unsupported:
                ranked_hints[existing_index] = ParamHint(
                    value=hint_value,
                    unsupported=True,
                )
        return ranked_hints

    @staticmethod
    def _build_auth_fingerprint(api_key: str) -> str:
        if not api_key:
            return ""
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    @staticmethod
    def _split_hint_segments(hint: str) -> tuple[str, ...]:
        return tuple(segment for segment in hint.split(".") if segment)

    @staticmethod
    def _select_rule_from_hint(
        *,
        hint: str,
        call_kwargs: dict[str, Any],
        unsupported_hint: bool,
    ) -> UnsupportedParamSelection | None:
        segments = UpstreamParamSelfHealController._split_hint_segments(hint)
        selection: UnsupportedParamSelection | None = None
        if not segments:
            return selection

        exact_rules = UpstreamParamSelfHealController._find_exact_param_rules(
            call_kwargs,
            segments,
        )
        if len(exact_rules) == 1:
            exact_rule = exact_rules[0]
            if unsupported_hint:
                selection = UnsupportedParamSelection(
                    rule=exact_rule,
                    cacheable=True,
                )
            else:
                selection = UnsupportedParamSelection(
                    rule=exact_rule,
                    cacheable=False,
                )
        elif len(segments) == 1:
            inferred_rules = UpstreamParamSelfHealController._find_inferred_nested_param_rules(
                call_kwargs,
                segments[0],
            )
            if len(inferred_rules) == 1:
                selection = UnsupportedParamSelection(
                    rule=inferred_rules[0],
                    cacheable=False,
                )
        return selection

    @staticmethod
    def _remove_path_from_mapping(
        mapping: dict[str, Any],
        path: tuple[str, ...],
    ) -> bool:
        if not path:
            return False

        key = path[0]
        if key not in mapping:
            return False

        if len(path) == 1:
            mapping.pop(key, None)
            return True

        child_obj = mapping.get(key)
        if not isinstance(child_obj, dict):
            return False
        child_mapping = dict(cast(dict[str, Any], child_obj))
        changed = UpstreamParamSelfHealController._remove_path_from_mapping(
            child_mapping,
            path[1:],
        )
        if not changed:
            return False

        if child_mapping:
            mapping[key] = child_mapping
        else:
            mapping.pop(key, None)
        return True


__all__ = [
    "TEMPORARY_SELF_HEAL_WARNING_PREFIX",
    "UnsupportedParamRule",
    "UnsupportedParamSelection",
    "UpstreamParamSelfHealController",
]
