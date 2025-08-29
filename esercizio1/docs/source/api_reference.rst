API Reference
=============

This section provides detailed API documentation for all modules, classes, and functions in the CrewAI Multi-Process Router System.

📚 **Modules Overview**
-----------------------

.. autosummary::
   :toctree: _autosummary
   :recursive:

   esercizio1.main
   esercizio1.routers.main_router
   esercizio1.crews.rag_crew.rag_crew
   esercizio1.crews.math_crew.math_crew
   esercizio1.crews.math_text_crew.math_text_crew
   esercizio1.crews.poem_crew.poem_crew
   esercizio1.tools.custom_tool

🎯 **Main Module**
------------------

.. automodule:: esercizio1.main
   :members:
   :undoc-members:
   :show-inheritance:

**Classes**

.. autoclass:: esercizio1.main.MultiProcessState
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: esercizio1.main.MultiProcessFlow
   :members:
   :undoc-members:
   :show-inheritance:

**Functions**

.. autofunction:: esercizio1.main.kickoff

.. autofunction:: esercizio1.main.plot

.. autofunction:: esercizio1.main.demo_routing

🧭 **Router Module**
--------------------

.. automodule:: esercizio1.routers.main_router
   :members:
   :undoc-members:
   :show-inheritance:

**Classes**

.. autoclass:: esercizio1.routers.main_router.MainRouter
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: esercizio1.routers.main_router.MathRouter
   :members:
   :undoc-members:
   :show-inheritance:

**Functions**

.. autofunction:: esercizio1.routers.main_router.route_user_input

🔍 **RAG Crew Module**
----------------------

.. automodule:: esercizio1.crews.rag_crew.rag_crew
   :members:
   :undoc-members:
   :show-inheritance:

**Classes**

.. autoclass:: esercizio1.crews.rag_crew.rag_crew.RagCrew
   :members:
   :undoc-members:
   :show-inheritance:

🧮 **Math Crew Module**
-----------------------

.. automodule:: esercizio1.crews.math_crew.math_crew
   :members:
   :undoc-members:
   :show-inheritance:

**Classes**

.. autoclass:: esercizio1.crews.math_crew.math_crew.MathCrew
   :members:
   :undoc-members:
   :show-inheritance:

📝 **Math Text Crew Module**
----------------------------

.. automodule:: esercizio1.crews.math_text_crew.math_text_crew
   :members:
   :undoc-members:
   :show-inheritance:

**Classes**

.. autoclass:: esercizio1.crews.math_text_crew.math_text_crew.MathTextCrew
   :members:
   :undoc-members:
   :show-inheritance:

🎨 **Poem Crew Module**
-----------------------

.. automodule:: esercizio1.crews.poem_crew.poem_crew
   :members:
   :undoc-members:
   :show-inheritance:

**Classes**

.. autoclass:: esercizio1.crews.poem_crew.poem_crew.PoemCrew
   :members:
   :undoc-members:
   :show-inheritance:

🛠️ **Tools Module**
-------------------

.. automodule:: esercizio1.tools.custom_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Tool Classes**

.. autoclass:: esercizio1.tools.custom_tool.MathCalculatorTool
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: esercizio1.tools.custom_tool.TextToNumberTool
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: esercizio1.tools.custom_tool.MyCustomTool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Schema Classes**

.. autoclass:: esercizio1.tools.custom_tool.MathCalculatorToolInput
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: esercizio1.tools.custom_tool.TextToNumberToolInput
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: esercizio1.tools.custom_tool.MyCustomToolInput
   :members:
   :undoc-members:
   :show-inheritance:

📋 **Type Definitions**
-----------------------

**Common Types**

.. code-block:: python

   from typing import Dict, Any, List, Optional, Union
   
   # Routing information dictionary
   RoutingInfo = Dict[str, Any]
   
   # User input string
   UserInput = str
   
   # Crew type identifier
   CrewType = str
   
   # Classification categories
   MainCategory = Literal["RAG", "MATH", "POEM"]
   MathSubCategory = Literal["NUMERIC", "TEXTUAL"]

