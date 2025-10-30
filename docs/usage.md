# Usage Guide

This guide explains how to run UN motion simulations with AI agents.

## Prerequisites

1. **Python 3.12+** installed
2. **Virtual environment** set up
3. **API key** (for cloud provider) OR **Ollama** (for local provider)

## Setup

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your preferred editor
nano .env  # or vim, code, etc.
```

**For Cloud API (OpenAI/GPT):**
```bash
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4
```

**For Cloud API (Anthropic/Claude):**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
MODEL_NAME=claude-3-opus-20240229
```

**For Local Models (Ollama):**
```bash
# No API key needed!
# Install Ollama from https://ollama.ai
# Pull a model: ollama pull llama3
LOCAL_MODEL_NAME=llama3
```

## Running Simulations

### Basic Usage

```bash
# Run a motion with cloud API (default)
python scripts/run_motion.py 01_gaza_ceasefire_resolution

# Run with local model
python scripts/run_motion.py 01_gaza_ceasefire_resolution --provider local

# Run with specific model
python scripts/run_motion.py 01_gaza_ceasefire_resolution --model gpt-4-turbo

# Test with sample (only 5 countries)
python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 5
```

### Command-Line Options

```
python scripts/run_motion.py <motion_id> [options]

Required:
  motion_id              ID of the motion (e.g., 01_gaza_ceasefire_resolution)

Options:
  --provider {cloud,local}   AI provider (default: cloud)
  --model MODEL_NAME         Specific model to use (optional)
  --sample N                 Only query N countries for testing (optional)
  -h, --help                 Show help message
```

## Example Output

```
============================================================
Running Motion: 01_gaza_ceasefire_resolution
Provider: cloud | Model: gpt-4
============================================================

✓ Loaded motion from /home/user/AI-Agent-UN/tasks/motions/01_gaza_ceasefire_resolution.md

📊 Querying 193 countries

[1/193] Querying Afghanistan... ✅ YES
[2/193] Querying Albania... ✅ YES
[3/193] Querying Algeria... ✅ YES
[4/193] Querying Andorra... ✅ YES
[5/193] Querying Angola... ✅ YES
...

============================================================
Vote Summary:
  YES:     156 (80.8%)
  NO:       25 (13.0%)
  ABSTAIN:  12 ( 6.2%)
============================================================

✓ Results saved to: tasks/reactions/01_gaza_ceasefire_resolution_20251009_143022.json
✓ Latest results: tasks/reactions/01_gaza_ceasefire_resolution_latest.json

✓ Motion simulation complete!
```

## Understanding Results

Results are saved as JSON files in `tasks/reactions/`:

### File Structure

```json
{
  "motion_id": "01_gaza_ceasefire_resolution",
  "motion_path": "tasks/motions/01_gaza_ceasefire_resolution.md",
  "timestamp": "2025-10-09T14:30:22.123456Z",
  "provider": "cloud",
  "model": "gpt-4",
  "total_votes": 193,
  "vote_summary": {
    "yes": 156,
    "no": 25,
    "abstain": 12
  },
  "votes": [
    {
      "country": "United States",
      "country_slug": "united-states",
      "vote": "yes",
      "statement": "The United States supports this ceasefire agreement as it represents a critical step toward de-escalation and humanitarian relief. We emphasize the importance of protecting civilians and ensuring accountability for violations of international law.",
      "error": null
    },
    {
      "country": "Russia",
      "country_slug": "russia",
      "vote": "yes",
      "statement": "Russia welcomes this ceasefire and calls for immediate humanitarian access. We emphasize the need for a comprehensive political settlement based on international law and UN resolutions.",
      "error": null
    }
  ]
}
```

### Analyzing Results

You can analyze results programmatically:

```python
import json

# Load results
with open('tasks/reactions/01_gaza_ceasefire_resolution_latest.json') as f:
    results = json.load(f)

# Print vote breakdown
print(f"Total votes: {results['total_votes']}")
print(f"YES: {results['vote_summary']['yes']}")
print(f"NO: {results['vote_summary']['no']}")
print(f"ABSTAIN: {results['vote_summary']['abstain']}")

# Find all NO votes
no_votes = [v for v in results['votes'] if v['vote'] == 'no']
for vote in no_votes:
    print(f"{vote['country']}: {vote['statement']}")
```

## Tips and Best Practices

