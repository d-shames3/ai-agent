## AI Coding Agent

A basic CLI coding agent implementation using Gemini. Limited to the example calculator app in the calculator/ directory. 

### Usage

- Install uv and sync dependencies
- To run the agent, run `uv run main.py` with the following args:
  - prompt: description of what you would like the agent to execute (wrapped in quotations)
  - --verbose or -v flags: print extra information out to the console during the agent loop

Example:
```bash
    uv run main.py "Examine the pkg/calculator.py file and the main.py. How does the calculator render output to the console?" -v
```
