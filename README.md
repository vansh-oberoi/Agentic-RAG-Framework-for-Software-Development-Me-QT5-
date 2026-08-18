# Agentic RAG Framework for Software Development — Me-QT5

> An agentic Retrieval-Augmented Generation framework for software development that combines context retrieval, context filtering, task-complexity evaluation, specialized language models, and coding-agent workflows.

---

## Overview

Modern coding agents can generate and modify software effectively, but their performance depends heavily on the quality and relevance of the context provided to them.

Large software repositories contain significant amounts of information, much of which may be irrelevant to a particular development task. Providing excessive or noisy context can increase computational cost and make it more difficult for an agent to identify the information that actually matters.

**Me-QT5** explores an agentic approach to this problem by integrating retrieval, context filtering, task-complexity evaluation, and specialized language models into a software-development workflow.

The framework focuses on:

- Retrieving potentially relevant software-development context
- Filtering irrelevant or redundant context
- Evaluating the complexity of development tasks
- Providing focused context to downstream coding agents
- Using specialized T5-based models for task-specific components
- Evaluating the framework on coding-oriented tasks

The overall objective is to investigate how **retrieval, context selection, and task-aware reasoning** can support more effective agentic software-development workflows.

---

## Key Features

### Agentic Retrieval-Augmented Generation

The framework integrates retrieval into an agentic software-development workflow rather than treating RAG as an isolated question-answering system.

Relevant information is retrieved and processed before being provided to the downstream coding workflow.

### Context Filtering

A dedicated context-filtering component processes retrieved information and attempts to identify information that is more relevant to the current software-development task.

This helps reduce unnecessary context passed to downstream models.

### Task Complexity Evaluation

Software-development tasks can vary considerably in difficulty.

The framework incorporates a complexity-evaluation component that analyzes development tasks and provides a task-complexity signal within the workflow.

### Specialized T5 Models

The framework uses **T5-based language models** for specialized components of the system, including context filtering and complexity evaluation.

This modular approach allows individual components to be designed for specific subtasks rather than relying exclusively on a single general-purpose model.

### Coding-Agent Workflow

The framework combines retrieval, context processing, task analysis, and generation into a broader workflow intended to support coding-agent systems.

---

# System Architecture

```text
                         ┌──────────────────────┐
                         │   Software Task      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Task Analysis     │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Context Retrieval│          │ Task Complexity  │
          │                  │          │   Evaluation     │
          └────────┬─────────┘          └────────┬─────────┘
                   │                             │
                   ▼                             │
          ┌──────────────────┐                   │
          │ Context Filterer │                   │
          └────────┬─────────┘                   │
                   │                             │
                   └──────────────┬──────────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ Focused Task Context │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    Coding Agent      │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ Software Development │
                       │      Response        │
                       └──────────────────────┘
```

---

# Why Agentic RAG for Software Development?

A conventional RAG system generally follows a relatively simple pipeline:

```text
Query
  ↓
Retrieve Documents
  ↓
Generate Answer
```

Software-development tasks introduce additional challenges. A coding task may require:

- Understanding the task
- Identifying relevant repository context
- Distinguishing useful information from irrelevant information
- Estimating task complexity
- Supplying the coding model with focused context
- Generating a solution based on the selected information

Me-QT5 therefore explores a more structured workflow:

```text
Task
 ↓
Retrieve
 ↓
Filter
 ↓
Evaluate
 ↓
Reason
 ↓
Generate
```

This makes retrieval and context management explicit components of the software-development agent.

---

# Core Components

## 1. Context Retrieval

The retrieval component identifies potentially relevant information for a given software-development task.

The retrieved information acts as the initial context available to subsequent components of the workflow.

---

## 2. Context Filterer

The context-filtering stage processes retrieved information and attempts to remove or reduce information that is less relevant to the current task.

The objective is to provide the downstream coding agent with a more focused context instead of forwarding all retrieved information.

---

## 3. Complexity Evaluator

Software-development tasks differ significantly in their level of difficulty.

The complexity evaluator provides a task-level complexity signal that can be incorporated into the overall agentic workflow.

This enables the framework to explicitly consider task complexity during the software-development process.

---

## 4. Specialized Language Models

The framework incorporates specialized **T5-based language models** for individual components.

These models are used for task-specific functionality such as:

- Context filtering
- Complexity evaluation

Using specialized models allows individual components to be optimized for their respective roles within the overall pipeline.

---

## 5. Coding Agent

The final stage of the workflow provides the processed information to a coding-oriented agent.

The coding agent can use the retrieved and filtered context to address software-development tasks.

The framework therefore treats retrieval and context selection as supporting components of a larger agentic software-engineering workflow.

---

# Dataset

The project includes a curated dataset designed around software-development and coding-agent tasks.

The dataset provides resources for experimentation and evaluation of the framework and its specialized components.

The repository contains the associated dataset archive and supporting project resources.

---

# Model Training

The framework includes specialized T5-based models for individual components of the system.

The project contains resources associated with:

- Context filtering
- Complexity evaluation
- Model training
- Model evaluation

This modular approach allows individual components to be developed and evaluated independently within the overall agentic pipeline.

---

# Evaluation

The framework is evaluated using software-development-oriented tasks and associated project resources.

Evaluation considers the effectiveness of the framework components and their role within the overall agentic workflow.

Detailed experimental methodology and results are provided in the project report included in the repository.

> Specific quantitative results are intentionally not reproduced here unless they are directly verified from the corresponding experimental materials.

---

# Repository Structure

