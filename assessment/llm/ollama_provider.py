"""Ollama local model provider."""
import time
import requests
from llm.base import LLMProvider, LLMResponse


class OllamaProvider(LLMProvider):

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self._base_url = base_url
        self._model = model

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def default_model(self) -> str:
        return self._model

    def generate(self, system_prompt: str, messages: list,
                 model: str | None = None,
                 reasoning_config: dict | None = None) -> LLMResponse:
        use_model = model or self._model
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages)

        start = time.perf_counter()
        resp = requests.post(
            f"{self._base_url}/api/chat",
            json={"model": use_model, "messages": api_messages, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        latency = (time.perf_counter() - start) * 1000

        return LLMResponse(
            text=data["message"]["content"],
            provider="ollama",
            model=use_model,
            latency_ms=latency,
        )

    def is_available(self) -> bool:
        try:
            resp = requests.get(f"{self._base_url}/api/tags", timeout=2)
            return resp.status_code == 200
        except Exception:
            return False