**Flow State Schema**

.. code-block:: python

   class MultiProcessState(BaseModel):
       user_input: str = ""
       routing_info: Dict[str, Any] = {}
       result: str = ""
       sentence_count: int = 1

**Routing Response Schema**

.. code-block:: python

   RoutingResponse = {
       "user_input": str,
       "main_category": Optional[str],
       "crew_type": Optional[str], 
       "sub_category": Optional[str]
   }

🔧 **Configuration Schemas**
----------------------------

**Agent Configuration**

.. code-block:: yaml

   agent_name:
     role: str              # Agent role description
     goal: str              # Agent goal with parameters
     backstory: str         # Agent background story
     verbose: bool          # Optional: verbose mode
     tools: List[str]       # Optional: tool names

**Task Configuration**

.. code-block:: yaml

   task_name:
     description: str       # Task description with parameters
     expected_output: str   # Expected output description
     agent: str            # Agent name to execute task
     context: List[str]    # Optional: context task names

🚀 **Usage Examples**
--------------------

**Basic Flow Execution**

.. code-block:: python

   from esercizio1.main import MultiProcessFlow
   
   # Create and execute flow
   flow = MultiProcessFlow()
   flow.kickoff()

**Direct Routing**

.. code-block:: python

   from esercizio1.routers.main_router import route_user_input
   
   # Route a user input
   routing_info = route_user_input("What is machine learning?")
   print(routing_info)
   # Output: {'user_input': '...', 'main_category': 'RAG', 'crew_type': 'rag_crew', 'sub_category': None}

**Tool Usage**

.. code-block:: python

   from esercizio1.tools.custom_tool import MathCalculatorTool, TextToNumberTool
   
   # Mathematical calculation
   calc_tool = MathCalculatorTool()
   result = calc_tool._run("2 + 3 * 4")
   print(result)  # "Result: 14"
   
   # Text to number conversion
   text_tool = TextToNumberTool()
   result = text_tool._run("two plus three")
   print(result)  # "Converted text: 2 plus 3"

**Crew Direct Usage**

.. code-block:: python

   from esercizio1.crews.rag_crew.rag_crew import RagCrew
   
   # Execute RAG crew directly
   rag_crew = RagCrew()
   result = rag_crew.crew().kickoff(inputs={"query": "Explain quantum computing"})
   print(result.raw)

⚠️ **Error Handling**
---------------------

**Common Exceptions**

.. code-block:: python

   # Mathematical calculation errors
   try:
       result = calc_tool._run("10 / 0")
   except ZeroDivisionError:
       print("Division by zero error")
   
   # Invalid expression errors
   try:
       result = calc_tool._run("invalid expression")
   except ValueError:
       print("Invalid mathematical expression")
   
   # AI classification fallback
   try:
       routing_info = route_user_input(user_input)
   except Exception as e:
       print(f"Classification failed: {e}")
       # System falls back to pattern-based routing

🔒 **Security Considerations**
------------------------------

**Safe Expression Evaluation**

The ``MathCalculatorTool`` implements several security measures:

.. code-block:: python

   def _is_safe_expression(self, expression: str) -> bool:
       """Validates mathematical expressions for safety."""
       safe_pattern = r'^[0-9+\-*/^().]+$'
       return bool(re.match(safe_pattern, expression))

**Input Sanitization**

.. code-block:: python

   def _clean_expression(self, expression: str) -> str:
       """Removes whitespace and sanitizes input."""
       return expression.strip().replace(' ', '')

📈 **Performance Notes**
-----------------------

**Routing Performance**

- Pattern-based classification: ~1-5ms
- AI-based classification: ~100-1000ms (depends on model)
- Fallback mechanisms ensure reliability

**Memory Usage**

- Flow state: ~1-10KB per execution
- Crew instances: ~10-100KB per crew
- Tool instances: ~1-5KB per tool

**Optimization Tips**

- Use pattern-based routing for high-frequency requests
- Configure crew verbosity appropriately
- Implement result caching for repeated queries
