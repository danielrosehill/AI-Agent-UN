#!/usr/bin/env python3
"""
Chunked UN Motion Simulation Runner

Processes countries in batches to allow incremental saving and better control.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from run_motion import MotionRunner


def run_chunked_simulation(motion_id: str, chunk_size: int = 20, provider: str = "cloud", model: str = None):
    """Run simulation in chunks and save incrementally"""

    runner = MotionRunner(provider=provider, model=model)
    motion = runner.load_motion(motion_id)
    countries = runner.get_country_list()

    print(f"\n{'='*60}")
    print(f"Chunked Motion Runner")
    print(f"Motion: {motion_id}")
    print(f"Total Countries: {len(countries)}")
    print(f"Chunk Size: {chunk_size}")
    print(f"Provider: {provider} | Model: {runner.model}")
    print(f"{'='*60}\n")

    # Initialize results
    all_votes = []
    vote_counts = {"yes": 0, "no": 0, "abstain": 0}

    # Process in chunks
    total_chunks = (len(countries) + chunk_size - 1) // chunk_size

    for chunk_idx in range(total_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, len(countries))
        chunk = countries[start_idx:end_idx]

        print(f"\n{'─'*60}")
        print(f"Processing Chunk {chunk_idx + 1}/{total_chunks}")
        print(f"Countries {start_idx + 1}-{end_idx} of {len(countries)}")
        print(f"{'─'*60}\n")

        for i, country in enumerate(chunk, start=start_idx + 1):
            print(f"[{i}/{len(countries)}] Querying {country['name']}...", end=" ", flush=True)

            result = runner.query_agent(country, motion)
            vote_counts[result["vote"]] += 1
            all_votes.append({
                "country": country['name'],
                "country_slug": country['slug'],
                "vote": result["vote"],
                "statement": result["statement"],
                "error": result.get("error")
            })

            vote_emoji = {"yes": "✅", "no": "❌", "abstain": "⚪"}
            print(f"{vote_emoji[result['vote']]} {result['vote'].upper()}")

        # Save intermediate results after each chunk
        intermediate_results = {
            "motion_id": motion_id,
            "motion_path": motion['path'],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "provider": provider,
            "model": runner.model,
            "total_votes": len(all_votes),
            "vote_summary": vote_counts.copy(),
            "votes": all_votes,
            "status": f"In progress: {len(all_votes)}/{len(countries)} countries processed"
        }

        # Save to intermediate file
        intermediate_path = runner.results_dir / f"{motion_id}_partial.json"
        runner.results_dir.mkdir(parents=True, exist_ok=True)
        with open(intermediate_path, 'w', encoding='utf-8') as f:
            json.dump(intermediate_results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Saved intermediate results: {len(all_votes)}/{len(countries)} countries")
        print(f"   File: {intermediate_path}")

    # Final results
    print(f"\n{'='*60}")
    print(f"Final Vote Summary:")
    print(f"  YES:     {vote_counts['yes']:3d} ({vote_counts['yes']/len(countries)*100:.1f}%)")
    print(f"  NO:      {vote_counts['no']:3d} ({vote_counts['no']/len(countries)*100:.1f}%)")
    print(f"  ABSTAIN: {vote_counts['abstain']:3d} ({vote_counts['abstain']/len(countries)*100:.1f}%)")
    print(f"{'='*60}\n")

    final_results = {
        "motion_id": motion_id,
        "motion_path": motion['path'],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "provider": provider,
        "model": runner.model,
        "total_votes": len(countries),
        "vote_summary": vote_counts,
        "votes": all_votes
    }

    # Save final results
    runner.save_results(final_results)

    # Clean up partial file
    intermediate_path = runner.results_dir / f"{motion_id}_partial.json"
    if intermediate_path.exists():
        intermediate_path.unlink()

    return final_results


def main():
    parser = argparse.ArgumentParser(description="Run UN motion simulation in chunks")

    parser.add_argument("motion_id", help="ID of the motion to run")
    parser.add_argument("--chunk-size", type=int, default=20, help="Countries per chunk (default: 20)")
    parser.add_argument("--provider", choices=["cloud", "local"], default="cloud", help="AI provider")
    parser.add_argument("--model", help="Model name (optional)")

    args = parser.parse_args()

    try:
        run_chunked_simulation(
            args.motion_id,
            chunk_size=args.chunk_size,
            provider=args.provider,
            model=args.model
        )
        print("\n✓ Chunked simulation complete!")
    except KeyboardInterrupt:
        print("\n\n⚠ Simulation interrupted by user")
        print("💾 Partial results saved in *_partial.json file")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
