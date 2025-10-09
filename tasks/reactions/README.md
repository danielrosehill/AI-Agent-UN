# Motion Reactions

This directory contains the results of motion simulations where AI agents representing UN member states vote on resolutions and provide statements.

## Directory Structure

Each motion simulation produces a timestamped JSON file with the following format:

```
tasks/reactions/
├── 01_gaza_ceasefire_resolution_20251009_143022.json
├── 01_gaza_ceasefire_resolution_latest.json
└── README.md
```

## Result File Format

Each result file contains:

```json
{
  "motion_id": "01_gaza_ceasefire_resolution",
  "motion_path": "path/to/motion.md",
  "timestamp": "2025-10-09T14:30:22.123456Z",
  "provider": "cloud",
  "model": "gpt-4",
  "total_votes": 193,
  "vote_summary": {
    "yes": 150,
    "no": 30,
    "abstain": 13
  },
  "votes": [
    {
      "country": "United States",
      "country_slug": "united-states",
      "vote": "yes",
      "statement": "The United States supports this ceasefire agreement...",
      "error": null
    }
  ]
}
```

## Fields Description

- **motion_id**: Identifier of the motion that was voted on
- **motion_path**: Path to the motion document
- **timestamp**: UTC timestamp of when the simulation was run
- **provider**: AI provider used (cloud or local)
- **model**: Specific model used for the simulation
- **total_votes**: Total number of countries that voted
- **vote_summary**: Breakdown of votes by type
- **votes**: Array of individual country votes and statements
  - **country**: Full country name
  - **country_slug**: URL-friendly country identifier
  - **vote**: Vote cast (yes/no/abstain)
  - **statement**: Brief explanation of the country's position
  - **error**: Error message if the vote failed (null if successful)

## Usage

Results are automatically generated when running:

```bash
python scripts/run_motion.py <motion_id>
```

The `*_latest.json` file is always updated to point to the most recent simulation for each motion, making it easy to reference the current results.
