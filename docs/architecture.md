# AI Agent UN - Architecture & Design

## Overview

This repository implements a **multi-agent simulation system** for the United Nations, where each AI agent represents a country with its own foreign policy stance, diplomatic style, and national interests. The system enables running structured simulations of UN proceedings, analyzing voting patterns, and studying international relations dynamics.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Simulation Layer                          │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ run_motion │  │ run_motion_  │  │ Other           │    │
│  │    .py     │  │  chunked.py  │  │ Simulations     │    │
│  └────────────┘  └──────────────┘  └─────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                      Agent Layer                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  AI Agents (195+ Countries)                         │   │
│  │  Each with:                                         │   │
│  │  • System prompt defining foreign policy           │   │
│  │  • Diplomatic style and national interests         │   │
│  │  • Historical voting patterns                      │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                     LLM Provider Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   OpenAI     │  │  Anthropic   │  │   Ollama     │     │
│  │   (GPT-4)    │  │  (Claude)    │  │   (Local)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                    Analysis Layer                            │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │   Bilateral    │  │  Vote Analysis │  │ PDF Report   │ │
│  │    Impact      │  │      CSV       │  │  Generator   │ │
│  └────────────────┘  └────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agent System (`agents/representatives/`)

Each country is represented by an AI agent with:

**Structure:**
```
agents/representatives/{country-slug}/
└── system-prompt.md    # Agent's system prompt defining behavior
```

**System Prompt Components:**
- **Role and Identity**: Country name, UN status, special positions (e.g., P5 membership)
- **Core Responsibilities**: Representing national interests, voting, coalition building
- **Behavioral Guidelines**: Diplomatic tone, historical context, strategic thinking
- **Foreign Policy Framework**: Key priorities, alliances, historical positions
- **Regional Context**: Geographic considerations, regional relationships
- **Voting Considerations**: Factors influencing vote decisions

**Example Countries:**
- `united-states/` - P5 member, global leadership role
- `china/` - P5 member, non-interference principle
- `india/` - Major regional power, non-aligned movement
- `vatican-city/` - Observer state, moral authority focus

### 2. Motion System (`tasks/motions/`)

Motions are UN resolutions or proposals that agents vote on.

**Structure:**
```
tasks/motions/
└── {motion_id}.md    # Resolution text in markdown
```

**Motion Format:**
```markdown
# Resolution Title

## Preamble
Acknowledging/Recognizing/Noting context...

## Operative Clauses
1. Calls upon all parties to...
2. Urges member states to...
3. Requests the Secretary-General to...
```

**Examples:**
- `01_gaza_ceasefire_resolution.md` - Ceasefire and peace agreement

### 3. Simulation Runner (`scripts/run_motion.py`)

The core simulation engine that orchestrates voting.

**Key Features:**
- Multi-provider support (OpenAI, Anthropic, Ollama)
- Structured JSON output from agents
- Progress tracking and error handling
- Sample mode for testing
- Timestamped result storage

**Workflow:**
1. Load motion text from `tasks/motions/`
2. Load all country agents from `agents/representatives/`
3. For each country:
   - Load agent's system prompt
   - Query LLM with motion text
   - Parse structured response (vote + statement)
   - Store result
4. Aggregate votes and save to `tasks/reactions/`

**Output Format:**
```json
{
  "motion_id": "01_gaza_ceasefire_resolution",
  "timestamp": "2025-10-09T15:30:00Z",
  "provider": "cloud",
  "model": "gpt-4",
  "total_votes": 195,
  "vote_summary": {
    "yes": 145,
    "no": 8,
    "abstain": 42
  },
  "votes": [
    {
      "country": "United States",
      "country_slug": "united-states",
      "vote": "yes",
      "statement": "The United States supports this ceasefire...",
      "error": null
    }
  ]
}
```

### 4. Analysis Scripts (`scripts/`)

Post-simulation analysis tools.

#### Bilateral Impact Analysis
**Script:** `analyze_israel_bilateral_impact.py`

Analyzes how votes affect country-to-country relationships.

**Process:**
1. Load voting results from `tasks/reactions/`
2. For each country, query LLM to analyze:
   - Historical relationship baseline
   - Vote alignment/divergence
   - Diplomatic tone in statements
   - Strategic implications
3. Categorize impact:
   - Strengthened (significantly, moderately, slightly)
   - Neutral
   - Strained (slightly, moderately, significantly)
