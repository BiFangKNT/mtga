from __future__ import annotations

from typing import Any


class VertexGeminiConfig:
    @staticmethod
    def _check_prompt_level_content_filter(
        processed_chunk: Any,
        response_id: Any,
    ) -> Any:
        del response_id
        return processed_chunk

    def _transform_google_generate_content_to_openai_model_response(
        self,
        completion_response: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        del args, kwargs
        return completion_response


__all__ = ["VertexGeminiConfig"]
