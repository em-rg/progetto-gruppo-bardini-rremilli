from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from esercizio1.tools.custom_tool import TextToNumberTool, MathCalculatorTool


@CrewBase
class MathTextCrew:
    """Math Text Crew for mathematical operations with textual numbers."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def text_number_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["text_number_parser"],
            tools=[TextToNumberTool()]
        )

    @agent
    def text_math_calculator(self) -> Agent:
        return Agent(
            config=self.agents_config["text_math_calculator"],
            tools=[MathCalculatorTool()]
        )

    @agent
    def text_result_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config["text_result_formatter"],
        )

    @task
    def parse_text_math_expression(self) -> Task:
        return Task(
            config=self.tasks_config["parse_text_math_expression"],
            agent=self.text_number_parser()
        )

    @task
    def calculate_text_math_result(self) -> Task:
        return Task(
            config=self.tasks_config["calculate_text_math_result"],
            agent=self.text_math_calculator(),
            context=[self.parse_text_math_expression()]
        )

    @task
    def format_text_math_result(self) -> Task:
        return Task(
            config=self.tasks_config["format_text_math_result"],
            agent=self.text_result_formatter(),
            context=[self.calculate_text_math_result()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Math Text Crew for textual number calculations"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
