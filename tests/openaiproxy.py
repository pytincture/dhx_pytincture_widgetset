"""Backend-for-frontend proxy for OpenAI-compatible chat APIs.

This module lives alongside the widget demo so the PyTincture packaging step
can detect the ``@backend_for_frontend`` decorator and auto-generate the Pyodide
stub that the frontend imports.  All network access happens server-side, so the
browser never deals with CORS or API keys.
"""

import os
from typing import Any

from openai import OpenAI

from pytincture.dataclass import backend_for_frontend, bff_stream


OPENAI_URL = os.getenv("OPENAI_SPEC_URL", "https://api.openai.com/v1/chat/completions")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
REQUEST_TIMEOUT = float(os.getenv("OPENAI_TIMEOUT", "60"))


def _infer_base_url(url: str) -> str:
    """Derive an OpenAI-compatible base URL from a chat completions endpoint."""

    if not url:
        return "https://api.openai.com/v1"

    suffixes = (
        "/chat/completions",
        "/v1/chat/completions",
    )
    for suffix in suffixes:
        if url.endswith(suffix):
            return url[: -len(suffix)] or url
    return url


@backend_for_frontend
class openaiproxy:
    """Thin proxy that fans requests out to an OpenAI Responses-compatible API."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "sk-")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is required for OpenAIProxy")

        base_url = os.getenv("OPENAI_BASE_URL") or _infer_base_url(OPENAI_URL)
        # Use per-instance client so the backend can reuse connection pooling.
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._client_timeout = REQUEST_TIMEOUT

    @bff_stream()
    def chat_stream(self, messages, model=None, **extra: Any):
        options = extra.copy()
        timeout_override = options.pop("timeout", None)
        options.pop("stream", None)
        timeout = timeout_override or self._client_timeout

        with self._client.chat.completions.stream(
            model=model or DEFAULT_MODEL,
            messages=messages,
            **options,
            timeout=timeout,
        ) as stream:
            for chunk in stream:
                # Convert the chunk to plain JSON so the frontend BFF machinery can forward it.
                yield chunk.model_dump(exclude_none=True)
