# AI Research & Report Generator

An AI-powered multi-agent application built using **CrewAI** that automates web research, evaluates the relevance of collected information, and generates structured research reports in Markdown format.

The project uses three specialized AI agents working together in a sequential workflow, with Python-based semantic similarity evaluation to improve the relevance of research sources.

## Features

- **Automated Web Research:** Searches the web using DuckDuckGo and collects relevant information.
- **Semantic Relevance Evaluation:** Uses Sentence Transformers to calculate semantic similarity between the research topic and collected sources.
- **AI-Powered Analysis:** Identifies key findings, trends, comparisons, contradictions, and research gaps.
- **Automated Report Generation:** Produces structured Markdown research reports.
- **Multi-Agent Architecture:** Uses CrewAI to coordinate multiple specialized agents in a single sequential workflow.
- **Flexible LLM Integration:** Supports compatible LLM providers through CrewAI and LiteLLM, including OpenRouter.

## Architecture

The application consists of three AI agents operating within one Crew using a sequential process.

```text
             User Input
                  |
                  v
          Research Topic
                  |
                  v
       +---------------------+
       |   Research Agent    |
       +---------------------+
                  |
                  v
          DuckDuckGo Search
                  |
                  v
         Research Sources
                  |
                  v
       +---------------------+
       |    Analyst Agent    |
       +---------------------+
                  |
                  v
       Python Semantic
       Relevance Evaluation
                  |
                  v
          Research Analysis
                  |
                  v
       +---------------------+
       |    Writer Agent     |
       +---------------------+
                  |
                  v
          Final Markdown
             Report
                  |
                  v
          research_report.md
```

### 1. Research Agent

**Responsibility:** Collect relevant information about the given research topic.

- Uses DuckDuckGo to search the web.
- Collects source titles, URLs, and descriptions.
- Returns research results in JSON format.

### 2. Analyst Agent

**Responsibility:** Evaluate the collected research and extract meaningful insights.

- Uses a Python-based semantic relevance evaluation tool.
- Compares the research topic with collected source descriptions.
- Calculates cosine similarity scores using Sentence Transformers.
- Identifies important findings, trends, agreements, contradictions, and research gaps.

**Semantic Relevance Evaluation:**

The project uses `all-MiniLM-L6-v2` to convert text into embeddings and calculate cosine similarity.

These scores indicate semantic similarity, not factual accuracy or source credibility.

### 3. Writer Agent

**Responsibility:** Generate a comprehensive research report.

- Uses research findings and the analyst's output.
- Organizes information into structured sections.
- Preserves source URLs.
- Generates the final report in Markdown format.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| CrewAI | Multi-agent orchestration |
| LiteLLM | LLM provider integration |
| OpenRouter | Access to hosted language models |
| DuckDuckGo Search (`ddgs`) | Web research |
| Sentence Transformers | Semantic embeddings |
| PyTorch | Embedding model execution |
| python-dotenv | Environment variable management |
| uv | Python dependency and environment management |

## Project Structure

```text
AI-Research-Report-Generator/
│
├── src/
│   └── ai_research_generator/
│       ├── __init__.py
│       ├── main.py
│       ├── agents.py
│       ├── tasks.py
│       ├── crew.py
│       └── tools.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

| File | Description |
|---|---|
| `main.py` | Application entry point; accepts the research topic and saves the report. |
| `agents.py` | Defines the Research, Analyst, and Writer agents and their LLM configuration. |
| `tasks.py` | Defines the tasks assigned to each agent. |
| `tools.py` | Contains DuckDuckGo search and semantic relevance evaluation tools. |
| `crew.py` | Creates and executes the single sequential Crew. |

## Prerequisites

Before running the project, install:

- Python 3.12 or later.
- [uv](https://docs.astral.sh/uv/).
- An API key from a supported LLM provider, such as [OpenRouter](https://openrouter.ai/).

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Research-Report-Generator.git
```

Navigate into the project directory:

```bash
cd AI-Research-Report-Generator
```

### 2. Install dependencies

If the repository contains `pyproject.toml` and `uv.lock`, run:

```bash
uv sync
```

If setting up the project dependencies for the first time, install the required packages using:

```bash
uv add "crewai[litellm]" ddgs sentence-transformers python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Get your API key from:

https://openrouter.ai/settings/keys

**Important:** Never commit your API key or `.env` file to GitHub.

### 4. Configure the LLM

Open `src/ai_research_generator/agents.py`.

Configure your preferred OpenRouter model:

```python
openrouter_llm = LLM(
    model="openrouter/PROVIDER/MODEL:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    timeout=120
)
```

Replace `PROVIDER/MODEL:free` with the exact model ID available on OpenRouter.

Choose a model that supports tool calling because the Research and Analyst agents need to execute their respective tools.

OpenRouter free models are subject to availability and usage limits.

## Running the Project

From the project root, execute:

```bash
uv run python -m ai_research_generator.main
```

Enter a research topic when prompted:

```text
Enter your research topic: Applications of Artificial Intelligence in Healthcare
```

The application will execute the following steps:

1. Research Agent searches the web.
2. Analyst Agent evaluates the relevance of the collected sources and analyzes the findings.
3. Writer Agent generates the final research report.

The generated report is saved in the project root as:

```text
research_report.md
```

You can open this Markdown file using VS Code or any Markdown editor.

## Example Output

For the research topic:

**Applications of Artificial Intelligence in Healthcare**

The generated report follows this structure:

1. Title
2. Executive Summary
3. Introduction
4. Background
5. Key Research Findings
6. Detailed Analysis
7. Trends and Comparisons
8. Limitations and Research Gaps
9. Conclusion
10. References

## Important Notes

- DuckDuckGo search results may vary between executions.
- Semantic similarity scores do not guarantee that a source is accurate or trustworthy.
- LLM API availability, rate limits, and pricing depend on the selected provider and model.
- The first semantic evaluation may take longer because the embedding model needs to be downloaded.
- The embedding model runs locally and does not require a separate embedding API key.


**Built with Python, CrewAI, and AI-powered research automation.**
