# FelixOS — LLM-Powered Terminal for Code Generation & Execution

FelixOS is an experimental AI-powered terminal that converts natural-language commands into executable shell scripts, schedules them using a First-Come-First-Served (FCFS) process queue, and manages them through OS-like process states.

This project was developed as part of the IT371 course at NITK Surathkal.

## Features

Natural Language → Executable Script:
Prefix any command with `felix`:
    felix open a browser tab and search for NITK

Felix:
1. Sends the prompt to the DeepSeek-Coder LLM
2. Generates a .sh script
3. Places it in the ready queue
4. Executes it automatically

## FCFS Process Scheduling
Scripts flow through:
ready_files/ → running_files/ → finished_files/

Implemented using collections.deque for fair FCFS execution.

## Interactive Terminal Shell
- Normal shell commands (ls, pwd, cd, etc.) still work
- Only commands prefixed with `felix` trigger the LLM pipeline
- Boot animation simulates an AI-powered OS startup

## Pluggable LLM Backend
Supported models:
- DeepSeek Coder 1.3B (default)
- Microsoft Phi
- GPT-Neo 1.3B
- Nova-1.3B
- FIM-NeoX

Built using Transformers + Accelerate + Torch.

## Security Warning
FelixOS executes generated scripts using bash.  
Do NOT run untrusted prompts on machines with sensitive data.

## Project Structure
main.py
model_utils.py
docs/OS_Report.pdf
requirements.txt
.gitignore
README.md

Auto-generated runtime folders:
ready_files/
running_files/
finished_files/

## Installation

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

## Usage
python main.py

Use AI commands:
    felix open youtube and search for classical music

## How It Works
1. User input
2. Detect `felix`
3. Build LLM instruction
4. Generate script
5. Save timestamped script
6. FCFS picks oldest
7. Execute bash script
8. Move to finished_files/
9. Display output

## Documentation
See docs/OS_Report.pdf