### 1. Testing with Samples

When developing or testing, use `--sample` to query only a few countries:

```bash
# Test with 5 countries first
python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 5
```

### 2. Cost Management (Cloud API)

- Start with small samples to estimate costs
- A full run (193 countries) typically uses ~200-300 API calls
- Use cheaper models (gpt-3.5-turbo) for testing
- Consider local models (Ollama) for cost-free experimentation

### 3. Local Models

Pros:
- No API costs
- Complete privacy
- Unlimited usage

Cons:
- Requires local compute resources
- May have lower quality responses
- Slower than cloud APIs

### 4. Troubleshooting

**Error: "api_key client option must be set"**
- Make sure `.env` file exists
- Check that `OPENAI_API_KEY` is set correctly
- Verify the key is valid

**Error: "Motion not found"**
- Check that the motion ID matches the filename (without .md)
- Motion files must be in `tasks/motions/`

**Error: "openai package not installed"**
- Install dependencies: `uv pip install -r requirements.txt`

**Error: Connection refused (local model)**
- Make sure Ollama is running: `ollama serve`
- Check that the model is pulled: `ollama pull llama3`

## Advanced Usage

### Using Alternative APIs

You can use any OpenAI-compatible API by setting `API_BASE_URL`:

```bash
# OpenRouter
API_BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=your-openrouter-key

# Local OpenAI-compatible server
API_BASE_URL=http://localhost:11434/v1
```

### Creating New Motions

1. Create a new markdown file in `tasks/motions/`
2. Use the format from existing motions
3. Run: `python scripts/run_motion.py your_new_motion_id`

### Analyzing Patterns

Compare different runs:

```bash
# Run with different models
python scripts/run_motion.py 01_gaza_ceasefire_resolution --model gpt-4
python scripts/run_motion.py 01_gaza_ceasefire_resolution --model gpt-3.5-turbo
python scripts/run_motion.py 01_gaza_ceasefire_resolution --provider local --model llama3

# Compare results
diff tasks/reactions/01_gaza_ceasefire_resolution_20251009_143022.json \
     tasks/reactions/01_gaza_ceasefire_resolution_20251009_144533.json
```

## Analysis and Reporting

### Running Bilateral Impact Analysis

After running a motion, analyze how votes affect bilateral relationships:

```bash
# Full analysis (all countries)
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

# Test with sample
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --sample 10

# Specify custom model
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --model claude-3-5-sonnet-20241022
```

**Outputs:**
- JSON: `tasks/analysis/{motion}_israel_bilateral_impact_latest.json`
- CSV: `tasks/analysis/{motion}_israel_bilateral_impact.csv`

### Generating CSV Reports

Convert voting results to CSV format for spreadsheet analysis:

```bash
python scripts/generate_vote_analysis_csv.py
```

This creates a CSV with:
- Country name
- Vote (yes/no/abstain)
- Statement
- Timestamp

### Creating PDF Reports

Generate formatted PDF reports from analysis results:

```bash
# From JSON analysis file
python scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

# From markdown file
python scripts/generate_simple_pdf.py analysis/01_gaza_ceasefire_resolution_analysis_REVISED.md
```

**Output:** `tasks/analysis/pdf/{filename}.pdf`

### Complete Analysis Pipeline

Run the full workflow from simulation to report:

```bash
# 1. Run motion simulation
python scripts/run_motion.py 01_gaza_ceasefire_resolution

# 2. Analyze bilateral relationships
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

# 3. Generate CSV for spreadsheet analysis
python scripts/generate_vote_analysis_csv.py

# 4. Create PDF report
python scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json

# 5. View results
ls -lh tasks/analysis/
```

## Understanding Impact Categories

The bilateral impact analysis categorizes relationship changes:

| Category | Symbol | Description |
|----------|--------|-------------|
| Strengthened Significantly | 💚 | Major improvement in bilateral relations |
| Strengthened Moderately | 🟢 | Noticeable positive impact |
| Strengthened Slightly | 🟡 | Minor improvement |
| Neutral | ⚪ | No meaningful change |
| Strained Slightly | 🟠 | Minor tension introduced |
| Strained Moderately | 🔴 | Noticeable deterioration |
| Strained Significantly | 🔥 | Major damage to relationship |

