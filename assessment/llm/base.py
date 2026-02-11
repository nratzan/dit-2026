"""Abstract LLM provider interface."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMResponse:
    """Response from an LLM provider."""
    text: str
    provider: str
    model: str
    latency_ms: float
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_estimate_usd: Optional[float] = None


class LLMProvider(ABC):
    """Abstract base for LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'openai', 'anthropic')."""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model ID for this provider."""
        ...

    @abstractmethod
    def generate(self, system_prompt: str, messages: list,
                 model: str | None = None,
                 reasoning_config: dict | None = None) -> LLMResponse:
        """Generate a response.

        Args:
            system_prompt: System-level instructions with RAG context
            messages: Conversation history [{"role": "user"|"assistant", "content": "..."}]
            model: Override model ID (or use default)
            reasoning_config: Provider-specific reasoning/thinking settings

        Returns:
            LLMResponse with text and metadata
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is configured and available."""
        ...