4. Export to JSON and CSV

**Output:**
- `tasks/analysis/{motion}_israel_bilateral_impact_latest.json`
- `tasks/analysis/{motion}_israel_bilateral_impact.csv`

#### Vote Analysis CSV
**Script:** `generate_vote_analysis_csv.py`

Generates spreadsheet-friendly vote summaries.

#### PDF Report Generator
**Scripts:** `generate_simple_pdf.py`, `generate_pdf_report.py`

Creates formatted PDF reports from analysis results.

### 5. Data Layer (`data/`)

**UN Body Membership:**
```
data/bodies/
└── general-assembly.json    # List of all UN member states
```

Contains structured data about UN membership, regional blocs, and organizational structures.

## Design Principles

### 1. Modularity
- **Separation of Concerns**: Agents, motions, simulations, and analysis are independent
- **Pluggable Components**: Easy to add new agents, motions, or analysis types
- **Provider Agnostic**: Support for multiple LLM providers

### 2. Structured Output
- **JSON Schema**: All agent responses follow strict JSON format
- **Validation**: Vote validation (yes/no/abstain only)
- **Error Handling**: Graceful degradation with error tracking

### 3. Reproducibility
- **Timestamped Results**: All outputs include timestamps and model information
- **Version Control**: System prompts and motions in git
- **Deterministic**: Same inputs produce comparable outputs (with temperature control)

### 4. Scalability
- **Batch Processing**: Efficient querying of 195+ agents
- **Sample Mode**: Test with subset of countries
- **Chunked Execution**: Support for rate limits and long-running simulations

### 5. Extensibility
- **New Motions**: Simply add markdown file to `tasks/motions/`
- **New Agents**: Add directory with system prompt to `agents/representatives/`
- **New Analysis**: Create new scripts in `scripts/` using existing data formats

## Data Flow

### Simulation Flow
```
1. User invokes: python scripts/run_motion.py <motion_id>
                              ↓
2. Load motion text from tasks/motions/{motion_id}.md
                              ↓
3. Load all agent system prompts from agents/representatives/*/system-prompt.md
                              ↓
4. For each agent:
   a. Construct prompt: system_prompt + motion_text + instructions
   b. Query LLM API (OpenAI/Anthropic/Ollama)
   c. Parse JSON response: {vote, statement}
   d. Validate vote (yes/no/abstain)
                              ↓
5. Aggregate results into JSON structure
                              ↓
6. Save to: tasks/reactions/{motion_id}_{timestamp}.json
7. Create symlink: tasks/reactions/{motion_id}_latest.json
```

### Analysis Flow
```
1. Load voting results from tasks/reactions/{motion_id}_latest.json
                              ↓
2. For each country vote:
   a. Extract: country, vote, statement
   b. Construct analysis prompt with relationship context
   c. Query LLM for impact assessment
   d. Parse structured response: {impact_category, reasoning, confidence, key_factors}
                              ↓
3. Aggregate analysis results
                              ↓
4. Generate outputs:
   • JSON: tasks/analysis/{motion}_israel_bilateral_impact_latest.json
   • CSV: tasks/analysis/{motion}_israel_bilateral_impact.csv
   • PDF: tasks/analysis/pdf/{motion}_israel_bilateral_impact_latest.pdf
```

## Agent Prompt Engineering

### Prompt Structure
```
┌────────────────────────────────────┐
│      SYSTEM PROMPT                 │
│  (from agent's system-prompt.md)   │
│                                    │
│  • Role and Identity               │
│  • Foreign Policy Framework        │
│  • Historical Positions            │
│  • Regional Context                │
│  • Behavioral Guidelines           │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│      USER PROMPT                   │
│  (generated by simulation runner)  │
│                                    │
│  • Motion Text                     │
│  • Voting Instructions             │
│  • JSON Output Format              │
│  • Statement Requirements          │
└────────────────────────────────────┘
              ↓
┌────────────────────────────────────┐
│      STRUCTURED OUTPUT             │
│  {                                 │
│    "vote": "yes|no|abstain",       │
│    "statement": "..."              │
│  }                                 │
└────────────────────────────────────┘
```

### Key Prompt Features

**1. Specificity**: Agents are instructed to reference their country's unique perspective
```
"Your statement must articulate {country}'s UNIQUE perspective,
national interests, and specific reasons for this vote."
```

