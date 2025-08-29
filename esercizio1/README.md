# CrewAI Multi-Process Router System

A sophisticated CrewAI-based system that intelligently routes user input to specialized crews for different types of tasks: information retrieval (RAG), mathematical operations, and creative writing.

## 🚀 Features

- **Intelligent Routing**: Automatically classifies user input and routes to appropriate specialized crews
- **Math Sub-Routing**: Distinguishes between numerical and textual mathematical expressions
- **Multi-Language Support**: Handles English and Italian textual numbers
- **Specialized Crews**: 
  - RAG Crew for information retrieval
  - Math Crew for numerical calculations
  - Math Text Crew for textual number calculations
  - Poem Crew for creative writing
- **Custom Tools**: Safe mathematical calculator and text-to-number converter
- **Flow-Based Architecture**: Uses CrewAI Flow for orchestrating the entire process

## 📁 Project Structure

```
src/esercizio1/
├── main.py                 # Main application flow
├── crews/
│   ├── rag_crew/          # Information retrieval crew
│   ├── math_crew/         # Numerical math crew
│   ├── math_text_crew/    # Textual math crew
│   └── poem_crew/         # Creative writing crew
├── routers/
│   └── main_router.py     # Main routing logic
└── tools/
    └── custom_tool.py     # Mathematical tools
```

## 🛠️ Installation

1. Ensure you have Python 3.10+ installed
2. Install dependencies:
```bash
pip install -e .
```

## 🎯 Usage

### Run the main application:
```bash
kickoff
```

### Test the routing system:
```bash
demo_routing
```

### View the flow diagram:
```bash
plot
```

### Run comprehensive tests:
```bash
python test_system.py
```

## 📝 Example Inputs and Routing

| Input | Routed To | Sub-Category |
|-------|-----------|--------------|
| "What is artificial intelligence?" | RAG Crew | - |
| "Calculate 15 + 27 * 3" | Math Crew | NUMERIC |
| "What is two plus three times five?" | Math Text Crew | TEXTUAL |
| "Write a poem about the ocean" | Poem Crew | - |
| "Explain quantum computing" | RAG Crew | - |
| "Solve: twenty-five divided by five" | Math Text Crew | TEXTUAL |

## 🔄 How It Works

1. **User Input**: System receives user request
2. **Main Classification**: AI agent classifies input as RAG/MATH/POEM
3. **Math Sub-Classification**: If MATH, determines NUMERIC vs TEXTUAL
4. **Crew Selection**: Routes to appropriate specialized crew
5. **Processing**: Selected crew processes the request with specialized agents
6. **Result**: Output is formatted and saved

## 🏗️ Architecture

### Main Router
- Uses a specialized CrewAI agent to classify user intent
- Routes to three main categories: RAG, MATH, POEM

### Math Sub-Router
- Pattern-based classification for mathematical expressions
- Distinguishes between numerical digits and textual numbers
- Supports multiple languages (English/Italian)

### Specialized Crews
Each crew has specialized agents with distinct roles:

**RAG Crew**:
- Knowledge Researcher: Gathers information
- Information Synthesizer: Creates structured answers

**Math Crew**:
- Math Parser: Analyzes numerical expressions
- Math Calculator: Performs calculations (with tools)
- Result Formatter: Presents results

**Math Text Crew**:
- Text Number Parser: Converts words to numbers (with tools)
- Text Math Calculator: Handles textual calculations
- Text Result Formatter: Shows conversions and results

**Poem Crew**:
- Poem Writer: Creates creative content

## 🛠️ Custom Tools

### MathCalculatorTool
- Safe evaluation of mathematical expressions
- Supports basic arithmetic and power operations
- Prevents code injection attacks

### TextToNumberTool
- Converts textual numbers to digits
- Supports English and Italian number words
- Handles complex textual expressions

## 🔧 Configuration

All crews use YAML configuration files for agents and tasks:
- `config/agents.yaml`: Agent roles, goals, and backstories
- `config/tasks.yaml`: Task descriptions and expected outputs

## 🧪 Testing

The system includes comprehensive tests:
- Routing accuracy tests
- Math sub-router classification tests
- Custom tool functionality tests

Run tests with:
```bash
python test_system.py
```

## 📊 Best Practices Implemented

- ✅ Modular crew design with specialized agents
- ✅ Clear separation of concerns
- ✅ Comprehensive YAML configuration
- ✅ Proper error handling and fallbacks
- ✅ Safe mathematical evaluation
- ✅ Multi-language support
- ✅ Sequential processing with context sharing
- ✅ Extensive testing and validation

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Run the demo: `kickoff`
4. Try different inputs to see the routing in action!

## 📈 Future Enhancements

- Add more language support for textual numbers
- Implement more sophisticated mathematical operations
- Add support for additional content types
- Enhance RAG capabilities with external knowledge sources
- Add web interface for easier interaction

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/esercizio1/config/agents.yaml` to define your agents
- Modify `src/esercizio1/config/tasks.yaml` to define your tasks
- Modify `src/esercizio1/crew.py` to add your own logic, tools and specific args
- Modify `src/esercizio1/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the esercizio1 Flow as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The esercizio1 Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the {{crew_name}} Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
