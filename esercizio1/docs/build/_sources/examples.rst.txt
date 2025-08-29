Examples
========

This section provides comprehensive examples demonstrating how to use the CrewAI Multi-Process Router System in various scenarios.

🎯 **Basic Usage Examples**
---------------------------

**Example 1: Information Retrieval (RAG)**

.. code-block:: python

   from esercizio1.main import MultiProcessFlow
   
   # Input that will be routed to RAG crew
   user_input = "What is artificial intelligence and how does it work?"
   
   # Create and execute flow
   flow = MultiProcessFlow()
   flow.state.user_input = user_input
   flow.kickoff()
   
   # Result will be saved to rag_crew_result.txt

**Example Output:**

.. code-block:: text

   User Input: What is artificial intelligence and how does it work?
   Crew Type: rag_crew
   Routing Info: {'user_input': '...', 'main_category': 'RAG', 'crew_type': 'rag_crew', 'sub_category': None}
   Result:
   Artificial Intelligence (AI) is a branch of computer science focused on creating 
   systems that can perform tasks typically requiring human intelligence...

**Example 2: Mathematical Calculation (Numeric)**

.. code-block:: python

   from esercizio1.routers.main_router import route_user_input
   from esercizio1.crews.math_crew.math_crew import MathCrew
   
   # Mathematical input with numbers
   user_input = "Calculate 25 * 4 + 10 / 2"
   
   # Route the input
   routing_info = route_user_input(user_input)
   print(f"Routed to: {routing_info['crew_type']}")  # math_crew
   print(f"Sub-category: {routing_info['sub_category']}")  # NUMERIC
   
   # Execute math crew
   math_crew = MathCrew()
   result = math_crew.crew().kickoff(inputs={"math_expression": user_input})
   print(f"Result: {result.raw}")

**Example Output:**

.. code-block:: text

   Routed to: math_crew
   Sub-category: NUMERIC
   Result: Expression: 25 * 4 + 10 / 2
   Calculation: (25 * 4) + (10 / 2) = 100 + 5 = 105
   Final Answer: 105

**Example 3: Textual Mathematics**

.. code-block:: python

   from esercizio1.crews.math_text_crew.math_text_crew import MathTextCrew
   
   # Mathematical input with text numbers
   user_input = "What is twenty-five times four plus ten divided by two?"
   
   # Route and execute
   routing_info = route_user_input(user_input)
   print(f"Sub-category: {routing_info['sub_category']}")  # TEXTUAL
   
   math_text_crew = MathTextCrew()
   result = math_text_crew.crew().kickoff(inputs={"math_expression": user_input})
   print(f"Result: {result.raw}")

**Example Output:**

.. code-block:: text

   Sub-category: TEXTUAL
   Result: Original: twenty-five times four plus ten divided by two
   Converted: 25 * 4 + 10 / 2
   Calculation: 25 * 4 + 10 / 2 = 105
   Final Answer: 105

**Example 4: Creative Writing**

.. code-block:: python

   from esercizio1.crews.poem_crew.poem_crew import PoemCrew
   
   # Creative writing input
   user_input = "Write a haiku about artificial intelligence"
   
   # Execute poem crew
   poem_crew = PoemCrew()
   result = poem_crew.crew().kickoff(inputs={"sentence_count": 3})
   print(f"Result: {result.raw}")

**Example Output:**

.. code-block:: text

   Result: Digital minds awake,
   Silicon dreams take their shape,
   Future unfolds bright.

🛠️ **Tool Usage Examples**
---------------------------

**Example 5: Mathematical Calculator Tool**

.. code-block:: python

   from esercizio1.tools.custom_tool import MathCalculatorTool
   
   # Create tool instance
   calc_tool = MathCalculatorTool()
   
   # Test various expressions
   expressions = [
       "2 + 3 * 4",
       "(10 + 5) / 3", 
       "2^3 + 1",
       "100 / 4 - 5"
   ]
   
   for expr in expressions:
       result = calc_tool._run(expr)
       print(f"{expr} = {result}")

**Output:**

.. code-block:: text

   2 + 3 * 4 = Result: 14
   (10 + 5) / 3 = Result: 5.0
   2^3 + 1 = Result: 9
   100 / 4 - 5 = Result: 20.0

**Example 6: Text to Number Converter Tool**

