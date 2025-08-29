Development Guide
=================

This guide provides information for developers who want to contribute to or extend the CrewAI Multi-Process Router System.

🛠️ **Development Setup**
-------------------------

**Prerequisites**

.. code-block:: bash

   # Required tools
   Python 3.10+
   Git
   pip or uv package manager

**Clone and Setup**

.. code-block:: bash

   # Clone the repository
   git clone <repository-url>
   cd esercizio1
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode
   pip install -e .
   
   # Install development dependencies
   pip install pytest sphinx sphinx-rtd-theme myst-parser

📁 **Project Structure**
------------------------

.. code-block:: text

   esercizio1/
   ├── src/esercizio1/           # Main package
   │   ├── main.py              # Main flow orchestrator
   │   ├── crews/               # Specialized crews
   │   │   ├── rag_crew/        # Information retrieval
   │   │   ├── math_crew/       # Numerical calculations
   │   │   ├── math_text_crew/  # Textual number operations
   │   │   └── poem_crew/       # Creative writing
   │   ├── routers/             # Routing logic
   │   │   └── main_router.py   # Main and math routers
   │   └── tools/               # Custom tools
   │       └── custom_tool.py   # Mathematical and text tools
   ├── docs/                    # Sphinx documentation
   ├── tests/                   # Test files
   ├── pyproject.toml           # Project configuration
   └── README.md               # Project overview

🧪 **Testing**
--------------

**Running Tests**

.. code-block:: bash

   # Run all tests
   python test_system.py
   
   # Run with pytest (if configured)
   pytest tests/
   
   # Run specific test categories
   python test_system.py --routing-only
   python test_system.py --tools-only

**Test Coverage**

The test suite covers:

- Routing accuracy for all input types
- Mathematical tool safety and correctness  
- Text-to-number conversion accuracy
- Flow state management
- Error handling and fallbacks

**Writing New Tests**

.. code-block:: python

   def test_new_feature():
       """Test template for new features."""
       # Arrange
       input_data = "test input"
       expected_result = "expected output"
       
       # Act
       result = your_function(input_data)
       
       # Assert
       assert result == expected_result

📚 **Documentation**
--------------------

**Building Documentation**

.. code-block:: bash

   # Navigate to docs directory
   cd docs
   
   # Build HTML documentation
   sphinx-build -b html source build/html
   
   # Or use make (if available)
   make html
   
   # Open documentation
   open build/html/index.html  # On macOS
   start build/html/index.html # On Windows

**Documentation Standards**

- All public APIs must have Google-style docstrings
- Include type hints for all function parameters and returns
- Provide usage examples for complex functions
- Update documentation when adding new features

**Docstring Example**

.. code-block:: python

   def example_function(param1: str, param2: int = 10) -> Dict[str, Any]:
       """
       Brief description of the function.
       
       Longer description explaining the function's purpose, behavior,
       and any important considerations.
       
       Args:
           param1 (str): Description of the first parameter.
           param2 (int, optional): Description of second parameter. Defaults to 10.
           
       Returns:
           Dict[str, Any]: Description of the return value.
           
       Raises:
           ValueError: Description of when this exception is raised.
           
       Examples:
           >>> result = example_function("test", 5)
           >>> print(result)
           {'status': 'success', 'value': 'test_5'}
       """
       return {"status": "success", "value": f"{param1}_{param2}"}

🔧 **Extending the System**
---------------------------

**Adding New Crews**

1. **Create crew directory structure:**

   .. code-block:: bash

      mkdir -p src/esercizio1/crews/new_crew/config
      touch src/esercizio1/crews/new_crew/__init__.py

2. **Define agents in YAML:**

   .. code-block:: yaml

      # config/agents.yaml
      agent_name:
        role: Agent Role Description
        goal: Agent goal with {parameters}
        backstory: Agent background story

3. **Define tasks in YAML:**

   .. code-block:: yaml

      # config/tasks.yaml
      task_name:
        description: Task description with {parameters}
        expected_output: Expected output description
        agent: agent_name

4. **Implement crew class:**

   .. code-block:: python

      from crewai import Agent, Crew, Process, Task
      from crewai.project import CrewBase, agent, crew, task

      @CrewBase
      class NewCrew:
          agents_config = "config/agents.yaml"
          tasks_config = "config/tasks.yaml"

          @agent
          def agent_name(self) -> Agent:
              return Agent(config=self.agents_config["agent_name"])

          @task  
          def task_name(self) -> Task:
              return Task(
                  config=self.tasks_config["task_name"],
                  agent=self.agent_name()
              )

          @crew
          def crew(self) -> Crew:
              return Crew(
                  agents=self.agents,
                  tasks=self.tasks,
                  process=Process.sequential,
                  verbose=True
              )

5. **Update router:**

   Add detection patterns and routing logic to ``main_router.py``.

**Adding New Tools**

