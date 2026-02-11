"""Token usage tracking with daily budget limits.

Uses Firestore when available, falls back to in-memory tracking.
"""

import os
from datetime import datetime, timezone

# Daily budget in tokens (input + output combined). Default ~500K tokens.
DAILY_TOKEN_BUDGET = int(os.environ.get("DAILY_TOKEN_BUDGET", "500000"))

# In-memory fallback
_daily_usage: dict[str, dict] = {}  # {"2026-02-11": {"tokens": N, "requests": N}}


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _firestore_enabled() -> bool:
    return os.environ.get("FIRESTORE_ENABLED", "").lower() in ("1", "true")


def _get_db():
    if not _firestore_enabled():
        return None
    try:
        from storage import _get_client
        return _get_client()
    except Exception:
        return None


def record_usage(input_tokens: int, output_tokens: int) -> dict:
    """Record token usage for a request. Returns usage summary."""
    total = (input_tokens or 0) + (output_tokens or 0)
    today = _today()

    db = _get_db()
    if db:
        try:
            from google.cloud.firestore_v1 import transforms
            doc_ref = db.collection("usage_daily").document(today)
            doc_ref.set({
                "total_tokens": transforms.Increment(total),
                "request_count": transforms.Increment(1),
                "date": today,
            }, merge=True)
        except Exception:
            pass

    # Always update in-memory too (used as fallback and for immediate reads)
    if today not in _daily_usage:
        _daily_usage[today] = {"tokens": 0, "requests": 0}
    _daily_usage[today]["tokens"] += total
    _daily_usage[today]["requests"] += 1

    return get_usage_stats()


def check_budget() -> bool:
    """Return True if under daily budget."""
    today = _today()

    db = _get_db()
    if db:
        try:
            doc = db.collection("usage_daily").document(today).get()
            if doc.exists:
                return doc.to_dict().get("total_tokens", 0) < DAILY_TOKEN_BUDGET
            return True
        except Exception:
            pass

    return _daily_usage.get(today, {}).get("tokens", 0) < DAILY_TOKEN_BUDGET


def get_usage_stats() -> dict:
    """Return current usage stats."""
    today = _today()
    tokens_used = 0
    requests = 0

    db = _get_db()
    if db:
        try:
            doc = db.collection("usage_daily").document(today).get()
            if doc.exists:
                data = doc.to_dict()
                tokens_used = data.get("total_tokens", 0)
                requests = data.get("request_count", 0)
                return {
                    "date": today,
                    "tokens_used": tokens_used,
                    "requests": requests,
                    "budget": DAILY_TOKEN_BUDGET,
                    "remaining": max(0, DAILY_TOKEN_BUDGET - tokens_used),
                }
        except Exception:
            pass

    mem = _daily_usage.get(today, {})
    tokens_used = mem.get("tokens", 0)
    requests = mem.get("requests", 0)
    return {
        "date": today,
        "tokens_used": tokens_used,
        "requests": requests,
        "budget": DAILY_TOKEN_BUDGET,
        "remaining": max(0, DAILY_TOKEN_BUDGET - tokens_used),
    }
