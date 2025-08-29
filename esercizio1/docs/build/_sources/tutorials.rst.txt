Tutorials
=========

This section provides step-by-step tutorials for common tasks and advanced usage patterns with the CrewAI Multi-Process Router System.

🎯 **Tutorial 1: Creating a Custom Crew**
-----------------------------------------

Learn how to create your own specialized crew for handling specific types of requests.

**Step 1: Define Your Crew Structure**

First, create the directory structure for your new crew:

.. code-block:: bash

   mkdir -p src/esercizio1/crews/weather_crew/config
   touch src/esercizio1/crews/weather_crew/__init__.py
   touch src/esercizio1/crews/weather_crew/weather_crew.py

**Step 2: Create Agent Configuration**

Create ``src/esercizio1/crews/weather_crew/config/agents.yaml``:

.. code-block:: yaml

   weather_analyst:
     role: >
       Weather Data Analyst
     goal: >
       Analyze and interpret weather data for {location} to provide accurate forecasts
     backstory: >
       You are an experienced meteorologist with expertise in weather pattern analysis.
       You can interpret atmospheric data and provide detailed weather insights.

   forecast_presenter:
     role: >
       Weather Forecast Presenter  
     goal: >
       Present weather information in a clear, user-friendly format for {location}
     backstory: >
       You specialize in communicating weather information to the general public.
       You make complex meteorological data easy to understand.

**Step 3: Create Task Configuration**

Create ``src/esercizio1/crews/weather_crew/config/tasks.yaml``:

.. code-block:: yaml

   analyze_weather:
     description: >
       Analyze current weather conditions and patterns for {location}.
       Consider temperature, humidity, pressure, wind patterns, and seasonal factors.
     expected_output: >
       A detailed weather analysis including current conditions and trend predictions
     agent: weather_analyst

   present_forecast:
     description: >
       Create a user-friendly weather forecast based on the analysis for {location}.
       Include current conditions, short-term forecast, and any weather advisories.
     expected_output: >
       A clear, easy-to-understand weather forecast and recommendations
     agent: forecast_presenter

**Step 4: Implement the Crew Class**

Create ``src/esercizio1/crews/weather_crew/weather_crew.py``:

.. code-block:: python

   from crewai import Agent, Crew, Process, Task
   from crewai.project import CrewBase, agent, crew, task
   from crewai.agents.agent_builder.base_agent import BaseAgent
   from typing import List


   @CrewBase
   class WeatherCrew:
       """Weather Crew for weather-related queries and forecasts."""

       agents: List[BaseAgent]
       tasks: List[Task]

       agents_config = "config/agents.yaml"
       tasks_config = "config/tasks.yaml"

       @agent
       def weather_analyst(self) -> Agent:
           """Create weather analyst agent."""
           return Agent(
               config=self.agents_config["weather_analyst"],
           )

       @agent
       def forecast_presenter(self) -> Agent:
           """Create forecast presenter agent."""
           return Agent(
               config=self.agents_config["forecast_presenter"],
           )

       @task
       def analyze_weather(self) -> Task:
           """Create weather analysis task."""
           return Task(
               config=self.tasks_config["analyze_weather"],
               agent=self.weather_analyst()
           )

       @task
       def present_forecast(self) -> Task:
           """Create forecast presentation task."""
           return Task(
               config=self.tasks_config["present_forecast"],
               agent=self.forecast_presenter(),
               context=[self.analyze_weather()]
           )

       @crew
       def crew(self) -> Crew:
           """Creates the Weather Crew."""
           return Crew(
               agents=self.agents,
               tasks=self.tasks,
               process=Process.sequential,
               verbose=True
           )

**Step 5: Update the Router**

Add weather detection to ``src/esercizio1/routers/main_router.py``:

