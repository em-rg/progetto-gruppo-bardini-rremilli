System Architecture
==================

This document provides a comprehensive overview of the CrewAI Multi-Process Router System architecture, design patterns, and component interactions.

🏗️ **High-Level Architecture**
-------------------------------

The system follows a **Flow-Based Architecture** pattern with intelligent routing and specialized processing units:

.. code-block:: text

   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │   User Input    │───▶│  Main Router    │───▶│ Specialized     │
   │                 │    │  (AI-Powered)   │    │ Crews           │
   └─────────────────┘    └─────────────────┘    └─────────────────┘
                                   │                       │
                                   ▼                       ▼
                          ┌─────────────────┐    ┌─────────────────┐
                          │  Math Router    │    │   Results &     │
                          │ (Rule-Based)    │    │   Persistence   │
                          └─────────────────┘    └─────────────────┘

🧩 **Core Components**
----------------------

**1. Flow Orchestrator (MultiProcessFlow)**

The central coordinator that manages the entire process:

.. code-block:: python

   class MultiProcessFlow(Flow[MultiProcessState]):
       """Main flow orchestrator for the multi-process routing system."""
       
       @start()
       def get_user_input(self): ...
       
       @listen(get_user_input) 
       def route_input(self): ...
       
       @listen(route_input)
       def process_request(self): ...
       
       @listen(process_request)
       def save_result(self): ...

**Key Responsibilities:**
   - User input collection and validation
   - Flow state management
   - Component coordination
   - Result persistence

**2. Routing System**

**Main Router (AI-Powered)**

.. code-block:: python

   class MainRouter:
       """AI-powered classification of user intent."""
       
       def classify_input_task(self, user_input: str) -> Task:
           # Creates AI task for intent classification
           
       def crew(self, user_input: str) -> Crew:
           # Returns configured crew for classification

**Classifications:**
   - **RAG**: Information retrieval, knowledge queries
   - **MATH**: Mathematical calculations and operations  
   - **POEM**: Creative writing, poetry, storytelling

**Math Sub-Router (Rule-Based)**

.. code-block:: python

   class MathRouter:
       """Rule-based classification for mathematical expressions."""
       
       def classify_math_input(self, user_input: str) -> str:
           # Returns 'NUMERIC' or 'TEXTUAL'

**Sub-Classifications:**
   - **NUMERIC**: Digit-based numbers (e.g., "15 + 27")
   - **TEXTUAL**: Word-based numbers (e.g., "fifteen plus twenty-seven")

**3. Specialized Crews**

Each crew implements the **CrewBase** pattern with specialized agents and tasks:

**RAG Crew Architecture**

.. code-block:: text

   RAG Crew
   ├── Knowledge Researcher (Agent)
   │   └── Research Information (Task)
   └── Information Synthesizer (Agent)
       └── Synthesize Answer (Task)

.. code-block:: python

   @CrewBase
   class RagCrew:
       @agent
       def knowledge_researcher(self) -> Agent: ...
       
       @agent  
       def information_synthesizer(self) -> Agent: ...
       
       @task
       def research_information(self) -> Task: ...
       
       @task
       def synthesize_answer(self) -> Task: ...

**Math Crew Architecture**

.. code-block:: text

   Math Crew
   ├── Math Parser (Agent)
   │   └── Parse Math Expression (Task)
   ├── Math Calculator (Agent)
   │   └── Calculate Result (Task)
   └── Result Formatter (Agent)
       └── Format Result (Task)

**Math Text Crew Architecture**

.. code-block:: text

   Math Text Crew  
   ├── Text Number Parser (Agent + Tools)
   │   └── Parse Text Math Expression (Task)
   ├── Text Math Calculator (Agent + Tools)
   │   └── Calculate Text Math Result (Task)
   └── Text Result Formatter (Agent)
       └── Format Text Math Result (Task)

**Poem Crew Architecture**

.. code-block:: text

   Poem Crew
   └── Poem Writer (Agent)
       └── Write Poem (Task)

**4. Custom Tools**

**MathCalculatorTool**

.. code-block:: python

   class MathCalculatorTool(BaseTool):
       """Safe mathematical expression calculator."""
       
       def _run(self, expression: str) -> str:
           # Safe evaluation with validation
           
       def _is_safe_expression(self, expression: str) -> bool:
           # Security validation

**Features:**
   - Safe expression evaluation
   - Input validation and sanitization
   - Support for basic arithmetic and power operations
   - Error handling and division by zero protection

**TextToNumberTool**

.. code-block:: python

   class TextToNumberTool(BaseTool):
       """Multilingual text-to-number converter."""
       
       def _convert_text_numbers(self, text: str) -> str:
           # Converts text numbers to digits
           
       def _get_word_to_num_dict(self) -> Dict[str, int]:
           # Multilingual number dictionary

