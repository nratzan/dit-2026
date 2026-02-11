"""OpenAI provider using the Responses API — supports multiple models."""
import os
import time
from llm.base import LLMProvider, LLMResponse
from llm.models import get_model_info

DEFAULT_MODEL = "gpt-5.2"


class OpenAIProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "openai"

    @property
    def default_model(self) -> str:
        return DEFAULT_MODEL

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI()
        return self._client

    def generate(self, system_prompt: str, messages: list,
                 model: str | None = None,
                 reasoning_config: dict | None = None) -> LLMResponse:
        client = self._get_client()
        model_id = model or DEFAULT_MODEL
        info = get_model_info(model_id)

        # Build Responses API input format
        api_input = [
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
        ]
        for msg in messages:
            api_input.append({
                "role": msg["role"],
                "content": [{"type": "input_text", "text": msg["content"]}],
            })

        # Build kwargs
        kwargs = {
            "model": model_id,
            "input": api_input,
            "max_output_tokens": 2000,
        }

        # Add reasoning if this model supports it
        if info and info.get("reasoning_param") == "effort":
            effort = "high"  # default
            if reasoning_config and "effort" in reasoning_config:
                effort = reasoning_config["effort"]
            if effort != "none":
                kwargs["reasoning"] = {"effort": effort}

        start = time.perf_counter()
        resp = client.responses.create(**kwargs)
        latency = (time.perf_counter() - start) * 1000

        # Extract text — try output_text first, then walk blocks
        text = ""
        if getattr(resp, 'output_text', None):
            text = resp.output_text.strip()
        else:
            for block in getattr(resp, 'output', []) or []:
                content = getattr(block, 'content', None)
                if not content:
                    continue
                for item in content:
                    t = getattr(item, 'text', None)
                    if t:
                        text = t.strip()

        # Extract usage if available
        input_tokens = None
        output_tokens = None
        if hasattr(resp, 'usage') and resp.usage:
            input_tokens = getattr(resp.usage, 'input_tokens', None)
            output_tokens = getattr(resp.usage, 'output_tokens', None)

        return LLMResponse(
            text=text,
            provider="openai",
            model=model_id,
            latency_ms=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    def is_available(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))