**Factors Considered:**
- Historical relationship baseline
- Vote alignment/divergence on the resolution
- Diplomatic tone in official statements
- Strategic and economic implications
- Regional dynamics and alliances

## Performance and Cost Estimates

### Simulation Performance (195 countries)

| Provider | Model | Time | Cost | Quality |
|----------|-------|------|------|---------|
| OpenAI | gpt-3.5-turbo | 5-8 min | $2-3 | Good |
| OpenAI | gpt-4 | 15-25 min | $20-30 | Excellent |
| OpenAI | gpt-4-turbo | 10-15 min | $15-20 | Excellent |
| Anthropic | claude-3-5-haiku | 6-10 min | $2-4 | Good |
| Anthropic | claude-3-5-sonnet | 20-30 min | $20-40 | Excellent |
| Anthropic | claude-opus | 40-60 min | $80-160 | Best |
| Ollama | llama3 (local) | 30-60 min | $0 | Good |

### Analysis Performance (195 countries)

| Analysis Type | Time | Model Recommendation |
|--------------|------|---------------------|
| Bilateral Impact | 6-15 min | claude-3-5-haiku (fast, affordable) |
| CSV Generation | < 1 sec | N/A (no LLM needed) |
| PDF Report | 5-10 sec | N/A (no LLM needed) |

**Cost Optimization Tips:**
- Use `--sample` for testing before full runs
- Use Haiku/gpt-3.5-turbo for initial iterations
- Use Sonnet/gpt-4 for final production runs
- Consider local models (Ollama) for experimentation

## Working with Multiple Motions

### Creating a New Motion

1. **Create the motion file:**
```bash
# Create new motion file
touch tasks/motions/02_climate_action_framework.md
```

2. **Write the resolution text:**
```markdown
# Resolution: Global Climate Action Framework

## Preamble

Recognizing the urgent need for coordinated international action on climate change,

Acknowledging the disproportionate impact of climate change on vulnerable nations,

Noting with concern the insufficient progress toward Paris Agreement targets,

## Operative Clauses

1. Calls upon all member states to submit updated Nationally Determined Contributions (NDCs) by December 2025;

2. Urges developed nations to fulfill their commitment of $100 billion annually in climate finance;

3. Requests the establishment of a Loss and Damage Fund to assist vulnerable nations;

4. Encourages the rapid phase-down of unabated coal power and inefficient fossil fuel subsidies;

5. Decides to establish an annual review mechanism to track progress toward climate goals.
```

3. **Run the simulation:**
```bash
python scripts/run_motion.py 02_climate_action_framework --sample 10  # Test first
python scripts/run_motion.py 02_climate_action_framework  # Full run
```

### Comparing Multiple Motions

```bash
# Run multiple motions
python scripts/run_motion.py 01_gaza_ceasefire_resolution
python scripts/run_motion.py 02_climate_action_framework
python scripts/run_motion.py 03_cybersecurity_treaty

# Compare voting patterns
python scripts/compare_motions.py 01_gaza_ceasefire_resolution 02_climate_action_framework
```

## Customizing Agent Behavior

### Understanding Agent System Prompts

Each country agent has a system prompt in `agents/representatives/{country-slug}/system-prompt.md`.

**Key sections:**
1. **Role and Identity**: Country name, UN status, special positions
2. **Foreign Policy Framework**: Core interests and principles
3. **Regional Context**: Geographic and alliance considerations
4. **Historical Positions**: Past voting patterns and stances
5. **Behavioral Guidelines**: Diplomatic style and tone

### Example: Viewing an Agent Prompt

```bash
# View United States agent prompt
cat agents/representatives/united-states/system-prompt.md

# View China agent prompt
cat agents/representatives/china/system-prompt.md

# List all available agents
ls agents/representatives/
```

### Testing Individual Agents

Test specific countries without running full simulation:

```bash
# Modify run_motion.py to filter by country
python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 1

# Or manually test in Python
python3 << EOF
from scripts.run_motion import MotionRunner
runner = MotionRunner(provider="cloud", model="gpt-4")
motion = runner.load_motion("01_gaza_ceasefire_resolution")
countries = [c for c in runner.get_country_list() if c['slug'] == 'united-states']
result = runner.query_agent(countries[0], motion)
print(result)
EOF
```

## Batch Processing and Automation

### Running Multiple Simulations