**Features:**
   - English and Italian number word support
   - Comprehensive number dictionary (0-1000+)
   - Punctuation handling
   - Preserves non-number words

🔄 **Data Flow**
----------------

**1. Input Processing Flow**

.. code-block:: text

   User Input
      ↓
   Input Validation
      ↓ 
   State Initialization
      ↓
   Main Router Classification
      ↓
   [RAG|MATH|POEM] Category
      ↓
   Math Sub-Classification (if MATH)
      ↓
   [NUMERIC|TEXTUAL] Sub-Category
      ↓
   Crew Selection
      ↓
   Specialized Processing

**2. Crew Processing Flow**

.. code-block:: text

   Selected Crew
      ↓
   Agent Initialization
      ↓
   Task Configuration
      ↓
   Sequential Task Execution
      ↓
   Context Sharing Between Tasks
      ↓
   Result Generation
      ↓
   Output Formatting

**3. Result Flow**

.. code-block:: text

   Crew Result
      ↓
   State Update
      ↓
   File Generation
      ↓
   Result Persistence
      ↓
   User Notification

🏛️ **Design Patterns**
-----------------------

**1. Flow Pattern**

Uses CrewAI Flow for declarative process orchestration:

.. code-block:: python

   @start()
   def step1(self): ...
   
   @listen(step1)
   def step2(self): ...
   
   @listen(step2) 
   def step3(self): ...

**2. Strategy Pattern**

Different crews implement the same interface but different strategies:

.. code-block:: python

   # All crews implement this pattern
   @CrewBase
   class XxxCrew:
       @crew
       def crew(self) -> Crew: ...

**3. Factory Pattern**

Router acts as a factory for crew selection:

.. code-block:: python

   def route_user_input(user_input: str) -> Dict[str, Any]:
       # Factory logic for crew selection
       if category == "RAG":
           return {"crew_type": "rag_crew"}
       elif category == "MATH":
           return {"crew_type": "math_crew"}
       # ...

**4. Template Method Pattern**

Tools follow a consistent template:

.. code-block:: python

   class CustomTool(BaseTool):
       name: str = "Tool Name"
       description: str = "Tool Description"
       args_schema: Type[BaseModel] = InputSchema
       
       def _run(self, **kwargs) -> str:
           # Implementation

🔧 **Configuration Architecture**
---------------------------------

**YAML-Based Configuration**

Each crew uses YAML files for agent and task configuration:

.. code-block:: text

   crews/
   ├── rag_crew/
   │   └── config/
   │       ├── agents.yaml
   │       └── tasks.yaml
   ├── math_crew/
   │   └── config/
   │       ├── agents.yaml  
   │       └── tasks.yaml
   └── ...

**Configuration Schema**

.. code-block:: yaml

   # agents.yaml
   agent_name:
     role: Agent Role Description
     goal: Agent Goal with {parameters}
     backstory: Agent Background Story
   
   # tasks.yaml  
   task_name:
     description: Task Description with {parameters}
     expected_output: Expected Output Description
     agent: agent_name

📊 **State Management**
-----------------------

**MultiProcessState Schema**

.. code-block:: python

   class MultiProcessState(BaseModel):
       user_input: str = ""           # Original user input
       routing_info: Dict[str, Any] = {}  # Routing decisions
       result: str = ""               # Final processed result  
       sentence_count: int = 1        # Poem-specific parameter

**State Transitions**

.. code-block:: text

   Empty State
      ↓ get_user_input()
   Input Captured
      ↓ route_input()  
   Routing Decided
      ↓ process_request()
   Result Generated
      ↓ save_result()
   Persisted State

🛡️ **Security Architecture**
-----------------------------

**Input Validation**

- Mathematical expression sanitization
- Safe evaluation patterns
- Injection prevention

**Safe Execution**

- No arbitrary code execution
- Controlled evaluation environment
- Error boundary handling

**Data Protection**

- No sensitive data logging
- Secure state management
- Clean input/output separation

⚡ **Performance Considerations**
---------------------------------

**Routing Optimization**

- Pattern-based fallbacks for offline operation
- Efficient regex compilation
- Early classification exits

**Memory Management**

- Stateless crew instances
- Efficient flow state management
- Resource cleanup after processing

**Scalability Features**

- Modular crew architecture
- Independent processing units
- Configurable concurrency options

🔍 **Monitoring & Observability**
----------------------------------

**Logging Strategy**

- Flow step tracking
- Crew execution monitoring  
- Error capture and reporting

**Debugging Support**

- Verbose mode configuration
- Step-by-step execution tracing
- State inspection capabilities

**Performance Metrics**

- Processing time measurement
- Success/failure rate tracking
- Resource utilization monitoring
