"""Evaluation metrics for LLM provider comparison on DIT framework Q&A."""


def theme_coverage_score(response_text: str, expected_themes: list) -> float:
    """Fraction of expected themes mentioned in response (case-insensitive).

    Args:
        response_text: LLM response text
        expected_themes: List of expected keywords/phrases

    Returns:
        Score between 0.0 and 1.0
    """
    if not expected_themes:
        return 0.0
    response_lower = response_text.lower()
    hits = sum(1 for theme in expected_themes if theme.lower() in response_lower)
    return hits / len(expected_themes)


def estimate_cost(provider: str, input_tokens: int = None, output_tokens: int = None) -> float:
    """Estimate cost in USD based on provider pricing (approximate, early 2026).

    Args:
        provider: Provider name ('openai', 'anthropic', 'google', 'ollama')
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in USD
    """
    PRICING = {
        "openai": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},     # gpt-5.1
        "anthropic": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},   # claude-sonnet-4
        "google": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},       # gemini-2.5-flash
        "ollama": {"input": 0.0, "output": 0.0},                                  # local
    }
    rates = PRICING.get(provider, {"input": 0.0, "output": 0.0})
    return (input_tokens or 0) * rates["input"] + (output_tokens or 0) * rates["output"]


def response_length_score(response_text: str, min_words: int = 50, max_words: int = 500) -> float:
    """Score response length — penalize too short or too long responses.

    Returns 1.0 for responses within the ideal range, scaled down otherwise.
    """
    word_count = len(response_text.split())
    if word_count < min_words:
        return word_count / min_words
    elif word_count > max_words:
        return max(0.5, max_words / word_count)
    return 1.0