**2. Historical Grounding**: Prompts encourage reference to past positions
```
"Reference your country's:
- Historical positions on this issue
- Regional concerns and alliances
- Domestic political considerations"
```

**3. Authenticity**: Avoid generic diplomatic language
```
"Avoid generic diplomatic language.
Be specific to {country}'s situation and worldview."
```

**4. Structured Output**: Strict JSON format enforcement
```json
{
  "vote": "yes",
  "statement": "Your explanation here."
}
```

## LLM Provider Support

### Cloud Providers

#### OpenAI
```python
client = openai.OpenAI(api_key=API_KEY)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7,
    max_tokens=800
)
```

#### Anthropic Claude
```python
client = anthropic.Anthropic(api_key=API_KEY)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=800,
    system=system_prompt,
    messages=[{"role": "user", "content": user_prompt}],
    temperature=0.7
)
```

### Local Provider

#### Ollama
```python
import ollama
response = ollama.chat(
    model="llama3",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
```

## Configuration

### Environment Variables
```bash
# Cloud API (OpenAI)
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4

# Cloud API (Anthropic)
ANTHROPIC_API_KEY=sk-ant-...
MODEL_NAME=claude-3-5-sonnet-20241022

# Cloud API (OpenRouter - any model)
OPENAI_API_KEY=sk-or-...
API_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=anthropic/claude-3.5-sonnet

# Local (Ollama)
LOCAL_MODEL_NAME=llama3
LOCAL_MODEL_PATH=/path/to/model
```

## File Naming Conventions

### Slugs
Country directory names use lowercase with hyphens:
- `united-states` (not `United States` or `USA`)
- `united-kingdom` (not `UK`)
- `saudi-arabia`

### Timestamps
ISO 8601 format with UTC timezone:
```
2025-10-09T15:30:00Z
```

File timestamps use compact format:
```
20251009_153000
```

### Motion IDs
Sequential numbering with descriptive slug:
```
01_gaza_ceasefire_resolution
02_climate_action_framework
03_cybersecurity_treaty
```

## Error Handling

### Agent Response Errors
- **JSON Parse Error**: Log error, default to abstain vote
- **Invalid Vote**: Log error, default to abstain vote
- **API Error**: Log error, mark as error in output
- **Timeout**: Retry once, then fail gracefully

### Validation
- Vote must be exactly: "yes", "no", or "abstain"
- Statement must be non-empty string
- All required fields must be present

### Recovery
- Partial results are saved (simulation can be resumed)
- Error details included in output JSON
- Graceful degradation for missing data

## Performance Considerations

### Simulation Performance
- **Sequential Processing**: One agent at a time (API rate limits)
- **Sample Mode**: Test with 5-10 countries for development
- **Chunked Processing**: Split large simulations into batches

### Model Performance
| Model | Speed (195 countries) | Cost | Quality |
|-------|----------------------|------|---------|
| GPT-3.5 Turbo | 5-8 min | $2-3 | Good |
| GPT-4 | 15-25 min | $20-30 | Excellent |
| Claude 3.5 Haiku | 6-10 min | $2-4 | Good |
| Claude 3.5 Sonnet | 20-30 min | $20-40 | Excellent |
| Llama 3 (local) | 30-60 min | $0 | Good |

### Analysis Performance
- **Bilateral Analysis**: ~10-15 minutes for 195 relationships
- **CSV Generation**: < 1 second
- **PDF Generation**: 5-10 seconds

## Use Cases

### 1. Educational Applications

#### International Relations Courses
**Use Case:** Teaching UN voting dynamics and coalition building
```python
# Demonstrate how regional blocs vote on contentious issues
python scripts/run_motion.py 01_gaza_ceasefire_resolution
# Analyze P5 voting patterns
python scripts/analyze_p5_voting.py 01_gaza_ceasefire_resolution
```

**Learning Outcomes:**
- Understand how national interests drive voting behavior
- Observe coalition formation (Arab League, EU, G77, etc.)
- Analyze the role of P5 members and veto power
- Study how diplomatic language reflects policy positions

#### Model UN Training
**Use Case:** Prepare students for Model UN competitions
```bash
# Students can study how their assigned country votes
cat agents/representatives/france/system-prompt.md

# Compare with actual UN voting records
python scripts/compare_with_real_votes.py 01_gaza_ceasefire_resolution
```

