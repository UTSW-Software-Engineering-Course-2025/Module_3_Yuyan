# 1.1 Place imports here
import json
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, List, Optional

import mlflow
import pandas as pd
from openai import AzureOpenAI
from tqdm import tqdm

# 2.1 Data Configuration

mlflow.set_tracking_uri("http://198.215.61.34:8153")
mlflow.set_experiment("s440914_1")

# 2.2 Model Configuration

# 2.3 Evaluation and Logging Configuration
AZURE_OPENAI_KEY = "FJ5GrEV5LG3Y0UIeac29BIhmVu8GPcmWyeTTFH0cBifgT7T68XHPJQQJ99BEACHYHv6XJ3w3AAAAACOGdwHb"
AZURE_OPENAI_ENDPOINT = (
    "https://michaelholcomb-5866-resource.cognitiveservices.azure.com/"
)
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4.1"
AZURE_OPENAI_API_VERSION = "2024-03-01-preview"

# 3.1 Load the JSON file


with open("./data/geneturing.json", "r") as f:
    data = json.load(f)
# Load the data here

# Build the TASKS variable here

TASKS = set(data)


# 3.2 Iterate through the JSON data recursively to collect each of the rows into a list
#     Each row should have a dictionary with keys of the columsn in the table above
rows = []

# Recursively iterate through each task and its Q&A pairs
for task, qas in data.items():
    for question, answer in qas.items():
        rows.append({"task": task, "question": question, "answer": answer})

# Preview first 3 rows
for row in rows[:3]:
    print(row)

# 3.3 Create the pandas dataframe from the collection of rows

df = pd.DataFrame(rows)

# 4.1 Setting up the large language model Ollama model client
client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)


# 4.2 Draft your own system prompt for our generic genomics question answering system.
#     Replace the system message `content` below with your own.
system_message = [
    {
        "role": "system",
        "content": "Hello. Your task is to use NCBI Web APIs to answer genomic questions.Please only answer the question concisely and don't generate to many other stuff. If you can specify the answer, please put it after word Answer. If you are not sure about the answer, please try to be concise and give a brief guess based on the NCBI results.",
    }
]

response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "What is the official gene symbol of LMP10?",
        },
        {
            "role": "assistant",
            "content": "The official gene symbol of LMP10 is PSMB10.",
        },
        {
            "role": "user",
            "content": "What is the official gene symbol of SNAT6?",
        },
    ],
    max_tokens=800,  # fixed
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=AZURE_OPENAI_DEPLOYMENT_NAME,
)

print(response.choices[0].message.content)


# 4.4 Implement THE model function


def query_model(
    client: AzureOpenAI,
    system_message: dict,
    few_shot_examples: List[dict],
    user_query: str,
) -> str:
    """
    Query the language model with few-shot examples and a user query.
    Returns the extracted answer string.
    """

    # Combine message components
    messages = (
        system_message + few_shot_examples + [{"role": "user", "content": user_query}]
    )

    # Call the model
    response = client.chat.completions.create(
        messages=messages,
        max_tokens=800,  # correct param name
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
    )

    # Extract content
    response_content = response.choices[0].message.content.strip()

    # Try to extract the part after "Answer:" if present
    if "Answer:" in response_content:
        answer = response_content.split("Answer:")[-1].strip()
    else:
        answer = response_content  # fallback

    return answer


# 5.1 Implement metrics


def exact_match(pred: str, true: str) -> float:
    pred = pred.lower().strip()
    true = true.lower().strip()
    return float(true in pred)


def gene_disease_association(pred: List[str], true: List[str]) -> float:
    pred_set = set(map(str.strip, pred))
    true_set = set(map(str.strip, true))
    if not true_set:
        return 1.0 if not pred_set else 0.0
    return len(pred_set & true_set) / len(true_set)


def disease_gene_location(pred: List[str], true: List[str]) -> float:
    pred_set = set(map(str.strip, pred))
    true_set = set(map(str.strip, true))
    if not true_set:
        return 1.0 if not pred_set else 0.0
    return len(pred_set & true_set) / len(true_set)


def human_genome_dna_alignment(pred: str, true: str) -> float:
    # Assuming the format 'chrX:position1-position2'
    def extract_chromosome(s: str) -> str:
        return s.strip().split(":")[0] if ":" in s else s.strip()

    pred_chr = extract_chromosome(pred)
    true_chr = extract_chromosome(true)
    if pred_chr == true_chr:
        return 0.5 if pred.strip() != true.strip() else 1.0
    return 0.0


metric_task_map = defaultdict(
    lambda: exact_match,
    {
        "gene_disease_association": gene_disease_association,
        "disease_gene_location": disease_gene_location,
        "human_genome_dna_alignment": human_genome_dna_alignment,
    },
)


import re


def get_answer(answer: str, task: str) -> str:
    answer = answer.strip()

    if task in ["Gene alias", "Gene location", "SNP location"]:
        # Extract last word that looks like a gene symbol (alphanumeric, all caps)
        match = re.findall(r"[A-Z0-9\-]+", answer)
        if match:
            return match[-1]  # Return last match (usually the actual symbol)
        else:
            return answer  # fallback

    elif task == "Gene disease association" or task == "Disease gene location":
        return answer.replace("Answer:", "").strip().split(", ")

    elif task == "Protein-coding genes":
        val = answer.replace("Answer:", "").strip()
        return "TRUE" if val == "Yes" else "NA"

    elif task == "Multi-species DNA aligment":
        mapper = {
            "Caenorhabditis elegans": "worm",
            "Homo sapiens": "human",
            "Danio rerio": "zebrafish",
            "Mus musculus": "mouse",
            "Saccharomyces cerevisiae": "yeast",
            "Rattus norvegicus": "rat",
            "Gallus gallus": "chicken",
        }
        val = answer.replace("Answer:", "").strip()
        return mapper.get(val, val)

    else:
        return answer.replace("Answer:", "").strip()


