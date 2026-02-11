"""Google Gemini provider — supports multiple models + thinking config."""
import os
import time
from llm.base import LLMProvider, LLMResponse
from llm.models import get_model_info

DEFAULT_MODEL = "gemini-2.5-flash"


class GoogleProvider(LLMProvider):

    @property
    def name(self) -> str:
        return "google"

    @property
    def default_model(self) -> str:
        return DEFAULT_MODEL

    def generate(self, system_prompt: str, messages: list,
                 model: str | None = None,
                 reasoning_config: dict | None = None) -> LLMResponse:
        import google.generativeai as genai
        from google.generativeai import types

        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model_id = model or DEFAULT_MODEL
        info = get_model_info(model_id)

        # Build generation config with thinking params
        gen_config_kwargs = {}
        if info and reasoning_config:
            param_type = info.get("reasoning_param")
            if param_type == "thinking_budget" and "thinking_budget" in reasoning_config:
                budget = int(reasoning_config["thinking_budget"])
                gen_config_kwargs["thinking_config"] = types.ThinkingConfig(
                    thinking_budget=budget
                )
            elif param_type == "thinking_level" and "thinking_level" in reasoning_config:
                level = reasoning_config["thinking_level"]
                gen_config_kwargs["thinking_config"] = types.ThinkingConfig(
                    thinking_level=level.upper()
                )

        gen_model = genai.GenerativeModel(
            model_id,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(**gen_config_kwargs) if gen_config_kwargs else None,
        )

        # Convert message history to Gemini format
        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = gen_model.start_chat(history=history)

        start = time.perf_counter()
        response = chat.send_message(messages[-1]["content"])
        latency = (time.perf_counter() - start) * 1000

        return LLMResponse(
            text=response.text,
            provider="google",
            model=model_id,
            latency_ms=latency,
        )

    def is_available(self) -> bool:
        return bool(os.environ.get("GOOGLE_API_KEY"))