**Benefits:**
- Learn authentic diplomatic language and negotiation tactics
- Understand historical voting patterns and alliances
- Practice position papers based on AI-generated statements
- Study how different countries frame similar arguments

### 2. Research Applications

#### Comparative AI Analysis
**Use Case:** Study how different LLMs model geopolitical reasoning
```bash
# Run same motion with different models
python scripts/run_motion.py 01_gaza_ceasefire_resolution --model gpt-4
python scripts/run_motion.py 01_gaza_ceasefire_resolution --model claude-3-5-sonnet-20241022
python scripts/run_motion.py 01_gaza_ceasefire_resolution --provider local --model llama3

# Compare results
python scripts/compare_model_outputs.py gpt-4 claude-3-5-sonnet llama3
```

**Research Questions:**
- How do different LLMs interpret foreign policy constraints?
- Which models better capture nuanced diplomatic positions?
- Do local models have biases in international relations?
- How consistent are model responses across temperature settings?

#### Predictive Analysis
**Use Case:** Predict likely voting patterns on proposed resolutions
```python
# Test hypothetical resolution before actual UN vote
python scripts/run_motion.py 04_hypothetical_taiwan_resolution --sample 20

# Analyze predicted impact on key relationships
python scripts/analyze_bilateral_impact.py 04_hypothetical_taiwan_resolution
```

**Applications:**
- Diplomatic planning and scenario analysis
- Understanding likely opposition and support
- Identifying potential coalition partners
- Assessing diplomatic risk

#### Multi-Agent Systems Research
**Use Case:** Study emergent behavior in complex agent systems
```python
# Enable multi-turn negotiations
python scripts/run_negotiation.py 01_gaza_ceasefire_resolution --rounds 3

# Analyze coalition formation
python scripts/analyze_coalitions.py 01_gaza_ceasefire_resolution
```

**Research Areas:**
- How do agents form voting blocs without explicit coordination?
- Can agents reach compromise through multi-turn debate?
- What role does diplomatic language play in persuasion?
- How do power dynamics emerge from position statements?

### 3. Policy Analysis Applications

#### Scenario Planning
**Use Case:** Explore "what-if" scenarios for diplomatic initiatives
```bash
# Test different resolution wordings
python scripts/run_motion.py 01_gaza_ceasefire_resolution
python scripts/run_motion.py 01_gaza_ceasefire_resolution_alternative_wording

# Compare outcomes
python scripts/compare_motions.py 01_gaza_ceasefire_resolution 01_gaza_ceasefire_resolution_alternative_wording
```

**Use Cases:**
- Draft resolution language for maximum support
- Identify contentious clauses that could be amended
- Test diplomatic messaging strategies
- Assess feasibility of proposed initiatives

#### Relationship Impact Assessment
**Use Case:** Understand how policy positions affect bilateral relations
```bash
# Full bilateral analysis
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution

# Generate relationship network visualization
python scripts/visualize_relationships.py 01_gaza_ceasefire_resolution
```

**Applications:**
- Assess diplomatic cost of taking specific positions
- Identify relationships at risk from policy stance
- Find opportunities for relationship improvement
- Plan diplomatic outreach strategies

### 4. Journalism and Media Applications

#### Background Research
**Use Case:** Understand country positions for reporting on UN proceedings
```bash
# Quick overview of expected positions
python scripts/run_motion.py 05_upcoming_un_resolution --sample 30

# Get detailed analysis
python scripts/generate_comprehensive_analysis.py 05_upcoming_un_resolution
```

**Media Use Cases:**
- Predict voting outcomes before actual UN votes
- Understand historical context of country positions
- Generate background material for news articles
- Create data visualizations for reporting

#### Fact-Checking
**Use Case:** Compare AI predictions with actual UN voting records
```python
import json

# Load AI simulation results
with open('tasks/reactions/01_gaza_ceasefire_resolution_latest.json') as f:
    ai_votes = json.load(f)

# Load actual UN voting record
with open('data/actual_votes/01_gaza_ceasefire_resolution.json') as f:
    actual_votes = json.load(f)

# Compare accuracy
python scripts/compare_predictions.py ai_votes actual_votes
```

### 5. Business and Strategy Applications

#### Market Risk Assessment
**Use Case:** Assess geopolitical risk for business planning
```bash
# Analyze how sanctions resolution might affect markets
python scripts/run_motion.py 06_economic_sanctions_resolution

# Identify countries likely to support/oppose
python scripts/analyze_vote_patterns.py 06_economic_sanctions_resolution --focus economic
```

