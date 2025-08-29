CrewAI Multi-Process Router System Documentation
=============================================

Welcome to the **CrewAI Multi-Process Router System** documentation! This project implements 
a sophisticated routing system that automatically classifies user input and routes it to 
appropriate specialized crews for different types of tasks.

🚀 **Key Features**
-------------------

* **Intelligent Routing**: Automatically classifies user input using AI agents
* **Math Sub-Routing**: Distinguishes between numerical and textual mathematical expressions  
* **Multi-Language Support**: Handles English and Italian textual numbers
* **Specialized Crews**: Dedicated crews for RAG, Math, Text Math, and Creative Writing
* **Custom Tools**: Safe mathematical calculator and text-to-number converter
* **Flow-Based Architecture**: Uses CrewAI Flow for complete process orchestration

📚 **Table of Contents**
------------------------

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   getting_started
   architecture
   api_reference
   examples
   tutorials
   development

🎯 **Quick Start**
------------------

Install dependencies and run the system:

.. code-block:: bash

   pip install -e .
   kickoff

The system will prompt for input and automatically route it to the appropriate crew.

🏗️ **System Overview**
-----------------------

The system consists of several key components:

**Main Router**
   AI-powered classification of user intent into RAG, MATH, or POEM categories

**Math Sub-Router** 
   Rule-based classification of mathematical expressions as NUMERIC or TEXTUAL

**Specialized Crews**
   - **RAG Crew**: Information retrieval and knowledge synthesis
   - **Math Crew**: Numerical mathematical calculations  
   - **Math Text Crew**: Textual number mathematical operations
   - **Poem Crew**: Creative writing and poetry generation

**Custom Tools**
   - **MathCalculatorTool**: Safe mathematical expression evaluation
   - **TextToNumberTool**: Multilingual text-to-number conversion

📝 **Example Usage**
--------------------

.. code-block:: python

   from esercizio1.routers.main_router import route_user_input
   
   # Information retrieval
   result = route_user_input("What is artificial intelligence?")
   # Routes to: rag_crew
   
   # Numerical math
   result = route_user_input("Calculate 15 + 27 * 3") 
   # Routes to: math_crew (NUMERIC)
   
   # Textual math
   result = route_user_input("What is two plus three times five?")
   # Routes to: math_text_crew (TEXTUAL)
   
   # Creative writing
   result = route_user_input("Write a poem about the ocean")
   # Routes to: poem_crew

🔧 **Development**
------------------

The project follows CrewAI best practices with:

* Modular crew design with specialized agents
* YAML configuration for agents and tasks  
* Comprehensive error handling and fallbacks
* Multi-language support
* Extensive testing and validation

📖 **API Reference**
--------------------

For detailed API documentation, see the :doc:`api_reference` section.

🚀 **Getting Started**
----------------------

New to the system? Check out our :doc:`getting_started` guide for step-by-step instructions.

📋 **Indices and Tables**
-------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
