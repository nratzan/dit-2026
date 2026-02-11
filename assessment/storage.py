"""Firestore storage for anonymous assessment results."""

import os
from datetime import datetime, timezone


def _is_enabled():
    return os.environ.get("FIRESTORE_ENABLED", "").lower() in ("1", "true")


COLLECTION = "assessment_results"

_client = None


def _get_client():
    global _client
    if _client is None:
        from google.cloud import firestore
        _client = firestore.Client()
    return _client


def store_result(sae_level: int, epias_stage: str) -> None:
    """Store a single anonymous assessment result."""
    if not _is_enabled():
        return
    from google.cloud import firestore as fs
    db = _get_client()
    db.collection(COLLECTION).add({
        "sae_level": sae_level,
        "epias_stage": epias_stage,
        "cell_key": f"{sae_level}_{epias_stage}",
        "timestamp": fs.SERVER_TIMESTAMP,
        "app_version": "1.0",
    })


def get_heatmap_data() -> dict:
    """Aggregate all results into a 6x5 count grid."""
    counts = {}
    for level in range(6):
        for stage in ["E", "P", "I", "A", "S"]:
            counts[f"{level}_{stage}"] = 0

    total = 0

    if _is_enabled():
        db = _get_client()
        docs = db.collection(COLLECTION).select(["cell_key"]).stream()
        for doc in docs:
            key = doc.to_dict().get("cell_key")
            if key in counts:
                counts[key] += 1
                total += 1

    return {
        "counts": counts,
        "total": total,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
