#!/usr/bin/env python3
"""
UN Motion Simulation Runner

This script runs a UN motion simulation where AI agents representing different countries
vote on resolutions and provide statements explaining their positions.

Usage:
    python scripts/run_motion.py <motion_id> [--provider cloud|local] [--model MODEL_NAME]

Example:
    python scripts/run_motion.py 01_gaza_ceasefire_resolution --provider cloud
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


class MotionRunner:
    """Runs UN motion simulations with AI agents"""

    VALID_VOTES = ["yes", "no", "abstain"]

    def __init__(self, provider: str = "cloud", model: Optional[str] = None):
        """
        Initialize the motion runner

        Args:
            provider: Either 'cloud' (API) or 'local' (local model)
            model: Model name/identifier (optional, uses defaults if not specified)
        """
        self.provider = provider
        self.model = model
        self.project_root = PROJECT_ROOT
        self.agents_dir = self.project_root / "agents" / "representatives"
        self.motions_dir = self.project_root / "tasks" / "motions"
        self.results_dir = self.project_root / "tasks" / "reactions"

        # Load configuration
        self._load_config()

        # Initialize AI client based on provider
        self._init_ai_client()

    def _load_config(self):
        """Load configuration from environment variables"""
        from dotenv import load_dotenv
        load_dotenv()

        if self.provider == "cloud":
            self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
            self.api_base = os.getenv("API_BASE_URL")
            if not self.model:
                self.model = os.getenv("MODEL_NAME", "gpt-4")
        else:
            # Local model configuration
            self.local_model_path = os.getenv("LOCAL_MODEL_PATH")
            if not self.model:
                self.model = os.getenv("LOCAL_MODEL_NAME", "llama3")

    def _init_ai_client(self):
        """Initialize the appropriate AI client"""
        if self.provider == "cloud":
            try:
                # Try OpenAI-compatible API
                import openai
                if self.api_base:
                    self.client = openai.OpenAI(
                        api_key=self.api_key,
                        base_url=self.api_base
                    )
                else:
                    self.client = openai.OpenAI(api_key=self.api_key)
                print(f"✓ Initialized cloud API client (model: {self.model})")
            except ImportError:
                print("Error: openai package not installed. Run: pip install openai")
                sys.exit(1)
        else:
            try:
                # Use Ollama for local models
                import ollama
                self.client = ollama
                print(f"✓ Initialized local model client (model: {self.model})")
            except ImportError:
                print("Error: ollama package not installed. Run: pip install ollama")
                sys.exit(1)

    def get_country_list(self) -> List[Dict[str, str]]:
        """Get list of all countries with agents"""
        countries = []
        for country_dir in sorted(self.agents_dir.iterdir()):
            if country_dir.is_dir():
                system_prompt_path = country_dir / "system-prompt.md"
                if system_prompt_path.exists():
                    country_name = country_dir.name.replace("-", " ").title()
                    countries.append({
                        "name": country_name,
                        "slug": country_dir.name,
                        "prompt_path": str(system_prompt_path)
                    })
        return countries

    def load_motion(self, motion_id: str) -> Dict:
        """Load motion text from file"""
        motion_path = self.motions_dir / f"{motion_id}.md"
        if not motion_path.exists():
            raise FileNotFoundError(f"Motion not found: {motion_path}")

        with open(motion_path, 'r', encoding='utf-8') as f:
            motion_text = f.read()

        return {
            "id": motion_id,
            "text": motion_text,
            "path": str(motion_path)
        }

    def load_agent_prompt(self, prompt_path: str) -> str:
        """Load agent system prompt"""
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def query_agent(self, country: Dict, motion: Dict) -> Dict:
        """
        Query an AI agent for their vote and statement

        Returns:
            Dict with 'vote' (yes/no/abstain) and 'statement' (brief explanation)
        """
        system_prompt = self.load_agent_prompt(country['prompt_path'])

        user_prompt = f"""You are voting on the following UN General Assembly resolution:

{motion['text']}

You must respond with a JSON object containing:
1. "vote": Your vote - must be exactly one of: "yes", "no", or "abstain"
2. "statement": A brief statement (2-4 sentences) explaining your country's position

Your response must be valid JSON in this exact format:
{{
  "vote": "yes",
  "statement": "Your explanation here."
}}

