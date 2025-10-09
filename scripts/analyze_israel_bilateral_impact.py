#!/usr/bin/env python3
"""
Israel Bilateral Relationship Impact Analysis

Analyzes how the Gaza ceasefire resolution affects Israel's bilateral relationships
with each UN member state, categorizing the impact and providing reasoning.

Usage:
    python scripts/analyze_israel_bilateral_impact.py <motion_id> [--sample N]

Example:
    python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --sample 5
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class BilateralImpactAnalyzer:
    """Analyzes bilateral relationship impacts from UN voting results"""

    # Impact categories
    IMPACT_CATEGORIES = [
        "strengthened_significantly",  # Major improvement in relations
        "strengthened_moderately",     # Noticeable improvement
        "strengthened_slightly",       # Minor improvement
        "neutral",                     # No meaningful change
        "strained_slightly",           # Minor tension
        "strained_moderately",         # Noticeable tension
        "strained_significantly"       # Major deterioration
    ]

    def __init__(self, model: str = "claude-3-5-haiku-20241022"):
        """
        Initialize the analyzer with a fast model for efficiency

        Args:
            model: Model name (default: claude-3-5-haiku for speed)
        """
        self.model = model
        self.project_root = PROJECT_ROOT
        self.reactions_dir = self.project_root / "tasks" / "reactions"
        self.results_dir = self.project_root / "tasks" / "analysis"

        # Load configuration
        self._load_config()
        self._init_ai_client()

    def _load_config(self):
        """Load configuration from environment variables"""
        from dotenv import load_dotenv
        load_dotenv()

        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

    def _init_ai_client(self):
        """Initialize Anthropic AI client"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            print(f"✓ Initialized Anthropic API client (model: {self.model})")
        except ImportError:
            print("Error: anthropic package not installed. Run: pip install anthropic")
            sys.exit(1)

    def load_voting_results(self, motion_id: str) -> Dict:
        """Load the latest voting results for a motion"""
        results_file = self.reactions_dir / f"{motion_id}_latest.json"

        if not results_file.exists():
            raise FileNotFoundError(
                f"No voting results found for {motion_id}. "
                f"Run the motion simulation first."
            )

        with open(results_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def analyze_bilateral_impact(self, country_vote: Dict, motion_context: str) -> Dict:
        """
        Analyze how a country's vote affects its bilateral relationship with Israel

        Args:
            country_vote: Dict with country name, vote, and statement
            motion_context: Context about the motion being voted on

        Returns:
            Dict with impact category, reasoning, and confidence
        """

        system_prompt = """You are an expert international relations analyst specializing in Middle East diplomacy and bilateral relationships.

Your task is to analyze how a country's vote on a UN resolution affects its bilateral relationship with Israel. Consider:
- Historical relationship baseline
- Vote alignment or divergence
- Diplomatic tone in statement
- Strategic implications
- Regional dynamics
- Economic/security ties

Be objective and nuanced. Not all "yes" votes strengthen relations equally, and not all "no" votes strain them equally."""

        user_prompt = f"""Analyze how this country's vote affects its bilateral relationship with Israel:

**Motion Context:** {motion_context}

**Country:** {country_vote['country']}
**Vote:** {country_vote['vote'].upper()}
**Statement:** {country_vote['statement']}

Based on this vote and statement, categorize the impact on Israel-{country_vote['country']} bilateral relations.

You must respond with a JSON object containing:
1. "impact_category": Must be exactly one of: {', '.join(self.IMPACT_CATEGORIES)}
2. "reasoning": 2-3 sentences explaining your assessment
3. "confidence": Your confidence level (high/medium/low)
4. "key_factors": Array of 2-4 key factors driving this assessment

Consider:
- Does this vote strengthen or strain the relationship compared to baseline?
- How significant is the impact (slightly/moderately/significantly)?
- What does the statement's tone reveal about the relationship?
- Are there strategic, economic, or security dimensions?

Your response must be valid JSON in this exact format:
{{
  "impact_category": "neutral",
  "reasoning": "Your analysis here.",
  "confidence": "high",
  "key_factors": ["factor 1", "factor 2", "factor 3"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=600,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5
            )
            content = response.content[0].text.strip()

            # Extract JSON from response (handle markdown code blocks and extra text)
            if content.startswith("```"):
                content = re.sub(r'^```(?:json)?\n', '', content)
                content = re.sub(r'\n```$', '', content)

            # Find JSON object boundaries
            start_idx = content.find('{')
            if start_idx == -1:
                raise ValueError("No JSON object found in response")

            # Find matching closing brace
            brace_count = 0
            end_idx = start_idx
            for i in range(start_idx, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break

            json_str = content[start_idx:end_idx]

            # Parse JSON response
            result = json.loads(json_str)

            # Validate response
            required_fields = ["impact_category", "reasoning", "confidence", "key_factors"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Response missing required field: {field}")

            if result["impact_category"] not in self.IMPACT_CATEGORIES:
                raise ValueError(f"Invalid impact category: {result['impact_category']}")

            return result

        except json.JSONDecodeError as e:
            print(f"  ⚠ JSON parse error for {country_vote['country']}: {e}")
            return {
                "impact_category": "neutral",
                "reasoning": "[Error: Unable to parse response]",
                "confidence": "low",
                "key_factors": ["analysis_error"],
                "error": str(e)
            }
        except Exception as e:
            print(f"  ⚠ Error analyzing {country_vote['country']}: {e}")
            return {
                "impact_category": "neutral",
                "reasoning": f"[Error: {str(e)}]",
                "confidence": "low",
                "key_factors": ["analysis_error"],
                "error": str(e)
            }

    def run_analysis(self, motion_id: str, sample_size: Optional[int] = None) -> Dict:
        """
        Run bilateral impact analysis for all countries

        Args:
            motion_id: ID of the motion to analyze
            sample_size: If set, only analyze this many countries (for testing)

        Returns:
            Dict containing all analyses and summary statistics
        """
        print(f"\n{'='*70}")
        print(f"Israel Bilateral Relationship Impact Analysis")
        print(f"Motion: {motion_id}")
        print(f"Model: {self.model}")
        print(f"{'='*70}\n")

        # Load voting results
        voting_results = self.load_voting_results(motion_id)
        print(f"✓ Loaded voting results: {voting_results['total_votes']} countries\n")

        # Extract motion context (first 500 chars of motion text for context)
        motion_context = f"Gaza ceasefire resolution - Vote summary: {voting_results['vote_summary']}"

        # Get votes to analyze
        votes = voting_results['votes']
        if sample_size:
            votes = votes[:sample_size]
            print(f"📊 Analyzing {sample_size} countries (sample mode)\n")
        else:
            print(f"📊 Analyzing {len(votes)} countries\n")

        # Analyze each country's impact
        analyses = []
        impact_counts = {cat: 0 for cat in self.IMPACT_CATEGORIES}

        for i, vote in enumerate(votes, 1):
            # Skip Israel itself
            if vote['country'].lower() == 'israel':
                print(f"[{i}/{len(votes)}] Skipping Israel (self)...")
                continue

            print(f"[{i}/{len(votes)}] Analyzing {vote['country']}...", end=" ", flush=True)

            impact_analysis = self.analyze_bilateral_impact(vote, motion_context)

            impact_counts[impact_analysis["impact_category"]] += 1

            analyses.append({
                "country": vote['country'],
                "vote": vote['vote'],
                "statement": vote['statement'],
                "impact_analysis": impact_analysis
            })

            # Print impact result with emoji
            impact_emoji = {
                "strengthened_significantly": "💚",
                "strengthened_moderately": "🟢",
                "strengthened_slightly": "🟡",
                "neutral": "⚪",
                "strained_slightly": "🟠",
                "strained_moderately": "🔴",
                "strained_significantly": "🔥"
            }
            emoji = impact_emoji.get(impact_analysis["impact_category"], "❓")
            print(f"{emoji} {impact_analysis['impact_category']}")

        # Compile results
        results = {
            "motion_id": motion_id,
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "total_analyzed": len(analyses),
            "impact_summary": impact_counts,
            "analyses": analyses,
            "metadata": {
                "voting_summary": voting_results['vote_summary'],
                "original_votes": voting_results['total_votes']
            }
        }

        # Print summary
        print(f"\n{'='*70}")
        print(f"Impact Summary:")
        total = len(analyses)
        for category in self.IMPACT_CATEGORIES:
            count = impact_counts[category]
            pct = (count/total*100) if total > 0 else 0
            print(f"  {category:30s}: {count:3d} ({pct:5.1f}%)")
        print(f"{'='*70}\n")

        return results

    def save_results(self, results: Dict):
        """Save analysis results to file"""
        # Create results directory if it doesn't exist
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{results['motion_id']}_israel_bilateral_impact_{timestamp}.json"
        filepath = self.results_dir / filename

        # Save results
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✓ Results saved to: {filepath}")

        # Also create/update a "latest" version
        latest_filepath = self.results_dir / f"{results['motion_id']}_israel_bilateral_impact_latest.json"
        with open(latest_filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✓ Latest results: {latest_filepath}")

        # Generate CSV export for easy analysis
        self._export_csv(results, self.results_dir / f"{results['motion_id']}_israel_bilateral_impact.csv")

    def _export_csv(self, results: Dict, filepath: Path):
        """Export results to CSV format"""
        import csv

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "Country",
                "Vote",
                "Impact Category",
                "Confidence",
                "Reasoning",
                "Key Factors"
            ])

            # Data rows
            for analysis in results['analyses']:
                impact = analysis['impact_analysis']
                writer.writerow([
                    analysis['country'],
                    analysis['vote'],
                    impact['impact_category'],
                    impact['confidence'],
                    impact['reasoning'],
                    '; '.join(impact['key_factors'])
                ])

        print(f"✓ CSV export: {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze how Gaza ceasefire vote affects Israel's bilateral relationships",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full analysis
  python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

  # Test with sample
  python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --sample 5

  # Use different model
  python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --model claude-3-5-sonnet-20241022
        """
    )

    parser.add_argument(
        "motion_id",
        help="ID of the motion to analyze (e.g., 01_gaza_ceasefire_resolution)"
    )

    parser.add_argument(
        "--sample",
        type=int,
        help="Only analyze N countries (for testing)"
    )

    parser.add_argument(
        "--model",
        default="claude-3-5-haiku-20241022",
        help="Model to use (default: claude-3-5-haiku for speed)"
    )

    args = parser.parse_args()

    # Run analysis
    try:
        analyzer = BilateralImpactAnalyzer(model=args.model)
        results = analyzer.run_analysis(args.motion_id, sample_size=args.sample)
        analyzer.save_results(results)

        print("\n✓ Bilateral impact analysis complete!")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠ Analysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
