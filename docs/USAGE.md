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

## Next Steps

- Create additional motions in `tasks/motions/`
- Analyze voting patterns across different issues
- Compare how different AI models vote
- Export results to visualization tools
- Build analysis scripts to identify voting blocs
