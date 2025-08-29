#!/usr/bin/env python
"""
Test script for the CrewAI Multi-Process Router System
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from esercizio1.routers.main_router import route_user_input, MathRouter
from esercizio1.tools.custom_tool import MathCalculatorTool, TextToNumberTool


def test_routing():
    """Test the routing functionality"""
    print("=== TESTING ROUTING SYSTEM ===\n")
    
    test_cases = [
        ("What is artificial intelligence?", "rag_crew"),
        ("Calculate 15 + 27 * 3", "math_crew"),
        ("What is two plus three times five?", "math_text_crew"),
        ("Write a poem about the ocean", "poem_crew"),
        ("Explain quantum computing", "rag_crew"),
        ("Solve: twenty-five divided by five", "math_text_crew"),
        ("How does photosynthesis work?", "rag_crew"),
        ("Compute 100 / 5 + 2", "math_crew"),
        ("Tell me about the history of Rome", "rag_crew"),
        ("Create a haiku about stars", "poem_crew")
    ]
    
    for user_input, expected_crew in test_cases:
        routing_info = route_user_input(user_input)
        actual_crew = routing_info.get("crew_type")
        
        status = "✓" if actual_crew == expected_crew else "✗"
        print(f"{status} Input: '{user_input}'")
        print(f"   Expected: {expected_crew}, Got: {actual_crew}")
        if routing_info.get("sub_category"):
            print(f"   Sub-category: {routing_info['sub_category']}")
        print()


def test_math_router():
    """Test the math sub-router"""
    print("=== TESTING MATH SUB-ROUTER ===\n")
    
    math_router = MathRouter()
    
    test_cases = [
        ("15 + 27 * 3", "NUMERIC"),
        ("two plus three times five", "TEXTUAL"),
        ("100 / 5 + 2", "NUMERIC"),
        ("twenty-five divided by five", "TEXTUAL"),
        ("due più tre", "TEXTUAL"),
        ("5 * 6 - 2", "NUMERIC"),
        ("ten minus four", "TEXTUAL")
    ]
    
    for expression, expected_type in test_cases:
        result = math_router.classify_math_input(expression)
        status = "✓" if result == expected_type else "✗"
        print(f"{status} '{expression}' → {result} (expected: {expected_type})")


def test_tools():
    """Test the custom tools"""
    print("\n=== TESTING CUSTOM TOOLS ===\n")
    
    # Test Math Calculator Tool
    print("Testing Math Calculator Tool:")
    calc_tool = MathCalculatorTool()
    
    calc_tests = [
        "2 + 3",
        "10 * 5 - 2",
        "100 / 4",
        "(5 + 3) * 2",
        "2^3"
    ]
    
    for expr in calc_tests:
        result = calc_tool._run(expr)
        print(f"  {expr} = {result}")
    
    # Test Text to Number Tool
    print("\nTesting Text to Number Tool:")
    text_tool = TextToNumberTool()
    
    text_tests = [
        "two plus three",
        "five times ten",
        "due più tre",
        "twenty minus five"
    ]
    
    for text in text_tests:
        result = text_tool._run(text)
        print(f"  '{text}' → {result}")


if __name__ == "__main__":
    try:
        test_routing()
        test_math_router()
        test_tools()
        print("=== ALL TESTS COMPLETED ===")
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
