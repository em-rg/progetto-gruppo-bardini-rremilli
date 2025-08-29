Getting Started
===============

This guide will help you get up and running with the CrewAI Multi-Process Router System.

📋 **Prerequisites**
--------------------

Before you begin, ensure you have:

* Python 3.10 or higher
* Git (for cloning the repository)
* Basic familiarity with CrewAI concepts

🛠️ **Installation**
--------------------

1. **Clone the repository**

   .. code-block:: bash

      git clone <repository-url>
      cd esercizio1

2. **Install dependencies**

   .. code-block:: bash

      pip install -e .

3. **Set up environment (optional)**

   Create a ``.env`` file for API keys:

   .. code-block:: bash

      OPENAI_API_KEY=your_openai_api_key_here

🚀 **Running the System**
--------------------------

**Main Application**

Run the interactive flow:

.. code-block:: bash

   kickoff

This will:

1. Prompt you for input
2. Automatically classify and route your request  
3. Process it with the appropriate specialized crew
4. Save results to a file

**Demo Mode**

Test the routing system with predefined examples:

.. code-block:: bash

   demo_routing

**Flow Visualization**

Generate a visual diagram of the system flow:

.. code-block:: bash

   plot

**System Testing**

Run comprehensive tests:

.. code-block:: bash

   python test_system.py

📝 **First Steps**
------------------

1. **Try Different Input Types**

   Test various inputs to see how the system routes them:

   .. code-block:: text

      "What is artificial intelligence?"          → RAG Crew
      "Calculate 15 + 27 * 3"                   → Math Crew (Numeric)  
      "What is two plus three times five?"       → Math Text Crew (Textual)
      "Write a poem about the ocean"             → Poem Crew

2. **Understand the Flow**

   The system follows this process:

   .. mermaid::

      graph TD
          A[User Input] --> B[Main Router Classification]
          B --> C{Category?}
          C -->|RAG| D[RAG Crew]
          C -->|MATH| E[Math Sub-Router]
          C -->|POEM| F[Poem Crew]
          E --> G{Number Type?}
          G -->|NUMERIC| H[Math Crew]
          G -->|TEXTUAL| I[Math Text Crew]
          D --> J[Save Result]
          F --> J
          H --> J
          I --> J

3. **Explore the Results**

   Results are saved to files like:
   
   * ``rag_crew_result.txt`` - Information retrieval results
   * ``math_crew_result.txt`` - Numerical math results  
   * ``math_text_crew_result.txt`` - Textual math results
   * ``poem_crew_result.txt`` - Creative writing results

🔧 **Configuration**
--------------------

**Agent Configuration**

Each crew uses YAML files for configuration:

.. code-block:: yaml

   # Example: crews/rag_crew/config/agents.yaml
   knowledge_researcher:
     role: Knowledge Research Specialist
     goal: Research comprehensive information about {query}
     backstory: You are an expert researcher...

**Task Configuration**

Tasks are also defined in YAML:

.. code-block:: yaml

   # Example: crews/rag_crew/config/tasks.yaml
   research_information:
     description: Research comprehensive information about {query}
     expected_output: A comprehensive research report
     agent: knowledge_researcher

🎯 **Example Workflows**
------------------------

**Information Retrieval Workflow**

.. code-block:: python

   from esercizio1.main import MultiProcessFlow
   
   # Create and run flow
   flow = MultiProcessFlow()
   # Input: "Explain quantum computing"
   # → Routes to RAG Crew
   # → Knowledge Researcher gathers information  
   # → Information Synthesizer creates structured answer

**Mathematical Calculation Workflow**

.. code-block:: python

   # Input: "Calculate 25 * 4 + 10"
   # → Routes to Math Crew (Numeric)
   # → Math Parser analyzes expression
   # → Math Calculator computes result
   # → Result Formatter presents answer

**Textual Math Workflow**

.. code-block:: python

   # Input: "What is twenty-five times four plus ten?"
   # → Routes to Math Text Crew (Textual)  
   # → Text Number Parser converts words to numbers
   # → Text Math Calculator performs calculation
   # → Text Result Formatter shows conversion and result

🐛 **Troubleshooting**
----------------------

**Common Issues**

1. **Import Errors**
   
   Ensure you're in the project root and have installed with ``pip install -e .``

2. **API Key Issues**
   
   The system works without API keys using pattern-based fallbacks

3. **Missing Dependencies**
   
   Install required packages: ``pip install crewai pydantic``

**Error Messages**

* ``"AI classification failed"`` - Falls back to pattern-based routing
* ``"Invalid mathematical expression"`` - Check expression syntax
* ``"Error converting text numbers"`` - Verify supported number words

📚 **Next Steps**
-----------------

* Read the :doc:`architecture` guide to understand system design
* Explore the :doc:`api_reference` for detailed documentation  
* Check out :doc:`examples` for more usage patterns
* See :doc:`tutorials` for advanced configuration

💡 **Tips**
-----------

* Use clear, specific language in your inputs
* The system supports both English and Italian number words
* Mathematical expressions support +, -, *, /, ^ operations
* Creative writing prompts work best with specific themes or styles
