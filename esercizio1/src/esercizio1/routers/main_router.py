"""
Main router module for the CrewAI Multi-Process Router System.

This module implements intelligent routing functionality that classifies user input
and routes it to appropriate specialized crews. It includes both AI-based classification
for general intent and rule-based classification for mathematical expressions.
"""

import re
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process


class MainRouter:
    """
    Main router crew that classifies user input using AI agents.
    
    This class uses a specialized AI agent to analyze user input and classify it
    into one of three main categories: RAG (information retrieval), MATH 
    (mathematical operations), or POEM (creative writing).
    
    The classification is performed by an expert agent that understands user
    intent and can distinguish between different types of requests.
    
    Attributes:
        input_classifier_agent (Agent): AI agent specialized in input classification.
    """
    
    def __init__(self):
        """
        Initialize the MainRouter with a specialized classification agent.
        
        Creates an AI agent that is expert at understanding user intent and
        classifying requests into appropriate categories.
        """
        self.input_classifier_agent = Agent(
            role="Input Classification Expert",
            goal="Classify user input into one of three categories: RAG (information retrieval), MATH (mathematical operations), or POEM (poetry/creative writing)",
            backstory="You are an expert at understanding user intent and classifying requests. You can distinguish between information retrieval requests, mathematical calculations, and creative writing requests.",
            verbose=True
        )

    def classify_input_task(self, user_input: str) -> Task:
        """
        Create a classification task for the given user input.
        
        Args:
            user_input (str): The user's input string to classify.
            
        Returns:
            Task: A CrewAI task configured to classify the input into RAG, MATH, or POEM.
        """
        return Task(
            description=f"""
            Analyze the user input: '{user_input}'
            
            Classify this input into exactly one of these categories:
            - RAG: If the user is asking for information, facts, explanations, or knowledge retrieval
            - MATH: If the user is asking for mathematical calculations, operations, or solving equations
            - POEM: If the user is asking for poetry, creative writing, stories, or similar creative content
            
            Return ONLY the category name (RAG, MATH, or POEM) with no additional text.
            """,
            expected_output="A single word: either 'RAG', 'MATH', or 'POEM'",
            agent=self.input_classifier_agent
        )

    def crew(self, user_input: str) -> Crew:
        """
        Create a crew to perform input classification.
        
        Args:
            user_input (str): The user's input string to classify.
            
        Returns:
            Crew: A CrewAI crew configured to classify the input.
        """
        return Crew(
            agents=[self.input_classifier_agent],
            tasks=[self.classify_input_task(user_input)],
            process=Process.sequential,
            verbose=True
        )


class MathRouter:
    """
    Router to determine if mathematical input contains numerical digits or textual numbers.
    
    This class implements rule-based classification for mathematical expressions,
    determining whether numbers are represented as digits (e.g., "15 + 27") or
    as words (e.g., "fifteen plus twenty-seven"). It supports both English and
    Italian number words.
    
    The classification is based on pattern matching using regular expressions
    to detect different number representations in the input text.
    
    Attributes:
        number_patterns (List[str]): Regex patterns for detecting numerical digits.
        text_number_patterns (List[str]): Regex patterns for detecting textual numbers.
    """
    
    def __init__(self):
        """
        Initialize the MathRouter with pattern definitions for number detection.
        
        Sets up regex patterns for identifying both numerical digits and textual
        number representations in multiple languages (English and Italian).
        """
        self.number_patterns = [
            r'\d+',  # digits
            r'\d+\.\d+',  # decimals
            r'\d+/\d+',  # fractions
        ]
        
        self.text_number_patterns = [
            r'\b(zero|one|two|three|four|five|six|seven|eight|nine|ten)\b',
            r'\b(eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\b',
            r'\b(thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b',
            r'\b(primo|secondo|terzo|quarto|quinto|sesto|settimo|ottavo|nono|decimo)\b',  # Italian numbers
            r'\b(uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci)\b',
            r'\b(undici|dodici|tredici|quattordici|quindici|sedici|diciassette|diciotto|diciannove|venti)\b'
        ]
    
    def classify_math_input(self, user_input: str) -> str:
        """
        Classify mathematical input as either 'NUMERIC' or 'TEXTUAL' based on number representation.
        
        Analyzes the input to determine whether numbers are represented as digits
        or as words. Uses pattern matching to identify different number formats
        and applies precedence rules when both types are present.
        
        Args:
            user_input (str): The mathematical input to classify.
            
        Returns:
            str: 'NUMERIC' if input contains numerical digits, 'TEXTUAL' if contains text numbers.
            
        Examples:
            >>> math_router = MathRouter()
            >>> math_router.classify_math_input("15 + 27")
            'NUMERIC'
            >>> math_router.classify_math_input("fifteen plus twenty-seven")
            'TEXTUAL'
        """
        user_input_lower = user_input.lower()
        
        # Check for numerical patterns
        has_numbers = any(re.search(pattern, user_input) for pattern in self.number_patterns)
        
        # Check for textual number patterns
        has_text_numbers = any(re.search(pattern, user_input_lower) for pattern in self.text_number_patterns)
        
        if has_numbers and not has_text_numbers:
            return "NUMERIC"
        elif has_text_numbers and not has_numbers:
            return "TEXTUAL"
        elif has_numbers and has_text_numbers:
            # If both are present, prioritize numeric
            return "NUMERIC"
        else:
            # Default to numeric if no clear pattern
            return "NUMERIC"


