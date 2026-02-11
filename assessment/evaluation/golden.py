"""Golden test questions with expected answer themes for DIT framework evaluation."""

GOLDEN_QUESTIONS = [
    {
        "id": "g01",
        "question": "What SAE level am I at if I use ChatGPT to brainstorm design ideas but rewrite everything?",
        "expected_level": "L1",
        "expected_themes": ["SAE L1", "AI-Assisted", "human drives", "suggest", "direct each step", "rewrite"],
        "category": "level_identification",
    },
    {
        "id": "g02",
        "question": "What's the difference between an Explorer and a Practitioner at L2?",
        "expected_themes": ["Explorer", "Practitioner", "trying", "repeatable", "consistent", "definition of done", "rework"],
        "category": "epias_distinction",
    },
    {
        "id": "g03",
        "question": "I use Bolt.new to generate React components from specs. Am I at L2 or L3?",
        "expected_level": "L2",
        "expected_themes": ["L2", "app-builders", "bounded chunks", "screens", "components", "Bolt"],
        "category": "level_identification",
    },
    {
        "id": "g04",
        "question": "What does it mean to be a Steward at L1?",
        "expected_themes": ["Steward", "L1", "standards", "team", "governs", "mentor", "judgment", "review"],
        "category": "role_description",
    },
    {
        "id": "g05",
        "question": "How do I transition from L2 to L3?",
        "expected_themes": ["screens", "runs", "IDE", "multi-step", "context engineering", "checkpoints", "workflow"],
        "category": "transition_guidance",
    },
    {
        "id": "g06",
        "question": "Is a Steward at L1 more mature than an Explorer at L4?",
        "expected_themes": ["yes", "depth", "judgment", "breadth", "tooling", "more valuable", "more mature"],
        "category": "framework_principles",
    },
    {
        "id": "g07",
        "question": "What's the key difference between L3 and L4?",
        "expected_themes": ["close laptop", "stops", "continues", "away", "exceptions", "harness", "IDE"],
        "category": "level_distinction",
    },
    {
        "id": "g08",
        "question": "What concrete things should I do to move from L3 Practitioner to L3 Integrator?",
        "expected_themes": ["decision framing", "failure mode", "escalation", "approval", "eval", "ownership"],
        "category": "growth_actions",
    },
    {
        "id": "g09",
        "question": "What tools do designers typically use at L3?",
        "expected_themes": ["VS Code", "Cursor", "IDE", "Copilot", "LangChain", "MCP", "workflow"],
        "category": "tooling",
    },
    {
        "id": "g10",
        "question": "Should I skip L2 and jump straight to L3?",
        "expected_themes": ["judgment", "deeper", "carry forward", "don't race", "reliability", "L2"],
        "category": "framework_principles",
    },
]