.. code-block:: python

   # Add weather patterns to route_user_input function
   weather_patterns = [
       r'\b(weather|forecast|temperature|rain|snow|wind|climate)\b',
       r'\b(sunny|cloudy|stormy|humid|cold|hot|warm)\b',
       r'\b(today|tomorrow|this week|weekend)\b.*\b(weather|forecast)\b'
   ]
   
   is_weather = any(re.search(pattern, user_input_lower) for pattern in weather_patterns)
   
   # Add to classification logic
   if is_weather:
       main_category = "WEATHER"
       routing_info["crew_type"] = "weather_crew"

**Step 6: Test Your Custom Crew**

.. code-block:: python

   from esercizio1.crews.weather_crew.weather_crew import WeatherCrew
   
   # Test the weather crew
   weather_crew = WeatherCrew()
   result = weather_crew.crew().kickoff(inputs={"location": "New York"})
   print(result.raw)

🛠️ **Tutorial 2: Building Custom Tools**
-----------------------------------------

Learn how to create specialized tools for your crews.

**Step 1: Define Tool Requirements**

Let's create a web search tool for the RAG crew:

.. code-block:: python

   from typing import Type
   from crewai.tools import BaseTool
   from pydantic import BaseModel, Field
   import requests
   from bs4 import BeautifulSoup


   class WebSearchToolInput(BaseModel):
       """Input schema for WebSearchTool."""
       query: str = Field(..., description="Search query to look up on the web")
       max_results: int = Field(default=3, description="Maximum number of results to return")


   class WebSearchTool(BaseTool):
       """
       Web search tool for gathering information from the internet.
       
       This tool performs web searches and extracts relevant content
       from search results to provide up-to-date information.
       """
       name: str = "Web Search"
       description: str = (
           "Searches the web for information on a given query and returns "
           "relevant content from the top search results."
       )
       args_schema: Type[BaseModel] = WebSearchToolInput

       def _run(self, query: str, max_results: int = 3) -> str:
           """
           Execute web search and return results.
           
           Args:
               query (str): Search query
               max_results (int): Maximum number of results to return
               
           Returns:
               str: Formatted search results
           """
           try:
               # Simulate web search (replace with actual search API)
               results = self._perform_search(query, max_results)
               
               if not results:
                   return f"No results found for query: {query}"
               
               # Format results
               formatted_results = f"Search results for '{query}':\n\n"
               for i, result in enumerate(results, 1):
                   formatted_results += f"{i}. {result['title']}\n"
                   formatted_results += f"   {result['snippet']}\n"
                   formatted_results += f"   URL: {result['url']}\n\n"
               
               return formatted_results
               
           except Exception as e:
               return f"Error performing web search: {str(e)}"

       def _perform_search(self, query: str, max_results: int) -> list:
           """
           Perform the actual web search.
           
           Note: This is a mock implementation. In production, 
           you would integrate with a real search API like Google Custom Search.
           """
           # Mock search results
           mock_results = [
               {
                   "title": f"Information about {query}",
                   "snippet": f"Comprehensive information about {query} including definitions, examples, and use cases.",
                   "url": f"https://example.com/search?q={query.replace(' ', '+')}"
               },
               {
                   "title": f"{query} - Wikipedia",
                   "snippet": f"Wikipedia article providing detailed information about {query}.",
                   "url": f"https://wikipedia.org/wiki/{query.replace(' ', '_')}"
               },
               {
                   "title": f"Latest news about {query}",
                   "snippet": f"Recent developments and news articles related to {query}.",
                   "url": f"https://news.example.com/search?q={query.replace(' ', '+')}"
               }
           ]
           
           return mock_results[:max_results]

**Step 2: Integrate Tool with Crew**

Update your RAG crew to use the new tool:

.. code-block:: python

   from esercizio1.tools.custom_tool import WebSearchTool

   @CrewBase
   class EnhancedRagCrew:
       """Enhanced RAG Crew with web search capabilities."""
       
       @agent
       def knowledge_researcher(self) -> Agent:
           return Agent(
               config=self.agents_config["knowledge_researcher"],
               tools=[WebSearchTool()]  # Add the web search tool
           )

**Step 3: Update Task to Use Tool**