.. code-block:: python

   from esercizio1.tools.custom_tool import TextToNumberTool
   
   # Create tool instance
   text_tool = TextToNumberTool()
   
   # Test text conversions
   texts = [
       "two plus three equals five",
       "twenty-five minus ten",
       "due più tre fa cinque",  # Italian
       "one hundred divided by five"
   ]
   
   for text in texts:
       result = text_tool._run(text)
       print(f"'{text}' -> {result}")

**Output:**

.. code-block:: text

   'two plus three equals five' -> Converted text: 2 plus 3 equals 5
   'twenty-five minus ten' -> Converted text: 25 minus 10
   'due più tre fa cinque' -> Converted text: 2 più 3 fa 5
   'one hundred divided by five' -> Converted text: 100 divided by 5

🎭 **Advanced Usage Examples**
------------------------------

**Example 7: Custom Flow Implementation**

.. code-block:: python

   from esercizio1.main import MultiProcessState, MultiProcessFlow
   from esercizio1.routers.main_router import route_user_input
   from typing import List
   
   class BatchProcessFlow(MultiProcessFlow):
       """Custom flow for processing multiple inputs."""
       
       def __init__(self, inputs: List[str]):
           super().__init__()
           self.inputs = inputs
           self.results = []
       
       def process_batch(self):
           """Process multiple inputs in sequence."""
           for user_input in self.inputs:
               print(f"Processing: {user_input}")
               
               # Route input
               routing_info = route_user_input(user_input)
               
               # Process based on crew type
               if routing_info["crew_type"] == "rag_crew":
                   from esercizio1.crews.rag_crew.rag_crew import RagCrew
                   crew = RagCrew()
                   result = crew.crew().kickoff(inputs={"query": user_input})
               
               elif routing_info["crew_type"] == "math_crew":
                   from esercizio1.crews.math_crew.math_crew import MathCrew
                   crew = MathCrew()
                   result = crew.crew().kickoff(inputs={"math_expression": user_input})
               
               # Store result
               self.results.append({
                   "input": user_input,
                   "routing": routing_info,
                   "result": result.raw
               })
   
   # Usage
   batch_inputs = [
       "What is machine learning?",
       "Calculate 15 + 27",
       "Write a poem about technology"
   ]
   
   batch_flow = BatchProcessFlow(batch_inputs)
   batch_flow.process_batch()
   
   for item in batch_flow.results:
       print(f"Input: {item['input']}")
       print(f"Crew: {item['routing']['crew_type']}")
       print(f"Result: {item['result'][:100]}...")
       print("-" * 50)

**Example 8: Error Handling and Fallbacks**

.. code-block:: python

   from esercizio1.routers.main_router import route_user_input
   from esercizio1.tools.custom_tool import MathCalculatorTool
   import logging
   
   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def robust_processing(user_input: str) -> dict:
       """Process input with comprehensive error handling."""
       
       try:
           # Attempt routing
           routing_info = route_user_input(user_input)
           logger.info(f"Successfully routed to: {routing_info['crew_type']}")
           
           # Process based on crew type
           if routing_info["crew_type"] == "math_crew":
               try:
                   # Try mathematical calculation
                   calc_tool = MathCalculatorTool()
                   result = calc_tool._run(user_input)
                   
                   if "Error" in result:
                       logger.warning(f"Math calculation error: {result}")
                       return {"status": "error", "message": result}
                   
                   return {"status": "success", "result": result}
                   
               except Exception as e:
                   logger.error(f"Math processing failed: {e}")
                   return {"status": "error", "message": f"Math processing failed: {e}"}
           
           else:
               # Process other crew types
               logger.info(f"Processing with {routing_info['crew_type']}")
               return {"status": "success", "routing": routing_info}
               
       except Exception as e:
           logger.error(f"Routing failed: {e}")
           return {"status": "error", "message": f"Routing failed: {e}"}
   
   # Test with various inputs
   test_inputs = [
       "Calculate 10 + 5",
       "10 / 0",  # Division by zero
       "invalid math expression !@#",
       "What is AI?",
       ""  # Empty input
   ]
   
   for test_input in test_inputs:
       result = robust_processing(test_input)
       print(f"Input: '{test_input}' -> Status: {result['status']}")
       if result['status'] == 'error':
           print(f"  Error: {result['message']}")