def route_user_input(user_input: str) -> Dict[str, Any]:
    """
    Main routing function that determines which crew to use based on user input.
    
    This function orchestrates the complete routing process by first classifying
    the general intent of the user input, then applying additional sub-classification
    for mathematical expressions to determine the most appropriate crew.
    
    Args:
        user_input (str): The user's input string to route.
        
    Returns:
        Dict[str, Any]: Dictionary containing routing information with keys:
            - user_input: Original input string
            - main_category: Primary classification (RAG, MATH, POEM)
            - crew_type: Specific crew to handle the request
            - sub_category: Additional classification for math inputs (NUMERIC/TEXTUAL)
            
    Examples:
        >>> route_user_input("What is AI?")
        {'user_input': 'What is AI?', 'main_category': 'RAG', 'crew_type': 'rag_crew', 'sub_category': None}
        
        >>> route_user_input("Calculate 15 + 27")
        {'user_input': 'Calculate 15 + 27', 'main_category': 'MATH', 'crew_type': 'math_crew', 'sub_category': 'NUMERIC'}
    """
    
    routing_info = {
        "user_input": user_input,
        "main_category": None,
        "crew_type": None,
        "sub_category": None
    }
    
    # Simple pattern-based classification (fallback when no API key available)
    user_input_lower = user_input.lower()
    
    # Check for mathematical patterns
    math_patterns = [
        r'\d+\s*[\+\-\*/\^]\s*\d+',  # basic math operations
        r'\b(calculate|compute|solve|math|plus|minus|times|divided|add|subtract|multiply|divide)\b',
        r'\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)\b',
        r'\b(uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|venti|trenta|quaranta|cinquanta|sessanta|settanta|ottanta|novanta|cento|mille)\b'
    ]
    
    # Check for creative writing patterns
    poem_patterns = [
        r'\b(poem|poetry|verse|rhyme|haiku|sonnet|ballad|limerick)\b',
        r'\b(write|create|compose|craft)\b.*\b(poem|story|song|verse|rhyme)\b',
        r'\b(filastrocca|poesia|verso|rima)\b'
    ]
    
    # Check for information/knowledge patterns
    rag_patterns = [
        r'\b(what|who|where|when|why|how|explain|describe|tell me about|information about)\b',
        r'\b(define|definition|meaning|concept|theory|principle)\b',
        r'\b(history|background|overview|summary)\b',
        r'\b(cos\'è|chi è|dove|quando|perché|come|spiega|descrivi|dimmi)\b'
    ]
    
    is_math = any(re.search(pattern, user_input_lower) for pattern in math_patterns)
    is_poem = any(re.search(pattern, user_input_lower) for pattern in poem_patterns)
    is_rag = any(re.search(pattern, user_input_lower) for pattern in rag_patterns)
    
    # Determine main category
    if is_math and not is_poem and not is_rag:
        main_category = "MATH"
    elif is_poem and not is_math:
        main_category = "POEM"
    elif is_rag and not is_math and not is_poem:
        main_category = "RAG"
    else:
        # Use AI-based classification if available
        try:
            main_router = MainRouter()
            classification_result = main_router.crew(user_input).kickoff()
            main_category = classification_result.raw.strip().upper()
        except Exception as e:
            print(f"AI classification failed ({e}), using pattern-based fallback")
            # Fallback logic
            if is_math:
                main_category = "MATH"
            elif is_poem:
                main_category = "POEM"
            elif is_rag:
                main_category = "RAG"
            else:
                main_category = "POEM"  # Default fallback
    
    routing_info["main_category"] = main_category
    
    if main_category == "RAG":
        routing_info["crew_type"] = "rag_crew"
        
    elif main_category == "MATH":
        # Further classify math input
        math_router = MathRouter()
        math_sub_category = math_router.classify_math_input(user_input)
        routing_info["sub_category"] = math_sub_category
        
        if math_sub_category == "NUMERIC":
            routing_info["crew_type"] = "math_crew"
        else:  # TEXTUAL
            routing_info["crew_type"] = "math_text_crew"
            
    elif main_category == "POEM":
        routing_info["crew_type"] = "poem_crew"
        
    else:
        # Default fallback
        routing_info["crew_type"] = "poem_crew"
    
    return routing_info