Update the task configuration to utilize the tool:

.. code-block:: yaml

   research_information:
     description: >
       Research comprehensive information about the query: {query}
       
       Use the Web Search tool to gather current information from the internet.
       Then analyze and synthesize the information to provide accurate insights.
     expected_output: >
       A comprehensive research report with current information about {query}
     agent: knowledge_researcher

🔧 **Tutorial 3: Advanced Flow Customization**
----------------------------------------------

Learn how to create complex flows with conditional logic and parallel processing.

**Step 1: Create a Multi-Stage Flow**

.. code-block:: python

   from esercizio1.main import MultiProcessState, MultiProcessFlow
   from crewai.flow import Flow, listen, start
   from typing import List, Dict, Any


   class AdvancedProcessState(MultiProcessState):
       """Extended state for advanced processing."""
       preprocessing_results: List[Dict[str, Any]] = []
       parallel_results: Dict[str, str] = {}
       final_synthesis: str = ""
       confidence_score: float = 0.0


   class AdvancedMultiProcessFlow(Flow[AdvancedProcessState]):
       """Advanced flow with preprocessing and parallel processing."""

       @start()
       def preprocess_input(self):
           """Preprocess and analyze input before routing."""
           print("Preprocessing input...")
           
           user_input = self.state.user_input
           
           # Analyze input complexity
           word_count = len(user_input.split())
           has_questions = '?' in user_input
           has_numbers = any(char.isdigit() for char in user_input)
           
           preprocessing_result = {
               "word_count": word_count,
               "has_questions": has_questions,
               "has_numbers": has_numbers,
               "complexity": "high" if word_count > 20 else "low"
           }
           
           self.state.preprocessing_results.append(preprocessing_result)
           print(f"Preprocessing complete: {preprocessing_result}")

       @listen(preprocess_input)
       def intelligent_routing(self):
           """Enhanced routing based on preprocessing results."""
           print("Performing intelligent routing...")
           
           from esercizio1.routers.main_router import route_user_input
           
           # Get standard routing
           routing_info = route_user_input(self.state.user_input)
           
           # Enhance routing based on preprocessing
           preprocessing = self.state.preprocessing_results[0]
           
           if preprocessing["complexity"] == "high":
               routing_info["processing_mode"] = "detailed"
           else:
               routing_info["processing_mode"] = "standard"
           
           self.state.routing_info = routing_info
           print(f"Enhanced routing: {routing_info}")

       @listen(intelligent_routing)
       def parallel_processing(self):
           """Process input with multiple crews in parallel (simulated)."""
           print("Starting parallel processing...")
           
           crew_type = self.state.routing_info.get("crew_type")
           user_input = self.state.user_input
           
           # Primary processing
           if crew_type == "rag_crew":
               from esercizio1.crews.rag_crew.rag_crew import RagCrew
               primary_crew = RagCrew()
               primary_result = primary_crew.crew().kickoff(inputs={"query": user_input})
               self.state.parallel_results["primary"] = primary_result.raw
           
           # Secondary analysis (always run for additional insights)
           from esercizio1.crews.poem_crew.poem_crew import PoemCrew
           poem_crew = PoemCrew()
           creative_result = poem_crew.crew().kickoff(inputs={"sentence_count": 2})
           self.state.parallel_results["creative"] = creative_result.raw
           
           print("Parallel processing complete")

       @listen(parallel_processing)
       def synthesize_results(self):
           """Synthesize results from parallel processing."""
           print("Synthesizing results...")
           
           primary_result = self.state.parallel_results.get("primary", "")
           creative_result = self.state.parallel_results.get("creative", "")
           
           # Create synthesis
           synthesis = f"""
           PRIMARY ANALYSIS:
           {primary_result}
           
           CREATIVE PERSPECTIVE:
           {creative_result}
           
           SYNTHESIS:
           The analysis provides comprehensive information while the creative perspective 
           offers an alternative viewpoint that enhances understanding.
           """
           
           self.state.final_synthesis = synthesis
           self.state.confidence_score = 0.85  # Mock confidence score
           
           print("Results synthesized successfully")

       @listen(synthesize_results)
       def generate_report(self):
           """Generate final comprehensive report."""
           print("Generating final report...")
           
           report = f"""
           =====================================
           ADVANCED PROCESSING REPORT
           =====================================
           
           INPUT: {self.state.user_input}
           
           PREPROCESSING ANALYSIS:
           {self.state.preprocessing_results[0]}
           
           ROUTING DECISION:
           {self.state.routing_info}
           
           RESULTS SYNTHESIS:
           {self.state.final_synthesis}
           
           CONFIDENCE SCORE: {self.state.confidence_score:.2f}
           
           =====================================
           """
           
           # Save to file
           with open("advanced_processing_report.txt", "w", encoding="utf-8") as f:
               f.write(report)
           
           print("Report generated: advanced_processing_report.txt")