```text
Agentic_Framework_for_Software_Development/
│
├── 53_h3_pathway_endterm.pdf       # Project report / technical documentation
├── dataset.zip                     # Dataset used for experiments
├── fine_tuned_models.txt           # Fine-tuned model references and resources
├── README.md                       # Project documentation
├── working_demo.mp4                # Demonstration of the framework
│
└── Me-QT5/
    │
    ├── Dockerfile                  # Container configuration
    ├── readme.md                   # Me-QT5-specific documentation
    ├── run.sh                      # Framework execution script
    ├── setup.sh                    # Environment setup script
    │
    └── Code/
        ├── agent.py                # Core agent implementation
        ├── agent_store.py          # Agent state / storage
        ├── complexity_evaluator.py # Task complexity evaluation
        ├── custom_generate.py      # Custom generation utilities
        ├── database.py             # Database interface
        ├── filter.py               # Context filtering
        ├── hr_database.txt         # Supporting knowledge base
        ├── llm_ui.py               # LLM user interface
        ├── memory.py               # Agent memory
        ├── prompts.py              # Prompt definitions
        ├── query_decomposer.py     # Query/task decomposition
        ├── rag-server.py           # RAG server
        ├── ragclient.py            # RAG client
        ├── Readme.md               # Code-level documentation
        ├── requirements.txt        # Python dependencies
        ├── sandbox.py              # Sandboxed execution
        ├── variables.py            # Configuration variables
        └── wrapper.py              # Framework integration wrapper
```

---

# Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Deep Learning | PyTorch |
| NLP | Hugging Face Transformers |
| Language Models | T5 |
| AI Architecture | Agentic RAG |
| Application Domain | Software Engineering |
| Data Processing | Python-based tooling |
| Evaluation | Coding / software-development benchmarks |

---

# Getting Started

## Prerequisites

Recommended environment:

- Python 3.14.7
- Git
- PyTorch
- Hugging Face Transformers
- Required dependencies listed in the project configuration

---

## Clone the Repository

```bash
git clone https://github.com/vansh-oberoi/Agentic-RAG-Framework-for-Software-Development-Me-QT5.git

cd Agentic-RAG-Framework-for-Software-Development-Me-QT5
```

---

## Install Dependencies

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r Me-QT5/Code/requirements.txt
```

---

# Running the Framework

The main implementation is located inside:

```text
Me-QT5/Code/
```

The project includes scripts and modules for:

- Agent execution
- Retrieval
- Context filtering
- Query decomposition
- Complexity evaluation
- Memory management
- RAG client/server communication
- Model generation
- Sandboxed execution
- User interaction

The project also includes:

- `setup.sh` for environment setup
- `run.sh` for execution
- `Dockerfile` for containerized deployment

Refer to the project-specific documentation in `Me-QT5/readme.md` and `Me-QT5/Code/Readme.md` for implementation-specific instructions.

---

# Workflow

At a high level, the framework follows:

```text
                    Software Development Task
                              │
                              ▼
                       Task Decomposition
                              │
                              ▼
                       Context Retrieval
                              │
                              ▼
                       Context Filtering
                              │
                              ▼
                    Complexity Evaluation
                              │
                              ▼
                       Focused Context
                              │
                              ▼
                         Coding Agent
                              │
                              ▼
                    Generated Solution
```

The modular architecture allows individual stages of the workflow to be analyzed and improved independently.

---

# Design Principles

## Modularity

Major capabilities are separated into individual components, allowing them to be developed, evaluated, and modified independently.

## Task-Aware Context

The framework focuses on providing context relevant to the specific software-development task instead of treating all retrieved information equally.

## Specialized Models

Task-specific models are used for specialized components such as filtering and complexity evaluation.

## Agentic Workflow

Multiple information-processing and reasoning stages are coordinated as part of a broader software-development workflow.

---

# Potential Applications

The architecture can be applied to software-engineering scenarios such as:

- Repository-level code understanding
- Code generation
- Code modification
- Issue resolution
- Software debugging
- Developer assistance
- Repository question answering
- Context-aware coding agents
- Automated software-development workflows

---

# Future Directions

Potential directions for extending the framework include:

- Hybrid dense + lexical retrieval
- Semantic code chunking
- Cross-encoder reranking
- Repository-level dependency graphs
- Long-term conversational memory
- GitHub-native repository ingestion
- Retrieval-quality benchmarking
- Agent trajectory evaluation
- Latency and cost optimization
- Multi-agent software-development workflows
- Human-in-the-loop feedback
- Improved observability and tracing

---

# Project Context

Me-QT5 is an agentic Retrieval-Augmented Generation framework for software development that integrates retrieval, context filtering, task-complexity evaluation, specialized language models, and coding-agent workflows.

The project explores how structured context selection and task-aware processing can improve software-development workflows involving large language models.

---

# Future Directions

Potential extensions include:

- Hybrid dense + lexical retrieval
- Semantic code chunking
- Cross-encoder reranking
- Repository-level dependency graphs
- Long-term conversational memory
- GitHub-native repository ingestion
- Retrieval-quality benchmarking
- Agent trajectory evaluation
- Latency and cost optimization
- Multi-agent software-development workflows
- Human-in-the-loop feedback
- Improved observability and tracing

---

# Author

**Vansh Oberoi**

GitHub:  
https://github.com/vansh-oberoi

---

## Keywords

`Agentic AI` · `RAG` · `Retrieval-Augmented Generation` · `LLM` · `Coding Agents` · `Software Engineering` · `T5` · `Transformers` · `PyTorch` · `Context Retrieval` · `Context Filtering` · `Task Complexity` · `AI Agents` · `Machine Learning`
