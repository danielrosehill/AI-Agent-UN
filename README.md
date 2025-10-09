# AI Agent UN
![alt text](images/banner.jpg)


An experimental Model United Nations simulation populated by AI agents. 

Each agent embodies the foreign policy positions, diplomatic style, and national interests of a specific country.

Motions can be run as tasks and using structured outputs both votes and supporting statements can be collected and then analysed.

## Overview

This is an AI experiment designed to:
- Simulate international diplomatic interactions and negotiations
- Model how different countries might approach global issues based on their historical positions and national interests
- Explore multi-agent AI systems in complex geopolitical scenarios
- Provide an educational and research tool for understanding international relations dynamics

## Project Structure

```
AI-Agent-UN/
├── agents/
│   └── representatives/     # AI agent system prompts for each country
│       ├── united-states/
│       ├── china/
│       ├── russia/
│       └── ...
├── data/
│   └── bodies/             # UN membership data
├── tasks/
│   ├── motions/            # UN resolutions to vote on
│   └── reactions/          # Simulation results (votes & statements)
├── scripts/
│   └── run_motion.py       # Main simulation runner
├── .env.example            # Configuration template
└── requirements.txt        # Python dependencies
```

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Agent-UN.git
cd AI-Agent-UN

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# For cloud API (OpenAI):
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4

# OR for local models (Ollama):
# Install Ollama from https://ollama.ai
# Pull a model: ollama pull llama3
```

### 3. Run a Motion Simulation

```bash
# Run with cloud API (default)
python scripts/run_motion.py 01_gaza_ceasefire_resolution

# Run with local model
python scripts/run_motion.py 01_gaza_ceasefire_resolution --provider local

# Test with only 5 countries
python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 5
```

### 4. View Results

Results are saved in `tasks/reactions/` as JSON files:
- `{motion_id}_{timestamp}.json` - Timestamped result
- `{motion_id}_latest.json` - Always points to latest simulation

## How It Works

1. **Agent System Prompts**: Each country has a detailed system prompt in `agents/representatives/{country}/system-prompt.md` that defines their foreign policy positions and diplomatic style.

2. **Motion Runner**: The `run_motion.py` script:
   - Loads the motion text from `tasks/motions/`
   - Queries each country's AI agent
   - Collects votes (yes/no/abstain) and statements
   - Saves results to `tasks/reactions/`

3. **JSON-Constrained Output**: Each agent responds with structured JSON:
   ```json
   {
     "vote": "yes",
     "statement": "Brief explanation of position..."
   }
   ```

## Available Motions

- `01_gaza_ceasefire_resolution` - Support for Ceasefire Agreement in Gaza and Commitment to Lasting Peace

## AI Providers

### Cloud API
- Supports OpenAI (GPT-4, GPT-3.5-turbo, etc.)
- Supports Anthropic Claude (with API key)
- Supports any OpenAI-compatible API

### Local Models
- Uses Ollama for local inference
- Supports Llama 3, Mistral, Mixtral, and other Ollama models
- No API costs, complete privacy

## Use Cases

- Educational demonstrations of international relations concepts
- Research into multi-agent AI behavior in diplomatic contexts
- Experimentation with large language models in structured debate scenarios
- Analysis of how AI systems model complex geopolitical positions

 
## Disclaimer

This is a simulation for research and educational purposes. The AI agents' positions do not represent actual government policies or diplomatic stances. The simulation is designed to model how countries might approach issues based on their historical positions, but should not be considered authoritative or predictive.