**Step 2: Use the Advanced Flow**

.. code-block:: python

   # Create and use advanced flow
   advanced_flow = AdvancedMultiProcessFlow()
   advanced_flow.state.user_input = "Explain the implications of quantum computing on cybersecurity"
   advanced_flow.kickoff()

🎨 **Tutorial 4: Creating Interactive Applications**
---------------------------------------------------

Learn how to build interactive applications using the router system.

**Step 1: Create a Conversational Interface**

.. code-block:: python

   import tkinter as tk
   from tkinter import scrolledtext, messagebox
   from threading import Thread
   from esercizio1.main import MultiProcessFlow


   class CrewAIGUI:
       """Graphical user interface for the CrewAI system."""
       
       def __init__(self):
           self.root = tk.Tk()
           self.root.title("CrewAI Multi-Process Router")
           self.root.geometry("800x600")
           
           self.setup_ui()
           
       def setup_ui(self):
           """Set up the user interface."""
           
           # Input frame
           input_frame = tk.Frame(self.root)
           input_frame.pack(fill=tk.X, padx=10, pady=5)
           
           tk.Label(input_frame, text="Enter your request:").pack(anchor=tk.W)
           
           self.input_text = tk.Text(input_frame, height=3)
           self.input_text.pack(fill=tk.X, pady=5)
           
           # Buttons frame
           buttons_frame = tk.Frame(self.root)
           buttons_frame.pack(fill=tk.X, padx=10, pady=5)
           
           self.process_btn = tk.Button(
               buttons_frame, 
               text="Process Request", 
               command=self.process_request,
               bg="#2980B9",
               fg="white",
               font=("Arial", 10, "bold")
           )
           self.process_btn.pack(side=tk.LEFT, padx=5)
           
           self.clear_btn = tk.Button(
               buttons_frame,
               text="Clear",
               command=self.clear_output
           )
           self.clear_btn.pack(side=tk.LEFT, padx=5)
           
           # Output frame
           output_frame = tk.Frame(self.root)
           output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
           
           tk.Label(output_frame, text="Results:").pack(anchor=tk.W)
           
           self.output_text = scrolledtext.ScrolledText(
               output_frame,
               wrap=tk.WORD,
               state=tk.DISABLED
           )
           self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
           
           # Status frame
           status_frame = tk.Frame(self.root)
           status_frame.pack(fill=tk.X, padx=10, pady=5)
           
           self.status_label = tk.Label(
               status_frame, 
               text="Ready",
               relief=tk.SUNKEN,
               anchor=tk.W
           )
           self.status_label.pack(fill=tk.X)
       
       def process_request(self):
           """Process the user request in a separate thread."""
           user_input = self.input_text.get("1.0", tk.END).strip()
           
           if not user_input:
               messagebox.showwarning("Warning", "Please enter a request")
               return
           
           # Disable button during processing
           self.process_btn.config(state=tk.DISABLED)
           self.update_status("Processing...")
           
           # Process in separate thread to avoid blocking UI
           thread = Thread(target=self._process_thread, args=(user_input,))
           thread.daemon = True
           thread.start()
       
       def _process_thread(self, user_input):
           """Process request in separate thread."""
           try:
               # Create and run flow
               flow = MultiProcessFlow()
               flow.state.user_input = user_input
               
               # Manual flow execution for GUI feedback
               self.update_status("Routing input...")
               flow.route_input()
               
               routing_info = flow.state.routing_info
               crew_type = routing_info.get("crew_type", "unknown")
               
               self.update_status(f"Processing with {crew_type}...")
               flow.process_request()
               
               result = flow.state.result
               
               # Update UI in main thread
               self.root.after(0, self._update_results, user_input, routing_info, result)
               
           except Exception as e:
               self.root.after(0, self._show_error, str(e))
       
       def _update_results(self, user_input, routing_info, result):
           """Update results in main thread."""
           self.output_text.config(state=tk.NORMAL)
           self.output_text.delete("1.0", tk.END)
           
           output = f"""INPUT: {user_input}

ROUTING INFO:
- Category: {routing_info.get('main_category', 'N/A')}
- Crew: {routing_info.get('crew_type', 'N/A')}
- Sub-category: {routing_info.get('sub_category', 'N/A')}

RESULT:
{result}
"""
           
           self.output_text.insert("1.0", output)
           self.output_text.config(state=tk.DISABLED)
           
           self.process_btn.config(state=tk.NORMAL)
           self.update_status("Complete")
       
       def _show_error(self, error_msg):
           """Show error in main thread."""
           messagebox.showerror("Error", f"Processing failed: {error_msg}")
           self.process_btn.config(state=tk.NORMAL)
           self.update_status("Error")
       
       def update_status(self, message):
           """Update status label."""
           self.status_label.config(text=message)
           self.root.update()
       
       def clear_output(self):
           """Clear the output text."""
           self.output_text.config(state=tk.NORMAL)
           self.output_text.delete("1.0", tk.END)
           self.output_text.config(state=tk.DISABLED)
           self.update_status("Ready")
       
       def run(self):
           """Start the GUI application."""
           self.root.mainloop()


   # Usage
   if __name__ == "__main__":
       app = CrewAIGUI()
       app.run()

