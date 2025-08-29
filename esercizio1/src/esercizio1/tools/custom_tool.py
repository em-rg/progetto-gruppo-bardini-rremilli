"""
Custom tools module for the CrewAI Multi-Process Router System.

This module provides specialized tools for mathematical calculations and text processing.
It includes safe mathematical evaluation, text-to-number conversion, and supports
multiple languages for textual number representations.
"""

from typing import Type, Dict, Union
import re
import operator

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class MathCalculatorToolInput(BaseModel):
    """
    Input schema for MathCalculatorTool.
    
    Attributes:
        expression (str): Mathematical expression to calculate (e.g., '2 + 3 * 4').
    """
    expression: str = Field(..., description="Mathematical expression to calculate (e.g., '2 + 3 * 4')")


class MathCalculatorTool(BaseTool):
    """
    Safe mathematical expression calculator tool.
    
    This tool provides secure evaluation of mathematical expressions without the
    risks of code injection. It supports basic arithmetic operations, parentheses,
    and power operations while ensuring input validation and safe execution.
    
    Supported Operations:
        - Addition (+)
        - Subtraction (-)
        - Multiplication (*)
        - Division (/)
        - Power (^ or **)
        - Parentheses for grouping
    
    Safety Features:
        - Input validation using regex patterns
        - Prevention of code injection attacks
        - Error handling for invalid expressions
        - Division by zero protection
    """
    name: str = "Math Calculator"
    description: str = (
        "Safely evaluates mathematical expressions with basic arithmetic operations. "
        "Supports +, -, *, /, ^, and parentheses. Ensures safe calculation without code execution."
    )
    args_schema: Type[BaseModel] = MathCalculatorToolInput

    def _run(self, expression: str) -> str:
        """
        Execute the mathematical calculation.
        
        Args:
            expression (str): Mathematical expression to evaluate.
            
        Returns:
            str: Result of the calculation or error message.
            
        Examples:
            >>> tool = MathCalculatorTool()
            >>> tool._run("2 + 3 * 4")
            "Result: 14"
            >>> tool._run("10 / 0")
            "Error: Division by zero"
        """
        try:
            # Clean and validate the expression
            cleaned_expr = self._clean_expression(expression)
            
            if not self._is_safe_expression(cleaned_expr):
                return f"Error: Invalid or unsafe mathematical expression: {expression}"
            
            # Replace ^ with ** for Python power operator
            cleaned_expr = cleaned_expr.replace('^', '**')
            
            # Safe evaluation
            result = eval(cleaned_expr)
            return f"Result: {result}"
            
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error calculating expression '{expression}': {str(e)}"
    
    def _clean_expression(self, expression: str) -> str:
        """
        Clean the mathematical expression by removing whitespace.
        
        Args:
            expression (str): Raw mathematical expression.
            
        Returns:
            str: Cleaned expression without whitespace.
        """
        # Remove whitespace and convert to lowercase
        cleaned = expression.strip().replace(' ', '')
        return cleaned
    
    def _is_safe_expression(self, expression: str) -> bool:
        """
        Check if the expression contains only safe mathematical operations.
        
        Uses regex pattern matching to ensure the expression only contains
        allowed mathematical symbols and prevents code injection.
        
        Args:
            expression (str): Expression to validate.
            
        Returns:
            bool: True if expression is safe, False otherwise.
        """
        # Only allow numbers, operators, parentheses, and decimal points
        safe_pattern = r'^[0-9+\-*/^().]+$'
        return bool(re.match(safe_pattern, expression))


class TextToNumberToolInput(BaseModel):
    """
    Input schema for TextToNumberTool.
    
    Attributes:
        text (str): Text containing numbers written as words to be converted.
    """
    text: str = Field(..., description="Text containing numbers written as words")


class TextToNumberTool(BaseTool):
    """
    Text-to-number conversion tool for multilingual support.
    
    This tool converts textual number representations (written as words) to
    numerical digits. It supports both English and Italian number words and
    can handle complex expressions containing mixed text and mathematical operators.
    
    Supported Languages:
        - English: "one", "two", "three", "twenty", "hundred", etc.
        - Italian: "uno", "due", "tre", "venti", "cento", etc.
    
    Features:
        - Comprehensive number word dictionary
        - Multi-language support
        - Preserves non-number words in text
        - Error handling for conversion failures
    """
    name: str = "Text to Number Converter"
    description: str = (
        "Converts textual numbers (written as words) to numerical digits. "
        "Supports English and Italian number words."
    )
    args_schema: Type[BaseModel] = TextToNumberToolInput

    def _run(self, text: str) -> str:
        """
        Execute the text-to-number conversion.
        
        Args:
            text (str): Input text containing textual numbers.
            
        Returns:
            str: Text with number words converted to digits.
            
        Examples:
            >>> tool = TextToNumberTool()
            >>> tool._run("two plus three")
            "Converted text: 2 plus 3"
            >>> tool._run("due più tre")
            "Converted text: 2 più 3"
        """
        try:
            converted_text = self._convert_text_numbers(text)
            return f"Converted text: {converted_text}"
        except Exception as e:
            return f"Error converting text numbers: {str(e)}"

    def _get_word_to_num_dict(self) -> Dict[str, int]:
        """
        Get the comprehensive word-to-number mapping dictionary.
        
        Returns:
            Dict[str, int]: Dictionary mapping number words to their numerical values
                           for both English and Italian languages.
        """
        return {
            # English numbers
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
            'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
            'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000,
            
            # Italian numbers
            'uno': 1, 'due': 2, 'tre': 3, 'quattro': 4, 'cinque': 5,
            'sei': 6, 'sette': 7, 'otto': 8, 'nove': 9, 'dieci': 10,
            'undici': 11, 'dodici': 12, 'tredici': 13, 'quattordici': 14, 'quindici': 15,
            'sedici': 16, 'diciassette': 17, 'diciotto': 18, 'diciannove': 19, 'venti': 20,
            'trenta': 30, 'quaranta': 40, 'cinquanta': 50, 'sessanta': 60, 'settanta': 70,
            'ottanta': 80, 'novanta': 90, 'cento': 100, 'mille': 1000
        }

    def _convert_text_numbers(self, text: str) -> str:
        """
        Convert textual numbers to digits in the given text.
        
        Processes the input text word by word, identifying number words using
        the multilingual dictionary and converting them to their numerical
        equivalents while preserving other words unchanged.
        
        Args:
            text (str): Input text containing textual numbers.
            
        Returns:
            str: Text with number words converted to digits.
            
        Note:
            Punctuation is removed from words before lookup to improve
            matching accuracy.
        """
        word_to_num = self._get_word_to_num_dict()
        words = text.lower().split()
        converted_words = []
        
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w]', '', word)
            
            if clean_word in word_to_num:
                converted_words.append(str(word_to_num[clean_word]))
            else:
                converted_words.append(word)
        
        return ' '.join(converted_words)


class MyCustomToolInput(BaseModel):
    """
    Input schema for MyCustomTool (template/example tool).
    
    Attributes:
        argument (str): Generic argument for demonstration purposes.
    """
    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    """
    Template/example custom tool for demonstration purposes.
    
    This is a placeholder tool that serves as a template for creating
    new custom tools. It demonstrates the basic structure and interface
    required for CrewAI tools.
    
    Note:
        This tool is included for reference and should be replaced or
        extended with actual functionality as needed.
    """
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        """
        Execute the tool with the given argument.
        
        Args:
            argument (str): Input argument for the tool.
            
        Returns:
            str: Example output for demonstration purposes.
        """
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
