from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from esercizio1.tools.custom_tool import MathCalculatorTool


@CrewBase
class MathCrew:
    """Math Crew for numerical mathematical operations."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def math_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["math_parser"],
        )

    @agent
    def math_calculator(self) -> Agent:
        return Agent(
            config=self.agents_config["math_calculator"],
            tools=[MathCalculatorTool()]
        )

    @agent
    def result_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config["result_formatter"],
        )

    @task
    def parse_math_expression(self) -> Task:
        return Task(
            config=self.tasks_config["parse_math_expression"],
            agent=self.math_parser()
        )

    @task
    def calculate_result(self) -> Task:
        return Task(
            config=self.tasks_config["calculate_result"],
            agent=self.math_calculator(),
            context=[self.parse_math_expression()]
        )

    @task
    def format_result(self) -> Task:
        return Task(
            config=self.tasks_config["format_result"],
            agent=self.result_formatter(),
            context=[self.calculate_result()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Math Crew for numerical calculations"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
