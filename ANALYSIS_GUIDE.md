# UN Motion Analysis Guide

Quick reference for running and understanding UN motion analyses.

## Quick Start

### 1. Run a Motion Simulation

```bash
# Full simulation (all countries)
python3 scripts/run_motion.py 01_gaza_ceasefire_resolution

# Test with sample
python3 scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 5
```

**Output:** `tasks/reactions/01_gaza_ceasefire_resolution_latest.json`

### 2. Analyze Bilateral Impact (Israel)

```bash
# Analyze Israel's bilateral relationships
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution
```

**Outputs:**
- JSON: `tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json`
- CSV: `tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact.csv`

### 3. Generate PDF Report

```bash
# From JSON analysis
python3 scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

# From markdown analysis
python3 scripts/generate_simple_pdf.py analysis/01_gaza_ceasefire_resolution_analysis_REVISED.md
```

**Output:** `tasks/analysis/pdf/{filename}.pdf`

## Analysis Types

### Bilateral Impact Analysis

**Purpose:** Understand how votes affect country-to-country relationships

**Categories:**
- 💚 **Strengthened Significantly** - Major improvement
- 🟢 **Strengthened Moderately** - Noticeable improvement
- 🟡 **Strengthened Slightly** - Minor improvement
- ⚪ **Neutral** - No meaningful change
- 🟠 **Strained Slightly** - Minor tension
- 🔴 **Strained Moderately** - Noticeable tension
- 🔥 **Strained Significantly** - Major deterioration

**Factors Considered:**
- Historical relationship baseline
- Vote alignment/divergence
- Diplomatic tone in statement
- Strategic implications
- Regional dynamics
- Economic/security ties

## JSON Schema - Bilateral Impact

```json
{
  "motion_id": "01_gaza_ceasefire_resolution",
  "timestamp": "2025-10-09T12:04:11",
  "model": "claude-3-5-haiku-20241022",
  "total_analyzed": 195,
  "impact_summary": {
    "strengthened_significantly": 5,
    "strengthened_moderately": 15,
    "strengthened_slightly": 45,
    "neutral": 100,
    "strained_slightly": 20,
    "strained_moderately": 8,
    "strained_significantly": 2
  },
  "analyses": [
    {
      "country": "Country Name",
      "vote": "yes|no|abstain",
      "statement": "Official voting statement...",
      "impact_analysis": {
        "impact_category": "neutral",
        "reasoning": "Brief 2-3 sentence analysis of impact",
        "confidence": "high|medium|low",
        "key_factors": [
          "Factor 1 affecting relationship",
          "Factor 2 affecting relationship"
        ]
      }
    }
  ]
}
```

## Performance

### Speed Comparison (195 countries)

| Model | Time | Cost | Quality |
|-------|------|------|---------|
| Claude 3.5 Haiku | 6-10 min | $2-4 | Good |
| Claude 3.5 Sonnet | 20-30 min | $20-40 | Excellent |
| Claude Opus | 40-60 min | $80-160 | Best |

**Recommendation:** Use **Haiku** for speed, **Sonnet** for production reports

## Common Workflows

### Workflow 1: Full Analysis Pipeline

```bash
# 1. Run motion (if not done)
python3 scripts/run_motion.py 01_gaza_ceasefire_resolution

# 2. Analyze bilateral impact
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

# 3. Generate PDF report
python3 scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

# 4. View results
open tasks/analysis/pdf/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.pdf
```

### Workflow 2: Quick Test

```bash
# Test with 10 countries
python3 scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 10
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --sample 10
```

### Workflow 3: CSV Analysis

```bash
# Generate analysis
python3 scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

# Open in spreadsheet
# CSV location: tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact.csv
```

## File Locations

```
AI-Agent-UN/
├── tasks/
│   ├── motions/                   # Input: resolution texts
│   │   └── 01_gaza_ceasefire_resolution.md
│   ├── reactions/                 # Output: voting results
│   │   └── 01_gaza_ceasefire_resolution_latest.json
│   └── analysis/                  # Output: analyses
│       ├── pdf/                   # PDF reports
│       ├── *_israel_bilateral_impact_latest.json
│       └── *_israel_bilateral_impact.csv
├── scripts/
│   ├── run_motion.py             # Run voting simulation
│   ├── analyze_israel_bilateral_impact.py
│   ├── generate_simple_pdf.py    # PDF generator
│   └── generate_pdf_report.py    # Alternative PDF
└── analysis/
    └── 01_gaza_ceasefire_resolution_analysis_REVISED.md
```

## Troubleshooting

### Missing API Key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Or create `.env` file:
```
ANTHROPIC_API_KEY=your-key-here
```

### Python Environment Issues

```bash
# Use system Python
python3 scripts/analyze_israel_bilateral_impact.py ...

# Or fix virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv reportlab
```

### PDF Generation Fails

```bash
# Install reportlab
pip install --break-system-packages reportlab

# Or use simple PDF generator
python3 scripts/generate_simple_pdf.py <input_file>
```

## Next Steps

1. ✅ Run bilateral impact analysis
2. ✅ Generate PDF reports
3. 🔄 Create visualizations (charts, graphs)
4. 📋 Regional bloc analysis
5. 📊 Time series tracking
6. 🌍 Multi-country relationship networks
