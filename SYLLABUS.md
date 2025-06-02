# LLMOps: A Practical Introduction to Software Engineering with LLMs

## Syllabus

**Table of Contents**
* [Instructors & Contact Info](#instructors--contact-info)
* [Course Overview](#course-overview)
* [Learning Objectives](#learning-objectives)
* [Tools & Infrastructure](#tools--infrastructure)
* [Project Framework: BioLLM Explorer](#project-framework-biollm-explorer)
* [Daily Schedule](#daily-schedule)
  * [Day 1 (Monday): Local LLMs, Test Harness Setup, Basic Benchmarking & DevOps Intro (Room: G9.250A)](#day-1-monday-local-llms-test-harness-setup-basic-benchmarking--devops-intro-room-g9250a)
  * [Day 2 (Tuesday): Proprietary APIs, Structured Outputs, Advanced Benchmarking (Gene Hop) & Evaluation (Room: NL03.120)](#day-2-tuesday-proprietary-apis-structured-outputs-advanced-benchmarking-gene-hop--evaluation-room-nl03120)
  * [Day 3 (Wednesday): Tool Use, RAG Concepts & Code Interpreter (Room: NL03.120)](#day-3-wednesday-tool-use-rag-concepts--code-interpreter-room-nl03120)
  * [Day 4 (Thursday): Refinement, Advanced Integration, Documentation & Demos (Room: NL03.120)](#day-4-thursday-refinement-advanced-integration-documentation--demos-room-nl03120)
* [Grading Rubric (20 points total)](#grading-rubric-20-points-total)
* [Implementation Note](#implementation-note)
* [Ethics & Data Privacy](#ethics--data-privacy)
* [Dataset Information](#dataset-information)
* [Pre-Readings & Preparation (Optional but Encouraged)](#pre-readings--preparation-optional-but-encouraged)
* [Project Guide](#project-guide)

**Dates:** June 2-5, 2025

**Room Assignments:**
*   **Monday:** G9.250A
*   **Tuesday - Thursday:** NL03.120

<a id="instructors--contact-info"></a>
**Instructors & Contact Info**
| Instructor          | Email                                   |
| :------------------ | :-------------------------------------- |
| Andrew Jamieson     | Andrew.jamieson@utsouthwestern.edu      |
| Michael Holcomb     | Michael.Holcomb@UTSouthwestern.edu      |
| David Hein          | david.hein@UTSouthwestern.edu           |
| Ameer Hamza Shakur  | AmeerHamza.Shakur@UTSouthwestern.edu    |

<a id="course-overview"></a>
**Course Overview**

This module provides a practical, hands-on introduction to large language models (LLMs) in biomedical research and software development. Students will incrementally build a single project—a **BioLLM Explorer (inspired by concepts like GeneGPT)**—throughout the four days. This involves setting up local LLM serving (Ollama on BioHPC), interacting with local and proprietary LLM APIs, implementing tool use for accessing external biomedical data (e.g., NCBI), and applying sound software engineering practices (version control, testing, MLflow for experiment tracking, modular design, documentation, and evaluation). The module emphasizes independent problem-solving with a focus on building a robust "test harness" and iteratively developing capabilities.

<a id="learning-objectives"></a>
**Learning Objectives**
*   Set up and run local LLMs via an API (Ollama on BioHPC).
*   Develop a "test harness" to benchmark LLM performance on biomedical tasks (e.g., GeneTuring, Gene Hop).
*   Utilize MLflow for experiment tracking and results logging.
*   Integrate proprietary LLM APIs (e.g., OpenAI/Azure) and implement best practices (key management, retries).
*   Implement structured outputs from LLMs (schema-based vs. function calling).
*   Design and implement "tool use" for LLMs to interact with external data sources (NCBI APIs, web search, code interpreters).
*   Apply software engineering best practices: Git, unit/integration testing (pytest), modular design, AI IDE usage.
*   Understand and apply various LLM evaluation metrics (exact match, semantic similarity, LLM-as-a-judge concepts).
*   Create maintainable documentation and deliver a project demonstration.

<a id="tools--infrastructure"></a>
**Tools & Infrastructure**
*   Development Environment: Python 3.10+, venv, VSCode (or other AI-assisted IDEs).
*   Version Control: GitHub.
*   Compute Resources: **BioHPC CPU nodes.**
*   Local LLM Serving: **Ollama (with models like Gemma 3, Granite 3.3).**
*   Experiment Tracking: **MLflow (initially local, potentially a shared server).**
*   Python Libraries: transformers, sentence-transformers, pytest, OpenAI API, **NCBI Entrez API**, httpx/requests, MLflow client.
*   Environment Management: uv + pyproject.toml.

<a id="project-framework-biollm-explorer"></a>
**Project Framework: BioLLM Explorer**
Students will build a command-line tool and associated "test harness" to evaluate LLM performance on specific biomedical question-answering tasks (e.g., "GeneTuring," "Gene Hop"). The project will involve:
1.  Setting up local LLM serving with Ollama on BioHPC.
2.  Creating scripts to call local and remote LLM APIs.
3.  Implementing functions to process benchmark datasets and log results to MLflow.
4.  Developing structured output parsing.
5.  Integrating various "tools" (e.g., NCBI API clients, web search functions, a Python code interpreter) for the LLM to use, enhancing its ability to answer complex, multi-hop questions.
Students will progressively build and evaluate their system, applying software engineering best practices throughout.

---

<a id="daily-schedule"></a>
**Daily Schedule**

<a id="day-1-monday-local-llms-test-harness-setup-basic-benchmarking--devops-intro-room-g9250a"></a>
**Day 1 (Monday): Local LLMs, Test Harness Setup, Basic Benchmarking & DevOps Intro (Room: G9.250A)**
*   **9:00–9:45 AM: Course Overview & LLM Fundamentals** (Lecture) - Andrew
    *   Broad overview of LLMs, key concepts, model landscape.
*   **9:45–10:30 AM: Project Introduction & Day 1 Task: GeneTuring Test Harness** (Lecture/Demo) - Mike
    *   Overall project vision: Biomedical Text Analysis Assistant.
    *   Day 1 Goal: Set up a test harness for the "GeneTuring" benchmark.
    *   Brief on basic evaluation (e.g., exact match for GeneTuring) & MLflow setup.
*   **10:30 AM–3:00 PM: Lab/Self-study (with lunch break)**
    *   Access BioHPC CPU nodes.
    *   Set up Ollama with a provided model (e.g., Gemma 3).
    *   Develop Python scripts to:
        *   Call the local Ollama API.
        *   Process the "GeneTuring" dataset.
        *   Log prompts, responses, and basic evaluation scores to a local MLflow instance.
    *   Initial function wrapping and basic code structure.
*   **3:00–4:00 PM: DevOps Concepts & Git Best Practices** (Lecture) - Andrew
    *   Git workflows (branching, merging, PRs).
    *   Introduction to unit testing.
    *   Importance of modular design.
    *   *(Students apply Git to their Day 1 work post-lecture or start of Day 2 lab)*

<a id="day-2-tuesday-proprietary-apis-structured-outputs-advanced-benchmarking-gene-hop--evaluation-room-nl03120"></a>
**Day 2 (Tuesday): Proprietary APIs, Structured Outputs, Advanced Benchmarking (Gene Hop) & Evaluation (Room: NL03.120)**
*   **9:00–10:00 AM: Structured Outputs & API Best Practices** (Lecture) - Dave
    *   Schema-based structured outputs vs. function calling (pros/cons).
    *   Integrating proprietary APIs (OpenAI/Azure): key management, .env files, retry logic, error handling.
*   **10:00–10:30 AM: Day 2 Task: "Gene Hop" Benchmark & Frontier Models** (Introduction) - Mike
    *   Introduce the more complex "Gene Hop" dataset requiring multi-hop reasoning.
    *   Discuss using frontier models (via API) for more challenging tasks.
*   **10:30 AM–3:00 PM: Lab/Self-study (with lunch break)**
    *   Integrate proprietary LLM APIs (e.g., OpenAI) into their test harness.
    *   Implement structured output generation/parsing for "GeneTuring" and/or "Gene Hop" tasks.
    *   Extend their test harness to run the "Gene Hop" benchmark, logging to MLflow.
    *   Write unit tests for API interaction and data processing logic.
    *   Compare local vs. proprietary model performance on tasks.
*   **3:00–4:00 PM: Advanced Evaluation Metrics & LLM-as-a-Judge Teaser** (Mini-Lecture) - Mike
    *   Beyond exact match: fuzzy matching, semantic similarity (e.g., BERTscore).
    *   Concept of LLM-as-a-judge for more nuanced evaluation.

<a id="day-3-wednesday-tool-use-rag-concepts--code-interpreter-room-nl03120"></a>
**Day 3 (Wednesday): Tool Use, RAG Concepts & Code Interpreter (Room: NL03.120)**
*   **9:00–10:30 AM: LLM Tool Use & RAG as a Tool** (Lecture/Demo) - Mike/Ameer
    *   Core concepts of LLM agents and tool use.
    *   Designing tools: NCBI API wrappers, web search functions.
    *   RAG: Conceptually as retrieval from existing knowledge bases (APIs) or local stores.
    *   Introduction to using a local Python code interpreter as an LLM tool.
*   **10:30 AM–3:00 PM: Lab/Self-study (with lunch break)**
    *   Develop and integrate "tools" into their assistant for the "Gene Hop" task:
        *   Wrapper for NCBI Entrez API (e.g., to search PubMed or Gene databases).
        *   Potentially a simple web search tool.
    *   Modify prompts/logic to enable the LLM to utilize these tools.
    *   *Optional/Bonus:* Set up and integrate a local Python code interpreter (with BioPython) as a tool.
    *   *Optional/Bonus:* If very advanced, build a small custom vector DB for a specific set of documents and use it as a retrieval tool.
    *   Evaluate the impact of tool use on "Gene Hop" performance, log to MLflow.
*   **3:00-4:00 PM: Peer Code Review / Q&A / TA Session** - Instructor Team

<a id="day-4-thursday-refinement-advanced-integration-documentation--demos-room-nl03120"></a>
**Day 4 (Thursday): Refinement, Advanced Integration, Documentation & Demos (Room: NL03.120)**
*   **9:00–9:30 AM: Q&A / Optional Advanced Topic Demo** (e.g., complex agent loops, advanced MLflow usage) - Instructor Team
*   **9:30 AM–3:00 PM: Lab/Wrap-up & Demo Preparation (with lunch break)**
    *   Refine project: improve code quality, modularity, error handling, tests.
    *   Finalize MLflow logging and experiment comparison.
    *   Complete README documentation: project description, setup, how to run, design choices, key findings/evaluation results.
    *   Prepare final demonstration.
*   **3:00-5:00 PM: Final Demonstrations & Code Submission** - Instructor Team
    *   Students present their "BioLLM Explorer" and their findings.
    *   Code submission.

---

<a id="grading-rubric-20-points-total"></a>
**Grading Rubric (20 points total)**
| Category                                  | Points | Details                                                                                                                                           |
| :---------------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| Local LLM (Ollama) & Test Harness Setup   | 4      | Successfully sets up Ollama on BioHPC, calls local API, processes "GeneTuring" task, logs to MLflow, basic Git usage.                             |
| Proprietary API & Structured Output       | 4      | Integrates proprietary API, implements structured outputs, handles API keys securely, robust API calling (retries).                                   |
| Tool Use Implementation & "Gene Hop" Task | 4      | Implements ≥1 LLM tool (e.g., NCBI API, web search), integrates for "Gene Hop" task, evaluates tool impact.                                          |
| Software Engineering/DevOps               | 4      | Effective Git use (branches, meaningful commits), 3-5 meaningful unit/integration tests (pytest), modular code design.                            |
| Documentation, Evaluation & Demo          | 4      | Clear README, effective demonstration, explains design choices, discusses evaluation methods applied and results from MLflow for different tasks. |

<a id="implementation-note"></a>
**Implementation Note**
Focus on a working "test harness" and demonstrating core concepts: local/remote API calls, MLflow, structured outputs, and basic tool use. Quality of implementation, testing, and clear articulation of evaluation are key. Advanced tool integration, RAG knowledge base building, or even GUIs are stretch goals.

<a id="ethics--data-privacy"></a>
**Ethics & Data Privacy**


<a id="dataset-information"></a>
**Dataset Information**
Students will primarily work with benchmark datasets like **"GeneTuring" and "Gene Hop"** (details/links to be provided). Interaction with public NCBI databases (PubMed, Gene, etc.) via their Entrez API will be central to tool-use tasks. Ollama models (e.g., Gemma 3, Granite 3.3) will be used for local LLM serving, pending BioHPC availability.

<a id="pre-readings--preparation-optional-but-encouraged"></a>
**Pre-Readings & Preparation (Optional but Encouraged)**
*   Attention Is All You Need (Vaswani et al.)
*   OpenAI API Documentation - Chat Completions and Embeddings endpoints
*   NCBI Entrez Programming Utilities Documentation
*   **Ollama Documentation (especially API interaction)**
*   **MLflow Quickstart/Documentation (Python API)**
*   Hugging Face Transformers Quickstart (conceptual)
*   PyTest Introduction
*   (Optional) Gene GPT Paper (Jin et al., 2023) ([Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10153281/), [Code](https://github.com/ncbi/GeneGPT))

---

## Project Guide

For detailed information about the project, please see the [Project Overview Guide](PROJECT_GUIDE.md).
