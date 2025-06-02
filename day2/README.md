# Day 2: OpenAI + GeneHop

## 0. Setup

1. Populate .env file with Azure OpenAI credentials
2. Download GeneHop dataset
3. Create new branch for Day 2 modifications.

## 1. Task
1. Refactor Day 1 code to add benchmarking for GeneHop with structured output
2. Run the script and collect results for Qwen 3 on GeneHop
3. Refactor code to add benchmarking for Azure OpenAI on GeneTuring and GeneHop with structured output
4. Run the script and collect results for Azure OpenAI model on GeneTuring and GeneHop
5. Use precommit to format code and run mypy before finally logging Day 2 code

## 2.Rubric

**Possible Points: 25**

| Task | Objective | Possible Points | 
| --- | --- | --- |
| 1 | Refactor Day 1 code to add benchmarking for GeneHop with structured output | 5 |
| 2 | Run the script and collect results for Qwen 3 on GeneHop | 5 |
| 3 | Refactor code to add benchmarking for OpenAI on GeneTuring and GeneHop with structured output | 5 |
| 4 | Run the script and collect results for OpenAI model on GeneTuring and GeneHop | 5 |
| 5 | Use precommit to format code and run mypy before finally logging Day 2 code | 5 |

### 2.1 Task 1
**Objective:** Refactor Day 1 code to add benchmarking for GeneHop with structured output

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 3 | Implement GeneHop benchmarking with Qwen 3 |
| 4 | + Implement structured output for GeneHop |
| 5 | + Implement new metric for GeneHop |

### 2.2 Task 2
**Objective:** Run the script and collect results for Qwen 3 on GeneHop

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | More than 50% of the run results collected
| 2      | More than 75% of the run results collected
| 3      | More than 90% of the run results collected
| 4      | All of the run results collected
| 5      | All of the run results collected, more than 10% exact match         

### 2.3 Task 3
**Objective:** Refactor code to add benchmarking for OpenAI on GeneTuring and GeneHop with structured output

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 3| Implement Azure OpenAI benchmarking |
| 4 | + Implement structured output for Azure OpenAI |
| 5 | + Implement new metric for Azure OpenAI |

### 2.4 Task 4
**Objective:** Run the script and collect results for Azure OpenAI model on GeneTuring and GeneHop

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | More than 50% of both of the run results collected, more than 1% exact match                                                |
| 2      | More than 75% of both of the run results collected, more than 5% exact match                                                |
| 3      | More than 90% of both of the run results collected, more than 10% exact match                                                |
| 4      | All of the run results collected, more than 15% exact match                                                |
| 5      | All of the run results collected, more than 20% exact match    |

### 2.5 Task 5
**Objective:** Use precommit to format code and run mypy before finally logging Day 2 code

**Possible Points: 5**
| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 3      | Used at least two tools to format code and run mypy before logging Day 2 code   |
| 4      | Used 3 or more tools to format code before logging Day 2 code |
| 5      | + mypy before logging Day 2 code |

# 3. Resources
### 3.1 ExternalResources

* [Ollama Structured Output](https://ollama.com/blog/structured-outputs)
* [Azure OpenAI Structured Output](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/structured-outputs?tabs=python-secure%2Cdotnet-entra-id&pivots=programming-language-python)
* [OpenAI Structured Output](https://openai.com/index/introducing-structured-outputs-in-the-api/)

### 3.2 Internal Resources

* [Structured Output Cheat Sheet](./resources/StructuredOutput.md)
* [Azure OpenAI ChatCompletions Cheat Sheet](./resources/AzureOpenAI.md)
* [NLP Metrics Definitions Cheat Sheet](./resources/AltMetrics.md)