**Example 9: Configuration Customization**

.. code-block:: python

   from esercizio1.crews.rag_crew.rag_crew import RagCrew
   from crewai import Agent, Task
   
   class CustomRagCrew(RagCrew):
       """Customized RAG crew with specialized configuration."""
       
       def knowledge_researcher(self) -> Agent:
           """Override with custom agent configuration."""
           return Agent(
               role="Specialized AI Research Expert",
               goal="Research cutting-edge AI technologies and their applications for: {query}",
               backstory="""You are a world-renowned AI researcher with deep expertise in 
               machine learning, neural networks, and emerging AI technologies. You have 
               published papers in top-tier conferences and have practical experience 
               implementing AI solutions.""",
               verbose=True,
               max_iter=3,  # Custom iteration limit
               memory=True   # Enable memory
           )
       
       def research_information(self) -> Task:
           """Override with custom task configuration."""
           return Task(
               description="""
               Conduct comprehensive research on: {query}
               
               Focus on:
               1. Current state-of-the-art approaches
               2. Recent breakthroughs and developments  
               3. Practical applications and use cases
               4. Future trends and implications
               5. Technical challenges and limitations
               
               Provide detailed, technical insights suitable for AI professionals.
               """,
               expected_output="""A comprehensive technical research report covering 
               state-of-the-art approaches, recent developments, applications, and future 
               trends related to the query.""",
               agent=self.knowledge_researcher()
           )
   
   # Usage
   custom_crew = CustomRagCrew()
   result = custom_crew.crew().kickoff(inputs={
       "query": "Transformer architectures in natural language processing"
   })
   print(result.raw)

🔧 **Integration Examples**
---------------------------

**Example 10: Web API Integration**

.. code-block:: python

   from flask import Flask, request, jsonify
   from esercizio1.routers.main_router import route_user_input
   from esercizio1.main import MultiProcessFlow
   
   app = Flask(__name__)
   
   @app.route('/process', methods=['POST'])
   def process_input():
       """API endpoint for processing user input."""
       try:
           data = request.get_json()
           user_input = data.get('input', '')
           
           if not user_input:
               return jsonify({"error": "No input provided"}), 400
           
           # Route the input
           routing_info = route_user_input(user_input)
           
           # Create flow and process
           flow = MultiProcessFlow()
           flow.state.user_input = user_input
           flow.route_input()
           flow.process_request()
           
           return jsonify({
               "input": user_input,
               "routing": routing_info,
               "result": flow.state.result,
               "status": "success"
           })
           
       except Exception as e:
           return jsonify({"error": str(e)}), 500
   
   @app.route('/demo', methods=['GET'])
   def demo_routing():
       """Demo endpoint showing routing examples."""
       examples = [
           "What is quantum computing?",
           "Calculate 15 + 27 * 3", 
           "Write a poem about AI"
       ]
       
       results = []
       for example in examples:
           routing_info = route_user_input(example)
           results.append({
               "input": example,
               "crew_type": routing_info["crew_type"],
               "category": routing_info["main_category"]
           })
       
       return jsonify({"examples": results})
   
   if __name__ == '__main__':
       app.run(debug=True)

**Usage:**

.. code-block:: bash

   # Start the server
   python web_api.py
   
   # Test the API
   curl -X POST http://localhost:5000/process \
        -H "Content-Type: application/json" \
        -d '{"input": "What is machine learning?"}'

**Example 11: Command Line Interface**

.. code-block:: python

   import argparse
   import sys
   from esercizio1.routers.main_router import route_user_input
   from esercizio1.main import MultiProcessFlow, demo_routing
   
   def main():
       parser = argparse.ArgumentParser(
           description="CrewAI Multi-Process Router CLI"
       )
       
       subparsers = parser.add_subparsers(dest='command', help='Available commands')
       
       # Process command
       process_parser = subparsers.add_parser('process', help='Process user input')
       process_parser.add_argument('input', help='User input to process')
       process_parser.add_argument('--verbose', action='store_true', help='Verbose output')
       
       # Route command  
       route_parser = subparsers.add_parser('route', help='Show routing decision')
       route_parser.add_argument('input', help='User input to route')
       
       # Demo command
       demo_parser = subparsers.add_parser('demo', help='Run routing demo')
       
       args = parser.parse_args()
       
       if args.command == 'process':
           flow = MultiProcessFlow()
           flow.state.user_input = args.input
           
           if args.verbose:
               print(f"Processing: {args.input}")
           
           flow.kickoff()
           print(f"Result saved to file")
           
       elif args.command == 'route':
           routing_info = route_user_input(args.input)
           print(f"Input: {args.input}")
           print(f"Category: {routing_info['main_category']}")
           print(f"Crew: {routing_info['crew_type']}")
           if routing_info.get('sub_category'):
               print(f"Sub-category: {routing_info['sub_category']}")
       
       elif args.command == 'demo':
           demo_routing()
       
       else:
           parser.print_help()
   
   if __name__ == '__main__':
       main()

