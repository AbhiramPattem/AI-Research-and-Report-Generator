
from crewai import Crew, Process

from .agents import (
    Research_Agent,
    Analyst_Agent,
    Writer_Agent
)

from .tasks import (
    create_research_task,
    create_analysis_task,
    create_writing_task
)


def run_pipeline(topic):

    # Create all three tasks
    research_task = create_research_task(
        Research_Agent,
        topic
    )

    analysis_task = create_analysis_task(
        Analyst_Agent,
        topic,
        research_task
    )

    writing_task = create_writing_task(
        Writer_Agent,
        topic,
        research_task,
        analysis_task
    )

    # Crew containing all agents and tasks
    research_crew = Crew(
        agents=[
            Research_Agent,
            Analyst_Agent,
            Writer_Agent
        ],
        tasks=[
            research_task,
            analysis_task,
            writing_task
        ],
        process=Process.sequential,
        verbose=True
    )

    # Execute the entire workflow
    result = research_crew.kickoff(
        inputs={"topic": topic}
    )

    return result.raw