1. **Define input schema:**

   .. code-block:: python

      from pydantic import BaseModel, Field

      class NewToolInput(BaseModel):
          parameter: str = Field(..., description="Parameter description")

2. **Implement tool class:**

   .. code-block:: python

      from crewai.tools import BaseTool

      class NewTool(BaseTool):
          name: str = "Tool Name"
          description: str = "Tool description for agents"
          args_schema: Type[BaseModel] = NewToolInput

          def _run(self, parameter: str) -> str:
              # Implementation
              return f"Result for {parameter}"

3. **Add to crew:**

   .. code-block:: python

      @agent
      def agent_with_tools(self) -> Agent:
          return Agent(
              config=self.agents_config["agent_name"],
              tools=[NewTool()]
          )

🎨 **Code Style Guidelines**
----------------------------

**Python Style**

- Follow PEP 8 conventions
- Use type hints for all public APIs
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

**Import Organization**

.. code-block:: python

   # Standard library imports
   import os
   import sys
   from typing import Dict, List, Any

   # Third-party imports
   from crewai import Agent, Crew, Process, Task
   from pydantic import BaseModel, Field

   # Local imports
   from esercizio1.tools.custom_tool import MathCalculatorTool

**Error Handling**

.. code-block:: python

   def robust_function(input_data: str) -> Dict[str, Any]:
       """Function with proper error handling."""
       try:
           # Main logic
           result = process_data(input_data)
           return {"status": "success", "data": result}
           
       except ValueError as e:
           logger.warning(f"Invalid input: {e}")
           return {"status": "error", "message": f"Invalid input: {e}"}
           
       except Exception as e:
           logger.error(f"Unexpected error: {e}")
           return {"status": "error", "message": "Processing failed"}

🚀 **Performance Guidelines**
-----------------------------

**Routing Optimization**

- Use pattern-based fallbacks for offline operation
- Cache compiled regex patterns
- Implement early exit conditions

**Memory Management**

- Create crew instances on-demand
- Clear large objects after processing
- Use generators for large data sets

**Benchmarking**

.. code-block:: python

   import time
   from functools import wraps

   def benchmark(func):
       """Decorator to benchmark function execution time."""
       @wraps(func)
       def wrapper(*args, **kwargs):
           start_time = time.time()
           result = func(*args, **kwargs)
           end_time = time.time()
           print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
           return result
       return wrapper

   @benchmark
   def process_request(input_data):
       # Function implementation
       pass

🔒 **Security Best Practices**
------------------------------

**Input Validation**

.. code-block:: python

   import re

   def validate_math_expression(expression: str) -> bool:
       """Validate mathematical expressions for safety."""
       # Only allow safe characters
       safe_pattern = r'^[0-9+\-*/^().\\s]+$'
       return bool(re.match(safe_pattern, expression))

**Safe Evaluation**

.. code-block:: python

   def safe_eval(expression: str) -> float:
       """Safely evaluate mathematical expressions."""
       if not validate_math_expression(expression):
           raise ValueError("Invalid mathematical expression")
       
       # Use ast.literal_eval for simple expressions
       # or implement custom parser for complex ones
       return eval(expression)  # Only after validation

**Data Protection**

- Never log sensitive user data
- Sanitize inputs before processing
- Use secure defaults for all configurations

📋 **Release Process**
---------------------

**Version Management**

.. code-block:: bash

   # Update version in pyproject.toml
   # Update version in docs/source/conf.py
   
   # Create git tag
   git tag v1.0.1
   git push origin v1.0.1

**Documentation Updates**

.. code-block:: bash

   # Build and verify documentation
   cd docs
   sphinx-build -b html source build/html
   
   # Check for warnings or errors
   sphinx-build -W -b html source build/html

**Testing Before Release**

.. code-block:: bash

   # Run comprehensive tests
   python test_system.py
   
   # Test installation
   pip install -e .
   kickoff  # Test main functionality

🤝 **Contributing**
-------------------

**Pull Request Process**

1. Fork the repository
2. Create a feature branch: ``git checkout -b feature-name``
3. Make your changes with tests
4. Update documentation if needed
5. Run tests: ``python test_system.py``
6. Submit pull request with clear description

**Commit Message Format**

.. code-block:: text

   type(scope): brief description

   Longer description if needed

   - List of changes
   - Another change

**Types:** feat, fix, docs, style, refactor, test, chore

**Bug Reports**

Include:

- System information (OS, Python version)
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs
- Minimal reproduction example

📞 **Support and Community**
----------------------------

**Getting Help**

- Check the documentation first
- Search existing issues
- Ask questions in discussions
- Join the community chat

**Contributing Areas**

- Bug fixes and improvements
- New crew implementations
- Additional tools and integrations
- Documentation improvements
- Performance optimizations
- Testing enhancements

This development guide should help you get started with contributing to the CrewAI Multi-Process Router System!