**Applications:**
- Assess political risk in target markets
- Understand government policy trajectories
- Plan for diplomatic tensions
- Identify regulatory risks

#### Supply Chain Planning
**Use Case:** Anticipate geopolitical disruptions
```python
# Test resolution on maritime security
python scripts/run_motion.py 07_maritime_security_treaty

# Analyze impact on key shipping routes
python scripts/analyze_geographic_impact.py 07_maritime_security_treaty
```

## Data Integration Opportunities

### 1. Real UN Voting Data

#### Historical Voting Records
**Integration:** Import actual UN voting records for validation and training

```python
# Example integration
import json

class VotingDataset:
    def __init__(self, ai_results_path, real_votes_path):
        with open(ai_results_path) as f:
            self.ai_votes = json.load(f)
        with open(real_votes_path) as f:
            self.real_votes = json.load(f)

    def calculate_accuracy(self):
        """Compare AI predictions with actual votes"""
        correct = 0
        total = len(self.real_votes)

        for country in self.real_votes:
            ai_vote = self.get_ai_vote(country['name'])
            if ai_vote == country['vote']:
                correct += 1

        return (correct / total) * 100

    def identify_discrepancies(self):
        """Find where AI predictions differ from reality"""
        discrepancies = []
        for country in self.real_votes:
            ai_vote = self.get_ai_vote(country['name'])
            if ai_vote != country['vote']:
                discrepancies.append({
                    'country': country['name'],
                    'ai_vote': ai_vote,
                    'real_vote': country['vote'],
                    'difference': self.explain_difference(country['name'])
                })
        return discrepancies
```