**Usage:**

.. code-block:: bash

   # Process input
   python cli.py process "What is artificial intelligence?"
   
   # Show routing decision
   python cli.py route "Calculate 15 + 27"
   
   # Run demo
   python cli.py demo

📊 **Performance Examples**
---------------------------

**Example 12: Benchmarking Routing Performance**

.. code-block:: python

   import time
   from esercizio1.routers.main_router import route_user_input
   from statistics import mean, stdev
   
   def benchmark_routing(test_inputs: list, iterations: int = 100):
       """Benchmark routing performance."""
       
       results = {}
       
       for input_text in test_inputs:
           times = []
           
           for _ in range(iterations):
               start_time = time.time()
               routing_info = route_user_input(input_text)
               end_time = time.time()
               times.append((end_time - start_time) * 1000)  # Convert to ms
           
           results[input_text] = {
               "crew_type": routing_info["crew_type"],
               "avg_time_ms": mean(times),
               "std_dev_ms": stdev(times) if len(times) > 1 else 0,
               "min_time_ms": min(times),
               "max_time_ms": max(times)
           }
       
       return results
   
   # Test inputs
   test_inputs = [
       "What is AI?",
       "Calculate 2 + 2",
       "What is two plus two?",
       "Write a poem",
       "Explain quantum computing"
   ]
   
   # Run benchmark
   print("Benchmarking routing performance...")
   results = benchmark_routing(test_inputs)
   
   for input_text, stats in results.items():
       print(f"\nInput: '{input_text}'")
       print(f"  Crew: {stats['crew_type']}")
       print(f"  Avg time: {stats['avg_time_ms']:.2f}ms")
       print(f"  Std dev: {stats['std_dev_ms']:.2f}ms")
       print(f"  Range: {stats['min_time_ms']:.2f}-{stats['max_time_ms']:.2f}ms")

🎨 **Creative Examples**
------------------------

**Example 13: Multi-Modal Processing**

.. code-block:: python

   from esercizio1.main import MultiProcessFlow
   from typing import List, Dict, Any
   
   class MultiModalFlow(MultiProcessFlow):
       """Extended flow supporting multiple input types."""
       
       def __init__(self):
           super().__init__()
           self.batch_results = []
       
       def process_conversation(self, conversation: List[str]) -> List[Dict[str, Any]]:
           """Process a conversation with multiple exchanges."""
           
           for i, user_input in enumerate(conversation):
               print(f"Processing message {i+1}: {user_input}")
               
               # Reset state for each input
               self.state.user_input = user_input
               self.state.result = ""
               
               # Process the input
               self.route_input()
               self.process_request()
               
               # Store result
               result_data = {
                   "message_id": i + 1,
                   "input": user_input,
                   "routing": self.state.routing_info,
                   "result": self.state.result
               }
               self.batch_results.append(result_data)
           
           return self.batch_results
   
   # Example conversation
   conversation = [
       "What is machine learning?",
       "Can you calculate 15 * 8 + 12?",
       "Now write that calculation in words",
       "Create a haiku about learning"
   ]
   
   # Process conversation
   flow = MultiModalFlow()
   results = flow.process_conversation(conversation)
   
   # Display results
   for result in results:
       print(f"\nMessage {result['message_id']}: {result['input']}")
       print(f"Routed to: {result['routing']['crew_type']}")
       print(f"Result: {result['result'][:100]}...")

This comprehensive examples section demonstrates the versatility and power of the CrewAI Multi-Process Router System across various use cases and integration scenarios.
