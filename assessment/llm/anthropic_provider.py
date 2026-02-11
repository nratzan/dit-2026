"""Anthropic Claude provider — supports multiple models + extended thinking."""
import os
import time
from llm.base import LLMProvider, LLMResponse

DEFAULT_MODEL = "claude-sonnet-4-5"


class AnthropicProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def default_model(self) -> str:
        return DEFAULT_MODEL

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    def generate(self, system_prompt: str, messages: list,
                 model: str | None = None,
                 reasoning_config: dict | None = None) -> LLMResponse:
        client = self._get_client()
        model_id = model or DEFAULT_MODEL

        kwargs = {
            "model": model_id,
            "max_tokens": 2000,
            "system": system_prompt,
            "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        }

        # Extended thinking support
        budget = None
        if reasoning_config and "thinking" in reasoning_config:
            val = reasoning_config["thinking"]
            if val != "off":
                budget = int(val)

        if budget and budget >= 1024:
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": budget}
            # Increase max_tokens to accommodate thinking + response
            kwargs["max_tokens"] = max(kwargs["max_tokens"], budget + 4000)

        start = time.perf_counter()
        resp = client.messages.create(**kwargs)
        latency = (time.perf_counter() - start) * 1000

        # Extract text — skip thinking blocks, find the text block
        text = ""
        for block in resp.content:
            if getattr(block, 'type', None) == 'text':
                text = block.text
                break

        return LLMResponse(
            text=text,
            provider="anthropic",
            model=model_id,
            latency_ms=latency,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
        )

    def is_available(self) -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
