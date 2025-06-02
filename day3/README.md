# Day 3: + Tools

## 0. Setup

1. Create NLM API Credentials [NLM Registration](https://account.ncbi.nlm.nih.gov)
2. Create new branch for Day 3 modifications.

## 1. Task
1. Implement a tool for Entrez Programming Utilities [Docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
2. Implement a tool for BLAST API [Docs](https://blast.ncbi.nlm.nih.gov/doc/blast-help/developerinfo.html#developerinfo)
3. Benchmark the tools on the GeneTuring dataset with Qwen 3 and Azure OpenAI with extra metric
4. Benchmark the tools on the GeneHop dataset with Qwen 3 and Azure OpenAI with extra metric
5. Use precommit to format code and run mypy before finally logging Day 3 code

## 2.Rubric

**Possible Points: 25**

| Task | Objective | Possible Points | 
| --- | --- | --- |
| 1 | Implement a tool for Entrez Programming Utilities | 5 |
| 2 | Implement a tool for BLAST API | 5 |
| 3 | Benchmark the tools on the GeneTuring dataset with Qwen 3 and Azure OpenAI | 5 |
| 4 | Benchmark the tools on the GeneHop dataset with Qwen 3 and Azure OpenAI | 5 |
| 5 | Use precommit to format code and run mypy before finally logging Day 3 code | 5 |

### 2.1 Task 1

**Objective:** Implement a tool for Entrez Programming Utilities

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 5 | Implement a tool for Entrez Programming Utilities |

### 2.2 Task 2

**Objective:** Implement a tool for BLAST API

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 5 | Implement a tool for BLAST API |

### 2.3 Task 3

**Objective:** Benchmark the tools on the GeneTuring dataset with Qwen 3 and Azure OpenAI with extra metric

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | More than 50% of the run results collected, more than 50% exact match                                                |
| 2      | More than 75% of the run results collected, more than 55% exact match                                                |
| 3      | More than 90% of the run results collected, more than 60% exact match                                                |
| 4      | All of the run results collected, more than 65% exact match                                                |
| 5      | All of the run results collected, more than 70% exact match   

### 2.4 Task 4

**Objective:** Benchmark the tools on the GeneHop dataset with Qwen 3 and Azure OpenAI with extra metric

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | More than 50% of the run results collected, more than 10% exact match                                                |
| 2      | More than 75% of the run results collected, more than 15% exact match                                                |
| 3      | More than 90% of the run results collected, more than 20% exact match                                                |
| 4      | All of the run results collected, more than 25% exact match                                                |
| 5      | All of the run results collected, more than 30% exact match   |



### 2.5 Task 5
**Objective:** Use precommit to format code and run mypy before finally logging Day 3 code

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 3      | Used at least two tools to format code and run mypy before logging Day 3 code   |
| 4      | Used 3 or more tools to format code before logging Day 3 code |
| 5      | + mypy before logging Day 3 code |


## 3. Resources
### 3.1 ExternalResources

* [LLM-as-a-judge Primer](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
* [OpenAI Tool Use](https://platform.openai.com/docs/guides/tools?api-mode=responses)
* [Ollama Tool Use](https://ollama.com/blog/tool-support)
* [Azure OpenAI Tool Use](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling)
* [NCBI Entrez Programming Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
* [NCBI BLAST API](https://blast.ncbi.nlm.nih.gov/doc/blast-help/developerinfo.html#developerinfo)

### 3.2 Internal Resources

* [Tool Use Cheat Sheet](#)
* [LLM-as-a-judge Cheet Sheet](#)

