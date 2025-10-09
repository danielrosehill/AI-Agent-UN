# UN Motion Analysis

This directory contains analysis results from UN motion simulations.

## Analysis Types

### 1. Bilateral Relationship Impact Analysis

Analyzes how voting on resolutions affects bilateral relationships between Israel and UN member states.

**JSON Output Schema:**

```json
{
  "motion_id": "string",
  "timestamp": "ISO 8601 datetime",
  "model": "AI model used",
  "total_analyzed": "number of countries",
  "impact_summary": {
    "strengthened_significantly": 0,
    "strengthened_moderately": 0,
    "strengthened_slightly": 0,
    "neutral": 0,
    "strained_slightly": 0,
    "strained_moderately": 0,
    "strained_significantly": 0
  },
  "analyses": [
    {
      "country": "Country Name",
      "vote": "yes|no|abstain",
      "statement": "Country's voting statement",
      "impact_analysis": {
        "impact_category": "one of the 7 categories above",
        "reasoning": "2-3 sentence analysis",
        "confidence": "high|medium|low",
        "key_factors": ["factor 1", "factor 2", ...]
      }
    }
  ],
  "metadata": {
    "voting_summary": {"yes": X, "no": Y, "abstain": Z},
    "original_votes": "total number of votes"
  }
}
```

## Impact Categories

The bilateral impact analysis uses seven categories to classify relationship changes:

| Category | Description | Effect |
|----------|-------------|--------|
| **strengthened_significantly** | Major improvement in relations | 💚 |
| **strengthened_moderately** | Noticeable improvement | 🟢 |
| **strengthened_slightly** | Minor improvement | 🟡 |
| **neutral** | No meaningful change | ⚪ |
| **strained_slightly** | Minor tension | 🟠 |
| **strained_moderately** | Noticeable tension | 🔴 |
| **strained_significantly** | Major deterioration | 🔥 |

## Running Analysis

### Bilateral Impact Analysis

```bash
# Run full analysis (all countries)
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

# Test with sample
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --sample 5

# Use different model (default: claude-3-5-haiku for speed)
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --model claude-3-5-sonnet-20241022
```

### Output Files

- **JSON:** `tasks/analysis/{motion_id}_israel_bilateral_impact_latest.json`
- **CSV:** `tasks/analysis/{motion_id}_israel_bilateral_impact.csv`
- **Timestamped:** `tasks/analysis/{motion_id}_israel_bilateral_impact_{timestamp}.json`

## Generating PDF Reports

### Using reportlab (lightweight, recommended)

```bash
# Generate PDF from JSON analysis
python3 scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

# Generate PDF from markdown
python3 scripts/generate_simple_pdf.py analysis/01_gaza_ceasefire_resolution_analysis_REVISED.md

# Custom output path
python3 scripts/generate_simple_pdf.py analysis/data.json --output custom_report.pdf
```

### Using weasyprint (requires system dependencies)

```bash
python3 scripts/generate_pdf_report.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json
```

## Key Factors Analyzed

The bilateral impact analysis considers:

1. **Historical relationship baseline** - Pre-existing ties between countries
2. **Vote alignment** - Whether vote matches or diverges from expected patterns
3. **Diplomatic tone** - Language and framing in official statement
4. **Strategic implications** - Security, economic, or political consequences
5. **Regional dynamics** - Influence of regional alliances and pressures
6. **Economic/security ties** - Existing bilateral agreements and cooperation

## Analysis Speed

Using **Claude 3.5 Haiku** for maximum efficiency:
- ~1-2 seconds per country analysis
- Full 195-country analysis: ~6-10 minutes
- Cost: ~$0.01-0.02 per country

Alternative models:
- **Claude 3.5 Sonnet**: Higher quality, ~3x slower, ~10x more expensive
- **Claude Opus**: Highest quality, ~5x slower, ~40x more expensive

## Output Formats

| Format | Use Case | Tool |
|--------|----------|------|
| **JSON** | Programmatic analysis, detailed data | Auto-generated |
| **CSV** | Spreadsheet analysis, filtering, sorting | Auto-generated |
| **PDF** | Presentation, sharing, printing | `generate_simple_pdf.py` |

## Directory Structure

```
tasks/analysis/
├── README.md                                    # This file
├── pdf/                                         # Generated PDF reports
│   ├── 01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.pdf
│   └── 01_gaza_ceasefire_resolution_analysis_REVISED.pdf
├── 01_gaza_ceasefire_resolution_analysis_REVISED.md  # Manual analysis
├── 01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json
├── 01_gaza_ceasefire_resolution_israel_bilateral_impact.csv
└── 01_gaza_ceasefire_resolution_israel_bilateral_impact_{timestamp}.json
```

## Future Analysis Types

Planned analysis extensions:

1. **Regional bloc impact** - How votes affect regional alliances
2. **Trade relationship impact** - Economic consequences of votes
3. **Security partnership impact** - Defense cooperation effects
4. **Multilateral forum impact** - Effects on UN/NATO/AU/etc. dynamics
5. **Time series analysis** - Tracking relationship changes over multiple votes
