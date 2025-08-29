from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class RagCrew:
    """RAG (Retrieval Augmented Generation) Crew for information retrieval and knowledge-based queries."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def knowledge_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["knowledge_researcher"],
        )

    @agent
    def information_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config["information_synthesizer"],
        )

    @task
    def research_information(self) -> Task:
        return Task(
            config=self.tasks_config["research_information"],
            agent=self.knowledge_researcher()
        )

    @task
    def synthesize_answer(self) -> Task:
        return Task(
            config=self.tasks_config["synthesize_answer"],
            agent=self.information_synthesizer(),
            context=[self.research_information()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the RAG Crew for information retrieval and synthesis"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