# 5.2 Implement the answer mapping function
def get_score(predictions: List[str], gold_answers: List[str], task: str) -> float:
    """
    Compute average score for a given task based on model predictions and ground truths.
    """
    assert len(predictions) == len(
        gold_answers
    ), "Mismatched number of predictions and ground truths."

    correct = []

    for pred, gold in zip(predictions, gold_answers):
        pred_processed = get_answer(pred, task)
        gold_processed = get_answer(gold, task)

        # Get the appropriate metric function for this task
        metric_fn = metric_task_map[task]
        score = metric_fn(pred_processed, gold_processed)
        correct.append(score)

    return sum(correct) / len(correct) if correct else 0.0


# 6.1 Set up data structures for results


@dataclass
class Result:
    id: int
    task: str
    question: str
    answer: str
    prediction: str
    score: Optional[float]
    success: bool


def save_results(results: List[Result], results_csv_filename: str) -> None:
    df = pd.DataFrame(results)
    # df = pd.DataFrame([asdict(r) for r in results])
    df.to_csv(results_csv_filename, index=False)


# 6.2 Loop over the dataset with a progress bar

# * Do not forget to add the results to our Result list, both successful and failed predictions
# * API calls will not always work, so make sure we capture the exceptions from failed calls
#    and add them to the Result list with a `status=False`


def evaluate_dataset(
    df: pd.DataFrame, model_fn: Callable[[str], str]
) -> (List[Result], dict, float):
    results: List[Result] = []
    task_scores = {}
    task_counts = {}

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        task = row["task"]
        question = row["question"]
        true_answer = row["answer"]

        try:
            # Call the model
            raw_pred = model_fn(question)

            # Post-process
            pred = get_answer(raw_pred, task)
            true = get_answer(true_answer, task)
            # print("="*60)
            # print(f"[{task}]")
            # print(f"Question: {question}")
            # print(f" True Answer: {true}")
            # print(f" Model Raw Output: {raw_pred}")
            # print(f"Processed Prediction: {pred}")
            # Score it
            metric_fn = metric_task_map[task]
            score = metric_fn(pred, true)
            success = True
            # print(f"[{task}] True: {true}, Pred: {pred}, Score: {score}")
        except Exception as e:
            raw_pred = f"[ERROR] {e}"
            score = 0.0
            success = False

        results.append(
            Result(
                id=idx,
                task=task,
                question=question,
                answer=true_answer,
                prediction=raw_pred,
                score=score,
                success=success,
            )
        )

        if success:
            task_scores[task] = task_scores.get(task, 0.0) + score
            task_counts[task] = task_counts.get(task, 0) + 1

    # Compute average score per task
    for task in task_scores:
        task_scores[task] /= task_counts[task]

    # Compute overall average score
    overall_score = sum(task_scores.values()) / len(task_scores) if task_scores else 0.0

    return results, task_scores, overall_score


# 6.3 Save the results


# Dummy model for testing
def model_fn(question: str) -> str:
    return query_model(client, system_message, [], question)


# subset_df = df.head(20)  # First 20 rows only
with mlflow.start_run(run_name="gene_turing_run"):
    # Log basic config
    mlflow.log_param("deployment_name", AZURE_OPENAI_DEPLOYMENT_NAME)
    mlflow.log_param("model", "Azure GPT-4.1")
    mlflow.log_param("num_questions", len(df))

    # Run evaluation
    results, task_scores, overall = evaluate_dataset(df, model_fn)
    save_results(results, "gene_turing_results.csv")

    # Log overall score
    mlflow.log_metric("overall_score", overall)

    # Log fraction of successful predictions
    results_df = pd.DataFrame(results)
    fraction_successful = results_df["success"].mean()
    mlflow.log_metric("fraction_successful", fraction_successful)

    # Log score per task
    for task, score in task_scores.items():
        mlflow.log_metric(f"score_{task}", score)

    # Log output CSV file
    mlflow.log_artifact("gene_turing_results.csv")

print(f"Overall Score: {overall:.3f}")


# 7.1 Calculate the fraction of successful predictions
results_df = pd.DataFrame(results)
fraction_successful = results_df["score"].mean()
print(f"Fraction of successful predictions: {fraction_successful:.2%}")


# 7.2 Calculate the overall score and the score by task
print(f" Overall score: {overall:.3f}")
print(" Scores by task:")
for task, score in task_scores.items():
    print(f"  - {task}: {score:.3f}")

# 7.3 Create a bar chart of the scores by task with a horizontal line for the overall score
import matplotlib.pyplot as plt

# Sort tasks by name
sorted_tasks = sorted(task_scores.keys())
scores = [task_scores[task] for task in sorted_tasks]

plt.figure(figsize=(10, 5))
plt.bar(sorted_tasks, scores)
plt.axhline(
    y=overall, color="red", linestyle="--", label=f"Overall Score = {overall:.2f}"
)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Score")
plt.title("Scores by Task")
plt.legend()
plt.tight_layout()
chart_filename = "scores_by_task.png"
plt.savefig(chart_filename)  # Save BEFORE plt.show()
plt.show()
plt.close()

# Log it as an artifact
mlflow.log_artifact(chart_filename)
