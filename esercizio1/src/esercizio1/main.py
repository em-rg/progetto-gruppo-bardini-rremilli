#!/usr/bin/env python
"""
Main module for the CrewAI Multi-Process Router System.

This module implements a sophisticated routing system that automatically classifies
user input and routes it to appropriate specialized crews for processing different
types of tasks: information retrieval (RAG), mathematical operations, and creative writing.
"""

from random import randint
from typing import Dict, Any

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from esercizio1.crews.poem_crew.poem_crew import PoemCrew
from esercizio1.crews.rag_crew.rag_crew import RagCrew
from esercizio1.crews.math_crew.math_crew import MathCrew
from esercizio1.crews.math_text_crew.math_text_crew import MathTextCrew
from esercizio1.routers.main_router import route_user_input


class MultiProcessState(BaseModel):
    """
    State model for the multi-process flow.
    
    This class defines the state variables that are shared across all steps
    of the flow execution, tracking user input, routing decisions, and results.
    
    Attributes:
        user_input (str): The original user input string.
        routing_info (Dict[str, Any]): Information about routing decisions including
            crew type and sub-categories.
        result (str): The final processed result from the selected crew.
        sentence_count (int): Number of sentences for poem generation (used by poem crew).
    """
    user_input: str = ""
    routing_info: Dict[str, Any] = {}
    result: str = ""
    sentence_count: int = 1


class MultiProcessFlow(Flow[MultiProcessState]):
    """
    Main flow orchestrator for the multi-process routing system.
    
    This class implements a CrewAI Flow that manages the entire process from
    user input collection through routing, processing, and result saving.
    It coordinates between different specialized crews based on input classification.
    
    The flow consists of four main steps:
    1. Get user input
    2. Route input to appropriate crew
    3. Process request with selected crew
    4. Save the result to file
    """

    @start()
    def get_user_input(self):
        """
        Get user input and initialize the flow state.
        
        This is the starting point of the flow. It prompts the user for input
        with a default fallback and stores the input in the flow state.
        
        Note:
            In a production application, this would typically receive input
            from a user interface rather than command line input.
        """
        print("Getting user input...")
        
        # In a real application, this would come from user interface
        # For demo purposes, you can modify this default input
        default_input = "Write a poem about artificial intelligence"
        
        self.state.user_input = input(f"Enter your request (default: '{default_input}'): ").strip()
        if not self.state.user_input:
            self.state.user_input = default_input
            
        print(f"User input: {self.state.user_input}")

    @listen(get_user_input)
    def route_input(self):
        """
        Route user input to the appropriate crew based on content analysis.
        
        Uses the main router to classify the user input and determine which
        specialized crew should handle the request. The routing decision is
        stored in the flow state for use in subsequent steps.
        
        The router can classify input into:
        - RAG: Information retrieval queries
        - MATH: Mathematical calculations (with sub-routing for numeric/textual)
        - POEM: Creative writing requests
        """
        print("Routing user input...")
        
        self.state.routing_info = route_user_input(self.state.user_input)
        print(f"Routing decision: {self.state.routing_info}")

    @listen(route_input)
    def process_request(self):
        """
        Process the user request using the appropriate specialized crew.
        
        Based on the routing decision, this method instantiates and executes
        the appropriate crew to handle the user's request. Each crew type
        requires different input parameters and handles different types of tasks.
        
        Crew Types:
        - rag_crew: Handles information retrieval and knowledge queries
        - math_crew: Processes numerical mathematical expressions
        - math_text_crew: Handles mathematical expressions with textual numbers
        - poem_crew: Creates creative content like poems and stories
        
        Raises:
            Exception: If crew execution fails, falls back to poem crew.
        """
        crew_type = self.state.routing_info.get("crew_type")
        user_input = self.state.user_input
        
        print(f"Processing request with {crew_type}...")
        
        if crew_type == "rag_crew":
            result = RagCrew().crew().kickoff(inputs={"query": user_input})
            
        elif crew_type == "math_crew":
            result = MathCrew().crew().kickoff(inputs={"math_expression": user_input})
            
        elif crew_type == "math_text_crew":
            result = MathTextCrew().crew().kickoff(inputs={"math_expression": user_input})
            
        elif crew_type == "poem_crew":
            # For poem crew, we need sentence count
            self.state.sentence_count = randint(1, 5)
            result = PoemCrew().crew().kickoff(inputs={"sentence_count": self.state.sentence_count})
            
        else:
            # Fallback to poem crew
            self.state.sentence_count = randint(1, 5)
            result = PoemCrew().crew().kickoff(inputs={"sentence_count": self.state.sentence_count})
        
        self.state.result = result.raw
        print(f"Process completed. Result: {self.state.result}")

    @listen(process_request)
    def save_result(self):
        """
        Save the processing result to a file.
        
        Creates a text file containing the user input, routing information,
        and the final result. The filename is based on the crew type that
        processed the request.
        
        File format includes:
        - Original user input
        - Crew type used
        - Complete routing information
        - Final processed result
        """
        crew_type = self.state.routing_info.get("crew_type", "unknown")
        filename = f"{crew_type}_result.txt"
        
        print(f"Saving result to {filename}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"User Input: {self.state.user_input}\n")
            f.write(f"Crew Type: {crew_type}\n")
            f.write(f"Routing Info: {self.state.routing_info}\n")
            f.write(f"Result:\n{self.state.result}")


def kickoff():
    """
    Main entry point for the multi-process flow application.
    
    Initializes and executes the MultiProcessFlow, which handles the complete
    workflow from user input to result processing and saving.
    
    This function is the primary way to run the application and is configured
    as a console script entry point in pyproject.toml.
    """
    multi_flow = MultiProcessFlow()
    multi_flow.kickoff()


def plot():
    """
    Generate and display a visual diagram of the flow structure.
    
    Creates a visual representation of the MultiProcessFlow showing the
    sequence of steps and their dependencies. Useful for understanding
    the flow architecture and debugging.
    
    Note:
        Requires appropriate plotting dependencies to be installed.
    """
    multi_flow = MultiProcessFlow()
    multi_flow.plot()


def demo_routing():
    """
    Demonstrate the routing system with predefined test inputs.
    
    Runs a series of test cases through the routing system to show how
    different types of user input are classified and routed to appropriate
    crews. This is useful for testing and demonstrating the system capabilities.
    
    Test cases include:
    - Information retrieval queries (routed to RAG crew)
    - Numerical mathematical expressions (routed to Math crew)
    - Textual mathematical expressions (routed to Math Text crew)
    - Creative writing requests (routed to Poem crew)
    """
    test_inputs = [
        "What is artificial intelligence?",
        "Calculate 15 + 27 * 3",
        "What is two plus three times five?",
        "Write a poem about the ocean",
        "Explain quantum computing",
        "Solve: twenty-five divided by five"
    ]
    
    print("=== ROUTING DEMO ===")
    for user_input in test_inputs:
        print(f"\nInput: {user_input}")
        routing_info = route_user_input(user_input)
        print(f"Route: {routing_info}")


if __name__ == "__main__":
    # Uncomment the function you want to run
    kickoff()
    # demo_routing()
    # plot()


if __name__ == "__main__":
    kickoff()
