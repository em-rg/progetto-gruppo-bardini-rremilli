# CrewAI Multi-Process Router System

This project implements a sophisticated routing system for CrewAI that automatically classifies user input and routes it to appropriate specialized crews.

## Architecture

### Main Router
The main router (`routers/main_router.py`) classifies user input into three main categories:
- **RAG**: Information retrieval and knowledge-based queries
- **MATH**: Mathematical operations and calculations  
- **POEM**: Creative writing and poetry requests

### Math Sub-Router
For mathematical inputs, a secondary router determines the number format:
- **NUMERIC**: Numbers written as digits (e.g., "15 + 27")
- **TEXTUAL**: Numbers written as words (e.g., "fifteen plus twenty-seven")

### Specialized Crews

1. **RAG Crew** (`crews/rag_crew/`)
   - Knowledge Researcher: Gathers comprehensive information
   - Information Synthesizer: Creates well-structured answers

2. **Math Crew** (`crews/math_crew/`)
   - Math Parser: Identifies numerical expressions
   - Math Calculator: Performs calculations
   - Result Formatter: Presents results clearly

3. **Math Text Crew** (`crews/math_text_crew/`)
   - Text Number Parser: Converts textual numbers to digits
   - Text Math Calculator: Handles textual mathematical expressions
   - Text Result Formatter: Shows conversion and results

4. **Poem Crew** (`crews/poem_crew/`)
   - Poem Writer: Creates creative content

## Usage

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

## Example Inputs and Routing

- "What is artificial intelligence?" → RAG Crew
- "Calculate 15 + 27 * 3" → Math Crew (Numeric)
- "What is two plus three times five?" → Math Text Crew (Textual)
- "Write a poem about the ocean" → Poem Crew
- "Explain quantum computing" → RAG Crew
- "Solve: twenty-five divided by five" → Math Text Crew (Textual)

## Flow Process

1. **User Input**: System receives user request
2. **Main Classification**: Input is classified into RAG/MATH/POEM
3. **Math Sub-Classification**: If MATH, determine NUMERIC vs TEXTUAL
4. **Crew Selection**: Route to appropriate specialized crew
5. **Processing**: Selected crew processes the request
6. **Result**: Output is formatted and saved

## Best Practices Implemented

- Modular crew design with specialized agents
- Clear separation of concerns
- Comprehensive YAML configuration
- Proper error handling and fallbacks
- Multi-language support (English/Italian) for textual numbers
- Sequential processing with context sharing between agents