```bash
#!/bin/bash
# run_all_motions.sh

MOTIONS=(
  "01_gaza_ceasefire_resolution"
  "02_climate_action_framework"
  "03_cybersecurity_treaty"
)

for motion in "${MOTIONS[@]}"; do
  echo "Running motion: $motion"
  python scripts/run_motion.py "$motion"
  python scripts/analyze_israel_bilateral_impact.py "$motion"
  python scripts/generate_simple_pdf.py "tasks/analysis/${motion}_israel_bilateral_impact_latest.json"
done
```

### Scheduled Simulations

```bash
# Add to crontab for daily runs
crontab -e

# Run simulation daily at 2 AM
0 2 * * * cd /path/to/AI-Agent-UN && python scripts/run_motion.py 01_gaza_ceasefire_resolution
```

## Data Management

### Cleaning Old Results

```bash
# Use the cleanup script
bash scripts/cleanup_old_analysis.sh

# Or manually
find tasks/reactions -name "*.json" -mtime +30 -delete  # Delete files older than 30 days
```

### Backing Up Results

```bash
# Backup all results
tar -czf backup_$(date +%Y%m%d).tar.gz tasks/reactions/ tasks/analysis/

# Backup specific motion
tar -czf backup_gaza_$(date +%Y%m%d).tar.gz \
  tasks/reactions/01_gaza_ceasefire_resolution_*.json \
  tasks/analysis/01_gaza_ceasefire_resolution_*.json \
  tasks/analysis/01_gaza_ceasefire_resolution_*.csv
```

### Organizing Results

```bash
# Create organized directory structure
mkdir -p results/{2025-10,2025-11}

# Move results by date
mv tasks/reactions/*_202510*.json results/2025-10/
mv tasks/reactions/*_202511*.json results/2025-11/
```

## Integration and Export

### Exporting to Spreadsheets

```python
import json
import csv

# Load results
with open('tasks/reactions/01_gaza_ceasefire_resolution_latest.json') as f:
    data = json.load(f)

# Export to CSV
with open('voting_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Country', 'Vote', 'Statement'])
    for vote in data['votes']:
        writer.writerow([vote['country'], vote['vote'], vote['statement']])
```

### Integrating with Visualization Tools

```python
import json
import matplotlib.pyplot as plt

# Load results
with open('tasks/reactions/01_gaza_ceasefire_resolution_latest.json') as f:
    data = json.load(f)

# Create pie chart
votes = data['vote_summary']
plt.pie([votes['yes'], votes['no'], votes['abstain']],
        labels=['Yes', 'No', 'Abstain'],
        autopct='%1.1f%%')
plt.title('Vote Distribution: Gaza Ceasefire Resolution')
plt.savefig('vote_distribution.png')
```

### API Integration

```python
# Create simple API endpoint to serve results
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/motion/<motion_id>')
def get_motion_results(motion_id):
    with open(f'tasks/reactions/{motion_id}_latest.json') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)
```

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: API Rate Limit Exceeded

**Solution:**
```bash
# Use chunked processing
python scripts/run_motion_chunked.py 01_gaza_ceasefire_resolution
```

#### Issue: JSON Parse Errors

**Symptoms:** Some agents return invalid JSON

**Solution:**
- Check the `error` field in output
- Increase `max_tokens` in [run_motion.py:184](scripts/run_motion.py#L184)
- Use more capable models (GPT-4 or Claude Sonnet)

#### Issue: Inconsistent Voting Patterns

**Solution:**
- Check temperature setting (default: 0.7)
- Lower temperature for more consistent results
- Review agent system prompts for clarity

#### Issue: Out of Memory (Local Models)

**Solution:**
```bash
# Use smaller local model
ollama pull llama3:8b  # Instead of 70b

# Or reduce context window
# Edit run_motion.py to reduce max_tokens
```

## Next Steps

- **Explore Documentation**: See [architecture.md](architecture.md) for system design
- **Review Analysis Guide**: See [analysis_guide.md](../analysis_guide.md) for quick reference
- **Create Custom Motions**: Add new resolutions in `tasks/motions/`
- **Develop Analysis Tools**: Build custom scripts in `scripts/`
- **Contribute**: Submit PRs with new agents, motions, or features

## Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: Report bugs on GitHub Issues
- **Examples**: Check `tasks/` for sample inputs/outputs
- **Community**: Join discussions on GitHub Discussions
