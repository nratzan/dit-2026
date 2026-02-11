"""Score assessment answers into SAE level and EPIAS stage."""
from assessment.questions import SAE_QUESTIONS, EPIAS_QUESTIONS


STAGE_TO_NUM = {"E": 1, "P": 2, "I": 3, "A": 4, "S": 5}
NUM_TO_STAGE = {1: "E", 2: "P", 3: "I", 4: "A", 5: "S"}
STAGE_NAMES = {
    "E": "Explorer", "P": "Practitioner", "I": "Integrator",
    "A": "Architect", "S": "Steward",
}
SAE_NAMES = {
    0: "Manual", 1: "AI-Assisted", 2: "Partially Automated",
    3: "Guided Automation", 4: "Mostly Automated", 5: "Full Automation",
}
SAE_EMOJIS = {
    0: "\U0001f697\U0001f4a8", 1: "\U0001f697\u2795", 2: "\U0001f697\U0001f9e0",
    3: "\U0001f697\U0001f634", 4: "\U0001f695\U0001f916", 5: "\U0001f697\u2728",
}


def score_assessment(answers: dict) -> dict:
    """Score user answers into SAE level and EPIAS stage.

    Args:
        answers: {
            "sae_tools": 2, "sae_qa": 1, ...  (SAE question id -> selected level int)
            "epias_l1_consistency": "P", ...     (EPIAS question id -> selected stage letter)
        }

    Returns:
        Dict with sae_level, epias_stage, and supporting data.
    """
    # 1. SAE Level: median of selected levels
    sae_values = []
    for q in SAE_QUESTIONS:
        val = answers.get(q["id"])
        if val is not None:
            sae_values.append(int(val))

    if not sae_values:
        sae_level = 1  # Default
    else:
        sorted_vals = sorted(sae_values)
        sae_level = sorted_vals[len(sorted_vals) // 2]

    # Clamp to valid range
    sae_level = max(0, min(5, sae_level))

    # 2. EPIAS Stage: median of selected stages within the identified SAE level
    epias_values = []
    level_questions = EPIAS_QUESTIONS.get(sae_level, [])
    for q in level_questions:
        val = answers.get(q["id"])
        if val is not None and val in STAGE_TO_NUM:
            epias_values.append(STAGE_TO_NUM[val])

    if not epias_values:
        epias_numeric = 1  # Default to Explorer
    else:
        sorted_vals = sorted(epias_values)
        epias_numeric = sorted_vals[len(sorted_vals) // 2]

    epias_stage = NUM_TO_STAGE[epias_numeric]

    return {
        "sae_level": sae_level,
        "sae_name": SAE_NAMES[sae_level],
        "sae_emoji": SAE_EMOJIS[sae_level],
        "epias_stage": epias_stage,
        "epias_name": STAGE_NAMES[epias_stage],
        "sae_distribution": {q["id"]: answers.get(q["id"]) for q in SAE_QUESTIONS},
        "epias_distribution": {q["id"]: answers.get(q["id"]) for q in level_questions},
    }