**Step 2: Create a Web Dashboard**

.. code-block:: python

   from flask import Flask, render_template, request, jsonify, session
   from flask_socketio import SocketIO, emit
   from esercizio1.main import MultiProcessFlow
   from esercizio1.routers.main_router import route_user_input
   import uuid
   from datetime import datetime


   app = Flask(__name__)
   app.secret_key = 'your-secret-key'
   socketio = SocketIO(app, cors_allowed_origins="*")


   class SessionManager:
       """Manage user sessions and conversation history."""
       
       def __init__(self):
           self.sessions = {}
       
       def get_session(self, session_id):
           if session_id not in self.sessions:
               self.sessions[session_id] = {
                   "history": [],
                   "created": datetime.now()
               }
           return self.sessions[session_id]
       
       def add_interaction(self, session_id, user_input, routing_info, result):
           session_data = self.get_session(session_id)
           session_data["history"].append({
               "timestamp": datetime.now().isoformat(),
               "input": user_input,
               "routing": routing_info,
               "result": result
           })


   session_manager = SessionManager()


   @app.route('/')
   def index():
       """Main dashboard page."""
       if 'session_id' not in session:
           session['session_id'] = str(uuid.uuid4())
       return render_template('dashboard.html')


   @socketio.on('process_request')
   def handle_process_request(data):
       """Handle real-time processing requests."""
       session_id = session.get('session_id')
       user_input = data.get('input', '').strip()
       
       if not user_input:
           emit('error', {'message': 'No input provided'})
           return
       
       try:
           # Emit status updates
           emit('status', {'message': 'Routing input...', 'stage': 'routing'})
           
           # Route the input
           routing_info = route_user_input(user_input)
           
           emit('routing_result', {
               'routing': routing_info,
               'message': f"Routed to: {routing_info['crew_type']}"
           })
           
           # Process with appropriate crew
           emit('status', {'message': f"Processing with {routing_info['crew_type']}...", 'stage': 'processing'})
           
           flow = MultiProcessFlow()
           flow.state.user_input = user_input
           flow.state.routing_info = routing_info
           flow.process_request()
           
           result = flow.state.result
           
           # Store in session
           session_manager.add_interaction(session_id, user_input, routing_info, result)
           
           # Emit final result
           emit('processing_complete', {
               'input': user_input,
               'routing': routing_info,
               'result': result,
               'timestamp': datetime.now().isoformat()
           })
           
       except Exception as e:
           emit('error', {'message': str(e)})


   @app.route('/api/history')
   def get_history():
       """Get conversation history for current session."""
       session_id = session.get('session_id')
       if not session_id:
           return jsonify([])
       
       session_data = session_manager.get_session(session_id)
       return jsonify(session_data['history'])


   # HTML Template (save as templates/dashboard.html)
   dashboard_template = """
   <!DOCTYPE html>
   <html>
   <head>
       <title>CrewAI Dashboard</title>
       <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
       <style>
           body { font-family: Arial, sans-serif; margin: 20px; }
           .container { max-width: 1200px; margin: 0 auto; }
           .input-section { margin-bottom: 20px; }
           .input-section textarea { width: 100%; height: 100px; }
           .button { background: #2980B9; color: white; padding: 10px 20px; border: none; cursor: pointer; }
           .status { padding: 10px; background: #f0f0f0; margin: 10px 0; }
           .result { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
           .history { background: #f9f9f9; padding: 10px; margin: 10px 0; }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>CrewAI Multi-Process Router Dashboard</h1>
           
           <div class="input-section">
               <textarea id="userInput" placeholder="Enter your request..."></textarea>
               <br><br>
               <button class="button" onclick="processRequest()">Process Request</button>
               <button class="button" onclick="clearResults()">Clear</button>
           </div>
           
           <div id="status" class="status" style="display: none;"></div>
           <div id="results"></div>
           <div id="history"></div>
       </div>

       <script>
           const socket = io();
           
           function processRequest() {
               const input = document.getElementById('userInput').value.trim();
               if (!input) {
                   alert('Please enter a request');
                   return;
               }
               
               socket.emit('process_request', { input: input });
           }
           
           function clearResults() {
               document.getElementById('results').innerHTML = '';
               document.getElementById('status').style.display = 'none';
           }
           
           socket.on('status', function(data) {
               const statusDiv = document.getElementById('status');
               statusDiv.textContent = data.message;
               statusDiv.style.display = 'block';
           });
           
           socket.on('routing_result', function(data) {
               console.log('Routing:', data.routing);
           });
           
           socket.on('processing_complete', function(data) {
               const resultsDiv = document.getElementById('results');
               resultsDiv.innerHTML = `
                   <div class="result">
                       <h3>Processing Complete</h3>
                       <p><strong>Input:</strong> ${data.input}</p>
                       <p><strong>Routed to:</strong> ${data.routing.crew_type}</p>
                       <p><strong>Category:</strong> ${data.routing.main_category}</p>
                       <div><strong>Result:</strong><br>${data.result}</div>
                       <p><small>Processed at: ${new Date(data.timestamp).toLocaleString()}</small></p>
                   </div>
               `;
               
               document.getElementById('status').style.display = 'none';
           });
           
           socket.on('error', function(data) {
               alert('Error: ' + data.message);
               document.getElementById('status').style.display = 'none';
           });
       </script>
   </body>
   </html>
   """

   # Save template
   import os
   os.makedirs('templates', exist_ok=True)
   with open('templates/dashboard.html', 'w') as f:
       f.write(dashboard_template)

   if __name__ == '__main__':
       socketio.run(app, debug=True)

These tutorials provide comprehensive guidance for extending and customizing the CrewAI Multi-Process Router System for various use cases and requirements.
