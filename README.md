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

## Analysis Tools

Beyond basic voting simulations, the repository includes powerful analysis capabilities:

### Bilateral Impact Analysis
Analyze how votes affect country-to-country relationships:
```bash
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution
```

**Output:** JSON and CSV files categorizing relationship impacts:
- 💚 Strengthened Significantly
- 🟢 Strengthened Moderately
- 🟡 Strengthened Slightly
- ⚪ Neutral
- 🟠 Strained Slightly
- 🔴 Strained Moderately
- 🔥 Strained Significantly

### PDF Report Generation
Create formatted reports from analysis results:
```bash
python scripts/generate_simple_pdf.py tasks/analysis/01_gaza_ceasefire_resolution_israel_bilateral_impact_latest.json
```

### CSV Export
Export results to spreadsheet format for further analysis:
```bash
python scripts/generate_vote_analysis_csv.py
```

[See full analysis guide →](analysis_guide.md)

## AI Providers

### Cloud API
- Supports OpenAI (GPT-4, GPT-3.5-turbo, etc.)
- Supports Anthropic Claude (with API key)
- Supports any OpenAI-compatible API

### Local Models
- Uses Ollama for local inference
- Supports Llama 3, Mistral, Mixtral, and other Ollama models
- No API costs, complete privacy

## Documentation

### Getting Started
- **[Quick Start](#quick-start)** - Installation and basic usage
- **[How It Works](#how-it-works)** - Overview of the simulation system
- **[Usage Guide](docs/usage.md)** - Comprehensive guide to running simulations
- **[Analysis Guide](analysis_guide.md)** - Quick reference for analysis tools

### Core Documentation
- **[Architecture & Design](docs/architecture.md)** - System design, data flows, and extensibility
- **[Agent System](agents/representatives/)** - AI agent system prompts for each country
- **[Motions](tasks/motions/)** - UN resolutions for voting simulations
- **[Analysis Results](tasks/analysis/)** - Simulation outputs and analysis data

### Advanced Topics
- **[Use Cases](docs/architecture.md#use-cases)** - Educational, research, policy, and business applications
- **[Data Integration](docs/architecture.md#data-integration-opportunities)** - Connect with UN data, economic indicators, news, and more
- **[LLM Provider Support](docs/architecture.md#llm-provider-support)** - Cloud and local AI model configuration

## Use Cases

### Education
- **International Relations Courses**: Teach UN voting dynamics and coalition building
- **Model UN Training**: Prepare students with authentic diplomatic language and tactics
- Study how national interests and alliances drive voting behavior

### Research
- **Comparative AI Analysis**: Compare how different LLMs model geopolitical reasoning
- **Predictive Analysis**: Test hypothetical resolutions and predict voting patterns
- **Multi-Agent Systems**: Study emergent behavior in complex diplomatic scenarios

### Policy Analysis
- **Scenario Planning**: Explore "what-if" scenarios for diplomatic initiatives
- **Impact Assessment**: Understand how votes affect bilateral relationships
- Test resolution language for maximum support

### Journalism & Media
- **Background Research**: Understand country positions for UN reporting
- **Fact-Checking**: Compare AI predictions with actual voting records
- Generate data visualizations for news stories

### Business & Strategy
- **Risk Assessment**: Assess geopolitical risk for business planning
- **Supply Chain Planning**: Anticipate diplomatic disruptions
- Understand government policy trajectories

[See full use case documentation →](docs/architecture.md#use-cases)


## Disclaimer

**This is an experimental model and educational tool.**

This repository presents a conceptual framework and experimental model for simulating UN proceedings using AI agents. The primary purpose is to outline an approach to multi-agent diplomatic simulation and provide educational insights into international relations.

- **Not Predictive**: AI agent positions do not represent actual government policies or diplomatic stances
- **Educational Purpose**: Designed for research, education, and exploring multi-agent AI systems
- **Experimental Nature**: This is a proof-of-concept demonstrating how AI can model diplomatic interactions
- **Model-Focused**: The value lies in the modeling approach and system architecture, not in predicting actual UN votes
- **Code Samples**: Python scripts are provided as supplementary implementation examples

The simulation models how countries might approach issues based on historical positions and foreign policy frameworks, but should not be considered authoritative, predictive, or representative of actual diplomatic positions.
