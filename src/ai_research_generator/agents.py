
import os
from dotenv import load_dotenv
from crewai import Agent, LLM

from .tools import (
    duckduckgo_search,
    semantic_relevance_tool
)

load_dotenv()

gemini_llm = LLM(
    model="gemini/",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    timeout=120
)

# Agent 1: Research
Research_Agent = Agent(
    role="Research Specialist",
    goal="Collect relevant information about the given research topic.",
    backstory="You are an experienced web researcher.",
    tools=[duckduckgo_search],
    llm=gemini_llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
    max_iter=3
)

# Agent 2: Analyst
Analyst_Agent = Agent(
    role="Research Analyst",
    goal="Evaluate research sources and extract meaningful insights.",
    backstory=(
        "You are an analytical researcher skilled in "
        "semantic relevance evaluation, source comparison, "
        "trend identification and evidence analysis."
    ),
    tools=[semantic_relevance_tool],
    llm=gemini_llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
    max_iter=3
)

# Agent 3: Writer
Writer_Agent = Agent(
    role="Technical Report Writer",
    goal="Create a detailed and structured research report.",
    backstory="You are a professional technical report writer.",
    tools=[],
    llm=gemini_llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
    max_iter=2
)