**Data Sources:**
- UN Digital Library: https://digitallibrary.un.org/
- UN Voting Data API: https://api.un.org/
- Academic datasets (e.g., Erik Voeten's UN voting data)

#### Integration Benefits:
- Validate AI agent accuracy
- Fine-tune agent prompts based on real voting patterns
- Create training datasets for improved models
- Build historical voting analysis tools

### 2. Economic and Trade Data

#### World Bank / IMF Data
**Integration:** Incorporate economic indicators into agent decision-making

```python
# Enhanced agent with economic context
import wbdata
import datetime

class EconomicAwareAgent:
    def __init__(self, country_code, system_prompt):
        self.country = country_code
        self.system_prompt = system_prompt
        self.economic_data = self.fetch_economic_data()

    def fetch_economic_data(self):
        """Get relevant economic indicators"""
        indicators = {
            'NY.GDP.MKTP.CD': 'gdp',
            'FP.CPI.TOTL.ZG': 'inflation',
            'NE.TRD.GNFS.ZS': 'trade_pct_gdp'
        }

        data = wbdata.get_dataframe(
            indicators,
            country=self.country,
            date=(datetime.datetime(2023, 1, 1), datetime.datetime(2025, 1, 1))
        )
        return data

    def enhanced_context(self, motion):
        """Add economic context to voting decision"""
        context = f"""
        Current Economic Context for {self.country}:
        - GDP: ${self.economic_data['gdp'].iloc[-1]:,.0f}
        - Inflation: {self.economic_data['inflation'].iloc[-1]:.1f}%
        - Trade as % of GDP: {self.economic_data['trade_pct_gdp'].iloc[-1]:.1f}%

        Consider how this motion might affect your economic interests.
        """
        return self.system_prompt + context
```

**Data Sources:**
- World Bank Open Data: https://data.worldbank.org/
- IMF Data: https://www.imf.org/en/Data
- WTO Statistics: https://www.wto.org/statistics

**Use Cases:**
- Understand economic motivations for votes
- Analyze trade relationship impacts
- Assess sanctions effectiveness
- Model economic coercion

### 3. Diplomatic Relations Data

#### GDELT Global Events Database
**Integration:** Track real-world diplomatic events and tensions

```python
from gdeltdoc import GdeltDoc, Filters

class DiplomaticContextAgent:
    def __init__(self, country_name):
        self.country = country_name
        self.gd = GdeltDoc()

    def get_recent_relations(self, other_country, days=30):
        """Fetch recent diplomatic events between countries"""
        f = Filters(
            keyword=f"{self.country} {other_country}",
            start_date="2025-09-01",
            end_date="2025-10-01"
        )

        articles = self.gd.article_search(f)

        # Analyze sentiment and tone
        positive_events = []
        negative_events = []

        for article in articles:
            if self.is_positive(article['tone']):
                positive_events.append(article)
            else:
                negative_events.append(article)

        return {
            'positive_events': len(positive_events),
            'negative_events': len(negative_events),
            'overall_tone': self.calculate_relationship_tone(articles)
        }
```

**Data Sources:**
- GDELT Project: https://www.gdeltproject.org/
- ACLED (conflict data): https://acleddata.com/
- ICEWS (political events): https://dataverse.harvard.edu/dataverse/icews

**Use Cases:**
- Real-time relationship assessment
- Conflict prediction
- Alliance formation analysis
- Crisis response simulation

### 4. News and Media Data

#### NewsAPI Integration
**Integration:** Provide agents with recent news context

```python
from newsapi import NewsApiClient

class NewsAwareAgent:
    def __init__(self, country, api_key):
        self.country = country
        self.newsapi = NewsApiClient(api_key=api_key)

    def get_recent_headlines(self, topic, days=7):
        """Fetch recent news about topic from country's perspective"""
        sources = self.get_country_news_sources(self.country)

        articles = self.newsapi.get_everything(
            q=topic,
            sources=sources,
            from_param=f"{days} days ago",
            language=self.get_country_language(self.country),
            sort_by='relevancy'
        )

        return self.summarize_coverage(articles)

    def enhanced_voting_context(self, motion):
        """Add recent news context to voting decision"""
        relevant_news = self.get_recent_headlines(
            self.extract_topic(motion['text']),
            days=30
        )

        context = f"""
        Recent media coverage in {self.country}:
        {relevant_news}

        Consider how public opinion and media framing in your country
        might influence your government's position on this issue.
        """
        return context
```

**Data Sources:**
- NewsAPI: https://newsapi.org/
- MediaCloud: https://mediacloud.org/
- GDELT News API: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/

### 5. Social Media and Public Opinion

#### Twitter/X API Integration
**Integration:** Gauge public sentiment on international issues

```python
import tweepy

class PublicOpinionAgent:
    def __init__(self, country, twitter_api):
        self.country = country
        self.api = twitter_api

    def analyze_public_sentiment(self, motion_topic):
        """Analyze public opinion in country on motion topic"""
        # Search tweets from country
        tweets = self.api.search_tweets(
            q=f"{motion_topic} geocode:{self.get_coordinates(self.country)},1000km",
            lang=self.get_language(self.country),
            count=100
        )

        # Sentiment analysis
        sentiments = [self.analyze_sentiment(tweet.text) for tweet in tweets]

        return {
            'support': sum(1 for s in sentiments if s > 0.3),
            'oppose': sum(1 for s in sentiments if s < -0.3),
            'neutral': sum(1 for s in sentiments if -0.3 <= s <= 0.3),
            'average_sentiment': sum(sentiments) / len(sentiments)
        }

    def incorporate_public_opinion(self, motion):
        """Add public opinion context to agent decision"""
        sentiment = self.analyze_public_sentiment(motion['topic'])

        if self.is_democracy(self.country):
            weight = 0.7  # High weight for democracies
        else:
            weight = 0.3  # Lower weight for non-democracies

        return sentiment, weight
```

**Data Sources:**
- Twitter/X API: https://developer.twitter.com/
- Reddit API: https://www.reddit.com/dev/api/
- Public opinion polls: Pew Research, Gallup International

### 6. Geographic and Conflict Data

#### Armed Conflict Location & Event Data (ACLED)
**Integration:** Real-time conflict data for informed voting

```python
import acled

class ConflictAwareAgent:
    def __init__(self, country_code):
        self.country = country_code
        self.acled_client = acled.ACLEDClient()

    def get_conflict_exposure(self, region, months=6):
        """Assess conflict events in region"""
        events = self.acled_client.get_events(
            country=self.country,
            start_date=f"-{months}m",
            event_types=['battles', 'violence_against_civilians', 'explosions']
        )

        return {
            'total_events': len(events),
            'fatalities': sum(e['fatalities'] for e in events),
            'event_types': self.categorize_events(events),
            'risk_level': self.calculate_risk(events)
        }

    def assess_motion_relevance(self, motion):
        """Determine if motion addresses country's security concerns"""
        conflict_data = self.get_conflict_exposure(self.country)

        if conflict_data['risk_level'] == 'high' and 'ceasefire' in motion['text'].lower():
            return 'highly_relevant'
        else:
            return 'moderately_relevant'
```

**Data Sources:**
- ACLED: https://acleddata.com/
- Uppsala Conflict Data Program: https://ucdp.uu.se/
- International Crisis Group: https://www.crisisgroup.org/

### 7. RAG (Retrieval-Augmented Generation)

#### Document Database Integration
**Integration:** Query relevant UN documents and resolutions

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader

class RAGEnhancedAgent:
    def __init__(self, country, documents_path):
        self.country = country
        self.vectorstore = self.build_vectorstore(documents_path)

    def build_vectorstore(self, path):
        """Create vector database of UN documents"""
        # Load all UN resolutions, treaties, etc.
        loader = UnstructuredPDFLoader(path)
        documents = loader.load()

        # Create embeddings and store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(documents, embeddings)

        return vectorstore

    def query_relevant_precedents(self, motion):
        """Find similar past resolutions"""
        similar_docs = self.vectorstore.similarity_search(
            motion['text'],
            k=5
        )

        # Extract voting patterns from similar resolutions
        precedents = self.extract_voting_patterns(similar_docs, self.country)

        return precedents

    def enhanced_prompt(self, motion):
        """Add historical precedents to prompt"""
        precedents = self.query_relevant_precedents(motion)

        context = f"""
        Relevant historical context:
        Your country previously voted as follows on similar issues:
        {precedents}

        Consider this historical voting pattern when deciding on the current motion.
        """
        return context
```

**Document Sources:**
- UN Digital Library
- Official UN document system
- Treaty databases
- Historical resolution archives

## Future Enhancements

### Planned Features
1. **Real-time Debate Simulation**: Multi-turn agent interactions
2. **Coalition Formation**: Agents negotiate and form voting blocs
3. **Amendment Proposals**: Agents can propose changes to resolutions
4. **Regional Bloc Analysis**: Study voting patterns by geographic region
5. **Time Series Tracking**: Track relationship changes over multiple motions
6. **Web Interface**: Browser-based simulation viewer
7. **Visualization**: Network graphs of relationships and voting patterns
8. **Economic Integration**: World Bank/IMF data in voting decisions
9. **Conflict Data Integration**: ACLED/UCDP data for security issues
10. **RAG Enhancement**: Query historical UN documents for precedents

### Extensibility Points
- Custom analysis scripts in `scripts/`
- New motion types (debates, appointments, budget votes)
- Alternative agent architectures (fine-tuned models, RAG systems)
- Integration with real UN data and documents
- External data source connectors (economic, conflict, news)
- Real-time event monitoring and response
- Multi-language support for global agents

## Security Considerations

### API Keys
- Never commit API keys to git
- Use `.env` files (gitignored)
- Support for environment variables

### Content Safety
- Agent prompts designed for diplomatic discourse
- No generation of harmful content
- Educational and research purposes only

### Data Privacy
- No personal data collection
- All simulations are synthetic
- Results are educational/research only

## Testing

### Unit Tests
```bash
# Test motion loading
python -m pytest tests/test_motion_loader.py

# Test agent system
python -m pytest tests/test_agents.py
```

### Integration Tests
```bash
# Test full simulation with sample
python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 5

# Test analysis pipeline
python scripts/analyze_israel_bilateral_impact.py 01_gaza_ceasefire_resolution --sample 5
```

### Validation
- JSON schema validation for all outputs
- Vote validation (yes/no/abstain only)
- Country name consistency checks

## Contributing

### Adding New Agents
1. Create directory: `agents/representatives/{country-slug}/`
2. Write `system-prompt.md` with foreign policy framework
3. Test with sample motion
4. Submit PR with agent

### Adding New Motions
1. Create file: `tasks/motions/{id}_{slug}.md`
2. Format with preamble and operative clauses
3. Run simulation with --sample first
4. Submit PR with results

### Adding New Analysis
1. Create script in `scripts/`
2. Use existing JSON schemas for input/output
3. Add documentation to `docs/`
4. Update analysis_guide.md

## License

See [LICENSE](../LICENSE) for details.

## Disclaimer

This is an experimental simulation for research and educational purposes. AI agent positions do not represent actual government policies or diplomatic stances.
