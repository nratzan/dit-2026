"""Test harness: run golden questions against all available LLM providers."""
import json
from datetime import datetime
from pathlib import Path

from evaluation.golden import GOLDEN_QUESTIONS
from evaluation.metrics import theme_coverage_score, estimate_cost, response_length_score


class EvaluationHarness:
    """Run golden questions against LLM providers and produce comparison report."""

    def __init__(self, registry, search_engine):
        """
        Args:
            registry: ProviderRegistry instance
            search_engine: SearchEngine instance for RAG context
        """
        self.registry = registry
        self.search_engine = search_engine

    def run(self, providers: list = None, num_runs: int = 1) -> dict:
        """Run all golden questions against specified (or all available) providers.

        Args:
            providers: List of provider names, or None for all available
            num_runs: Number of times to run each question (for consistency)

        Returns:
            Evaluation report dict
        """
        if providers is None:
            providers = [
                p["name"]
                for p in self.registry.get_available_providers()
                if p["available"]
            ]

        if not providers:
            return {"error": "No providers available", "providers": []}

        results = []

        for provider_name in providers:
            print(f"\n--- Evaluating: {provider_name} ---")
            provider = self.registry.get_provider(provider_name)
            provider_results = []

            for qi, question in enumerate(GOLDEN_QUESTIONS):
                print(f"  [{qi+1}/{len(GOLDEN_QUESTIONS)}] {question['id']}: {question['question'][:60]}...")
                run_results = []

                for run_idx in range(num_runs):
                    # Retrieve RAG context
                    chunks = self.search_engine.search(question["question"], top_k=5)
                    context = "\n\n---\n\n".join(c["text"] for c in chunks)

                    system_prompt = (
                        "You are an expert on the Design in Tech Report 2026 "
                        "E-P-I-A-S x SAE Framework by John Maeda. "
                        "Answer based on the framework content below. "
                        "Be specific and cite SAE levels and EPIAS stages.\n\n"
                        f"FRAMEWORK CONTEXT:\n{context}"
                    )

                    try:
                        response = provider.generate(
                            system_prompt=system_prompt,
                            messages=[{"role": "user", "content": question["question"]}],
                        )

                        coverage = theme_coverage_score(
                            response.text, question["expected_themes"]
                        )
                        length = response_length_score(response.text)
                        cost = estimate_cost(
                            provider_name, response.input_tokens, response.output_tokens
                        )

                        run_results.append({
                            "run": run_idx,
                            "response_preview": response.text[:500],
                            "theme_coverage": round(coverage, 3),
                            "length_score": round(length, 3),
                            "latency_ms": round(response.latency_ms, 1),
                            "cost_usd": round(cost, 6),
                            "input_tokens": response.input_tokens,
                            "output_tokens": response.output_tokens,
                            "error": None,
                        })

                    except Exception as e:
                        print(f"    ERROR: {e}")
                        run_results.append({
                            "run": run_idx,
                            "response_preview": "",
                            "theme_coverage": 0.0,
                            "length_score": 0.0,
                            "latency_ms": 0,
                            "cost_usd": 0,
                            "error": str(e),
                        })

                # Aggregate across runs
                successful = [r for r in run_results if not r["error"]]
                if successful:
                    coverages = [r["theme_coverage"] for r in successful]
                    avg_coverage = sum(coverages) / len(coverages)
                    consistency = 1.0 - (max(coverages) - min(coverages)) if len(coverages) > 1 else 1.0
                    avg_latency = sum(r["latency_ms"] for r in successful) / len(successful)
                    total_cost = sum(r["cost_usd"] for r in run_results)
                else:
                    avg_coverage = 0.0
                    consistency = 0.0
                    avg_latency = 0.0
                    total_cost = 0.0

                provider_results.append({
                    "question_id": question["id"],
                    "question": question["question"],
                    "category": question["category"],
                    "runs": run_results,
                    "avg_theme_coverage": round(avg_coverage, 3),
                    "avg_latency_ms": round(avg_latency, 1),
                    "total_cost_usd": round(total_cost, 6),
                    "consistency": round(consistency, 3),
                    "errors": sum(1 for r in run_results if r["error"]),
                })

            # Provider summary
            n = len(provider_results)
            results.append({
                "provider": provider_name,
                "model": provider.model_name,
                "questions": provider_results,
                "summary": {
                    "avg_theme_coverage": round(sum(q["avg_theme_coverage"] for q in provider_results) / n, 3),
                    "avg_latency_ms": round(sum(q["avg_latency_ms"] for q in provider_results) / n, 1),
                    "total_cost_usd": round(sum(q["total_cost_usd"] for q in provider_results), 6),
                    "avg_consistency": round(sum(q["consistency"] for q in provider_results) / n, 3),
                    "total_errors": sum(q["errors"] for q in provider_results),
                },
            })

        report = {
            "timestamp": datetime.now().isoformat(),
            "num_runs": num_runs,
            "num_questions": len(GOLDEN_QUESTIONS),
            "providers": results,
        }

        return report

    @staticmethod
    def print_summary(report: dict):
        """Print a human-readable summary of the evaluation report."""
        print("\n" + "=" * 70)
        print("DIT Framework Evaluation Report")
        print(f"Time: {report['timestamp']}")
        print(f"Questions: {report['num_questions']} | Runs per question: {report['num_runs']}")
        print("=" * 70)

        for p in report.get("providers", []):
            s = p["summary"]
            print(f"\n  {p['provider'].upper()} ({p['model']})")
            print(f"    Theme Coverage: {s['avg_theme_coverage']:.1%}")
            print(f"    Avg Latency:    {s['avg_latency_ms']:.0f}ms")
            print(f"    Total Cost:     ${s['total_cost_usd']:.4f}")
            print(f"    Consistency:    {s['avg_consistency']:.1%}")
            print(f"    Errors:         {s['total_errors']}")

        print("\n" + "=" * 70)
