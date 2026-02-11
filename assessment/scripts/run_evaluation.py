"""Run the DIT framework evaluation harness.

Usage:
    cd prototypes/dit-assessment
    python scripts/run_evaluation.py
    python scripts/run_evaluation.py --providers openai anthropic
    python scripts/run_evaluation.py --runs 3
    python scripts/run_evaluation.py --output evaluation_report.json
"""
import argparse
import json
import sys
from pathlib import Path

# Add package root to path
pkg_root = Path(__file__).parent.parent
sys.path.insert(0, str(pkg_root))

from dotenv import load_dotenv
load_dotenv(pkg_root / ".env")


def main():
    parser = argparse.ArgumentParser(description="DIT Framework LLM Evaluation Harness")
    parser.add_argument("--providers", nargs="+", help="Provider names to evaluate (default: all available)")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs per question (default: 1)")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file path")
    args = parser.parse_args()

    # Initialize components
    from embeddings.search import SearchEngine
    from llm import create_provider_registry
    from evaluation.harness import EvaluationHarness

    print("Initializing search engine...")
    search_engine = SearchEngine()

    print("Initializing LLM providers...")
    registry = create_provider_registry()

    available = [p for p in registry.get_available_providers() if p["available"]]
    print(f"Available providers: {[p['name'] for p in available]}")

    if not available:
        print("ERROR: No LLM providers available. Set API keys in .env")
        sys.exit(1)

    # Run evaluation
    harness = EvaluationHarness(registry, search_engine)
    report = harness.run(providers=args.providers, num_runs=args.runs)

    # Print summary
    harness.print_summary(report)

    # Save report
    output_path = args.output or f"evaluation_report_{report['timestamp'][:10]}.json"
    output_path = pkg_root / output_path
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nFull report saved to: {output_path}")


if __name__ == "__main__":
    main()
