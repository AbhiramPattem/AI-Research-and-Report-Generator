
from crewai import Task


def create_research_task(agent, topic):

    return Task(
        description="""
        Research the following topic:

        {topic}

        Instructions:
        1. Search the web using DuckDuckGo.
        2. Collect at least 5 relevant sources.
        3. Extract each source's title, URL and description.
        4. Return ONLY a valid JSON list.

        Required JSON structure:

        [
            {
                "title": "Source title",
                "url": "https://example.com",
                "description": "Source description"
            }
        ]

        Do not include Markdown fences or explanations outside the JSON.
        """,
        expected_output="A valid JSON list containing research sources.",
        agent=agent
    )


def create_analysis_task(agent, topic, research_task):

    return Task(
        description="""
        Analyze the research collected for:

        {topic}

        Use the research results provided in the previous task.

        Instructions:

        1. Call the Python Semantic Relevance Evaluation tool
           exactly once, passing:
           - The research topic.
           - The complete research JSON returned by the Research Agent.

        2. Examine the relevance scores returned by the tool.

        3. Identify the most relevant findings.

        4. Compare information across different sources.

        5. Identify common trends and patterns.

        6. Identify agreements and contradictions.

        7. Identify research gaps and limitations.

        8. Produce a structured analysis.

        Important:
        - Do not invent research findings.
        - Do not treat semantic similarity as factual accuracy.
        - Do not treat relevance scores as source credibility scores.
        - Preserve source URLs.
        """,
        expected_output=(
            "A structured research analysis containing "
            "relevant findings, comparisons, trends, "
            "contradictions and research gaps."
        ),
        agent=agent,
        context=[research_task]
    )


def create_writing_task(agent, topic, research_task, analysis_task):

    return Task(
        description="""
        Create a comprehensive research report about:

        {topic}

        Use the research sources and analysis from the
        previous tasks.

        Structure the report using these sections:

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

        Instructions:
        - Write in professional language.
        - Use clear headings and subheadings.
        - Preserve source URLs in references.
        - Do not fabricate information.
        - Do not introduce unsupported claims.
        - Return the report in Markdown format.
        """,
        expected_output="A complete Markdown research report.",
        agent=agent,
        context=[research_task, analysis_task]
    )