Remember to vote according to {country['name']}'s national interests and foreign policy positions."""

        try:
            if self.provider == "cloud":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                content = response.choices[0].message.content
            else:
                response = self.client.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                content = response['message']['content']

            # Extract JSON from response (handle markdown code blocks)
            content = content.strip()
            if content.startswith("```"):
                # Remove markdown code block
                content = re.sub(r'^```(?:json)?\n', '', content)
                content = re.sub(r'\n```$', '', content)

            # Parse JSON response
            result = json.loads(content)

            # Validate response
            if "vote" not in result or "statement" not in result:
                raise ValueError("Response missing required fields")

            if result["vote"].lower() not in self.VALID_VOTES:
                raise ValueError(f"Invalid vote: {result['vote']}")

            result["vote"] = result["vote"].lower()
            return result

        except json.JSONDecodeError as e:
            print(f"  ⚠ JSON parse error for {country['name']}: {e}")
            print(f"  Raw response: {content[:200]}...")
            return {
                "vote": "abstain",
                "statement": f"[Error: Unable to parse response]",
                "error": str(e)
            }
        except Exception as e:
            print(f"  ⚠ Error querying {country['name']}: {e}")
            return {
                "vote": "abstain",
                "statement": f"[Error: {str(e)}]",
                "error": str(e)
            }

    def run_motion(self, motion_id: str, sample_size: Optional[int] = None) -> Dict:
        """
        Run a motion through all country agents

        Args:
            motion_id: ID of the motion to run
            sample_size: If set, only query this many countries (for testing)

        Returns:
            Dict containing all votes and metadata
        """
        print(f"\n{'='*60}")
        print(f"Running Motion: {motion_id}")
        print(f"Provider: {self.provider} | Model: {self.model}")
        print(f"{'='*60}\n")

        # Load motion
        motion = self.load_motion(motion_id)
        print(f"✓ Loaded motion from {motion['path']}\n")

        # Get countries
        countries = self.get_country_list()
        if sample_size:
            countries = countries[:sample_size]
            print(f"📊 Querying {sample_size} countries (sample mode)\n")
        else:
            print(f"📊 Querying {len(countries)} countries\n")

        # Query each country
        votes = []
        vote_counts = {"yes": 0, "no": 0, "abstain": 0}

        for i, country in enumerate(countries, 1):
            print(f"[{i}/{len(countries)}] Querying {country['name']}...", end=" ", flush=True)

            result = self.query_agent(country, motion)

            vote_counts[result["vote"]] += 1
            votes.append({
                "country": country['name'],
                "country_slug": country['slug'],
                "vote": result["vote"],
                "statement": result["statement"],
                "error": result.get("error")
            })

            # Print vote result
            vote_emoji = {"yes": "✅", "no": "❌", "abstain": "⚪"}
            print(f"{vote_emoji[result['vote']]} {result['vote'].upper()}")

        # Compile results
        results = {
            "motion_id": motion_id,
            "motion_path": motion['path'],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "provider": self.provider,
            "model": self.model,
            "total_votes": len(countries),
            "vote_summary": vote_counts,
            "votes": votes
        }

        # Print summary
        print(f"\n{'='*60}")
        print(f"Vote Summary:")
        print(f"  YES:     {vote_counts['yes']:3d} ({vote_counts['yes']/len(countries)*100:.1f}%)")
        print(f"  NO:      {vote_counts['no']:3d} ({vote_counts['no']/len(countries)*100:.1f}%)")
        print(f"  ABSTAIN: {vote_counts['abstain']:3d} ({vote_counts['abstain']/len(countries)*100:.1f}%)")
        print(f"{'='*60}\n")

        return results

    def save_results(self, results: Dict):
        """Save simulation results to file"""
        # Create results directory if it doesn't exist
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{results['motion_id']}_{timestamp}.json"
        filepath = self.results_dir / filename

        # Save results
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✓ Results saved to: {filepath}")

        # Also create/update a "latest" symlink or copy
        latest_filepath = self.results_dir / f"{results['motion_id']}_latest.json"
        with open(latest_filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✓ Latest results: {latest_filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Run UN motion simulation with AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with cloud API (default)
  python scripts/run_motion.py 01_gaza_ceasefire_resolution

  # Run with local model
  python scripts/run_motion.py 01_gaza_ceasefire_resolution --provider local

  # Test with only 5 countries
  python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 5

  # Use specific model
  python scripts/run_motion.py 01_gaza_ceasefire_resolution --model gpt-4-turbo
        """
    )

    parser.add_argument(
        "motion_id",
        help="ID of the motion to run (e.g., 01_gaza_ceasefire_resolution)"
    )

    parser.add_argument(
        "--provider",
        choices=["cloud", "local"],
        default="cloud",
        help="AI provider: cloud (API) or local (Ollama)"
    )

    parser.add_argument(
        "--model",
        help="Model name (optional, uses config defaults)"
    )

    parser.add_argument(
        "--sample",
        type=int,
        help="Only query N countries (for testing)"
    )

    args = parser.parse_args()

    # Run simulation
    try:
        runner = MotionRunner(provider=args.provider, model=args.model)
        results = runner.run_motion(args.motion_id, sample_size=args.sample)
        runner.save_results(results)

        print("\n✓ Motion simulation complete!")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠ Simulation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
