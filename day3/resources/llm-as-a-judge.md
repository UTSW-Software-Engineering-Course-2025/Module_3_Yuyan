Here's a concise cheat sheet (under 500 words) in Markdown format, tailored for graduate students with an academic tone:

---

# Cheat Sheet: Using LLMs-as-a-Judge

Large Language Models (LLMs) can be used to evaluate outputs from other models, particularly in research and tool-using settings. Two dominant evaluation paradigms are **pairwise selection** and **rubric-based (solo) grading**.

---

## Modes of LLM-as-a-Judge

### 1. Pairwise Selection (Comparison Judge)

LLMs compare two outputs (A and B) for a given input and select the better one.

**Use Cases:** Benchmarking model improvements, A/B testing.

**Prompt Structure:**

* Input (e.g., question or task)
* Response A
* Response B
* Evaluation criteria (e.g., accuracy, coherence, correctness)
* System prompt: *“Given the question and responses, select the better answer and explain why.”*

**Output Format:**

* Choice: A or B
* Rationale: Text justification

---

### 2. Rubric-Based Grading (Metric Judge)

LLMs assess a single response against a detailed rubric or gold standard.

**Use Cases:** Automated evaluation in dataset creation, longitudinal model testing.

**Prompt Structure:**

* Input (e.g., question)
* Candidate response
* Gold standard (optional)
* Rubric (structured or free-form)
* System prompt: *“Evaluate the response based on the rubric. Provide a score and explanation.”*

**Output Format:**

* Score (e.g., 1–5 scale)
* Explanation

---

## Prompt Elements

Effective prompts contain the following:

* **Clear context:** Task definition, background
* **Explicit criteria:** What constitutes a good answer?
* **Standardized structure:** Consistent formatting for traceability
* **Instructional tone:** Direct LLM to act as a careful grader

> Avoid vague prompts. Specificity enhances grading reliability and reduces hallucinations.

---

## Azure OpenAI Example (Rubric-Based)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
deployment_name = "gpt-4-judge"

def evaluate_trace(question, candidate, gold, rubric):
    prompt = f"""You are a domain expert grading an AI response.

Question:
{question}

Candidate Answer:
{candidate}

Gold Standard Answer:
{gold}

Rubric:
{rubric}

Instructions:
Score the candidate's answer on a scale of 1 to 5 based on the rubric. Provide a justification for the score.
Return your answer in this format:
Score: X
Explanation: ...
"""
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a meticulous evaluator following an academic grading rubric."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

# Example usage
question = "What is the capital of France?"
candidate = "The capital of France is Lyon."
gold = "The capital of France is Paris."
rubric = "Correctness of factual information."

print(evaluate_trace(question, candidate, gold, rubric))
```

---

## References

* [Liu et al., 2023. "Evaluating Language Models with LLMs."](https://arxiv.org/abs/2310.19736)
* OpenAI documentation: [https://learn.microsoft.com/en-us/azure/cognitive-services/openai](https://learn.microsoft.com/en-us/azure/cognitive-services/openai)
* [Zhuge et al., 2024. "Agent-as-a-Judge: Evaluate Agents with Agents."](https://arxiv.org/pdf/2410.10934)