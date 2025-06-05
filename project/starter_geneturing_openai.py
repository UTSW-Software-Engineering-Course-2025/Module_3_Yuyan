# 1.1 Place imports here
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
from tqdm import tqdm

# 2.1 Data Configuration
os.environ["no_proxy"] = "*"
mlflow.set_tracking_uri("http://198.215.61.34:8153")
mlflow.set_experiment("s440914_1")

# 2.2 Model Configuration

# 2.3 Evaluation and Logging Configuration
load_dotenv()
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
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
        "content": "Hello. "
        "Your task is to use NCBI Web APIs to answer genomic questions."
        "Please only answer the question concisely "
        " don't generate to many other stuff."
        " If you can specify the answer, please put it after word Answer. "
        "If you are not sure about the answer, please try to be concise"
        " and give a brief guess based on the NCBI results.",
    }
]
few_shot_examples = [
    {
        "role": "user",
        "content": "What is the official gene symbol of LMP10?",
    },
    {
        "role": "assistant",
        "content": "The official gene symbol of LMP10 is PSMB10.",
    },
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
    system_message: List[Dict[str, Any]],
    few_shot_examples: List[Dict[str, str]],
    user_query: str,
) -> str:
    """
    Query the language model with few-shot examples and a user query.
    Returns the extracted answer string.
    """
    # print("sys",type(system_message))
    # print("eg",type(few_shot_examples))
    # print("user:",type ([{"role": "user", "content": user_query}]))
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
    content = response.choices[0].message.content
    response_content = content.strip() if content is not None else ""

    # Try to extract the part after "Answer:" if present
    if "Answer:" in response_content:
        answer = response_content.split("Answer:")[-1].strip()
    else:
        answer = response_content  # fallback

    return answer


# 5.1 Implement metrics


def exact_match(pred, true):
    pred_str = str(pred).strip().lower()
    true_str = str(true).strip().lower()
    return pred_str == true_str


def gene_disease_association(pred: list[str], true: list[str]) -> float:
    pred_set = set(map(str.lower, map(str.strip, pred)))
    true_set = set(map(str.lower, map(str.strip, true)))
    if not true_set:
        return 1.0 if not pred_set else 0.0
    return len(pred_set & true_set) / len(true_set)


def disease_gene_location(pred: list[str], true: list[str]) -> float:
    pred_set = set(map(str.lower, map(str.strip, pred)))
    true_set = set(map(str.lower, map(str.strip, true)))
    if not true_set:
        return 1.0 if not pred_set else 0.0
    return len(pred_set & true_set) / len(true_set)


def human_genome_dna_alignment(pred: str, true: str) -> float:
    pred = pred.strip().lower()
    true = true.strip().lower()
    if pred == true:
        return 1.0
    pred_chr = pred.split(":")[0]
    true_chr = true.split(":")[0]
    return 0.5 if pred_chr == true_chr else 0.0


metric_task_map = defaultdict(
    lambda: exact_match,
    {
        "gene_disease_association": gene_disease_association,
        "disease_gene_location": disease_gene_location,
        "human_genome_dna_alignment": human_genome_dna_alignment,
    },
)


def get_answer(answer: str, task: str) -> List[str]:
    answer = answer.strip()

    if task in ["Gene alias", "Gene location", "SNP location"]:
        # Extract last word that looks like a gene symbol (alphanumeric, all caps)
        match: List[str] = re.findall(r"[A-Z0-9\-]+", answer)
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
def get_score_and_success(
    predictions: List[str], gold_answers: List[str], task: str
) -> Tuple[float, List[bool]]:
    """
    Compute average score and success flags for a given task.
    """
    assert len(predictions) == len(
        gold_answers
    ), "Mismatched number of predictions and ground truths."

    scores = []
    successes = []

    for pred, gold in zip(predictions, gold_answers):
        pred_processed = get_answer(pred, task)
        gold_processed = get_answer(gold, task)

        metric_fn = metric_task_map[task]
        score = metric_fn(pred_processed, gold_processed)

        scores.append(score)
        successes.append(score == 1.0)  # or use `>= 0.9` if soft match

    avg_score = sum(scores) / len(scores) if scores else 0.0
    return avg_score, successes


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

# * Do not forget to add the results to our Result list,
#  both successful and failed predictions
# * API calls will not always work,
# so make sure we capture the exceptions from failed calls
#    and add them to the Result list with a `status=False`


def evaluate_dataset(
    df: pd.DataFrame, model_fn: Callable[[str], str]
) -> Tuple[List[Result], Dict[str, float], float]:

    results: List[Result] = []
    task_predictions: Dict[str, List[str]] = {}
    task_answers: Dict[str, List[str]] = {}
    task_questions: Dict[str, List[str]] = {}
    task_indices: Dict[str, List[int]] = {}

    raw_preds: List[str] = []

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        task = row["task"]
        question = row["question"]
        true_answer = row["answer"]

        try:
            raw_pred = model_fn(question)
        except Exception as e:
            raw_pred = f"[ERROR] {e}"

        raw_preds.append(raw_pred)

        # Save data for batch scoring
        task_predictions.setdefault(task, []).append(raw_pred)
        task_answers.setdefault(task, []).append(true_answer)
        task_questions.setdefault(task, []).append(question)
        task_indices.setdefault(task, []).append(idx)

    # Now compute scores and successes per task
    id_to_result: Dict[int, Result] = {}

    for task in task_predictions:
        preds = task_predictions[task]
        golds = task_answers[task]
        questions = task_questions[task]
        indices = task_indices[task]

        avg_score, success_flags = get_score_and_success(preds, golds, task)

        # Regenerate processed predictions and fill in result
        for i, (idx, pred_raw, question, gold, success) in enumerate(
            zip(indices, preds, questions, golds, success_flags)
        ):
            id_to_result[idx] = Result(
                id=idx,
                task=task,
                question=question,
                answer=gold,
                prediction=pred_raw,
                score=1.0 if success else 0.0,
                success=success,
            )

    # Build full result list
    results = [id_to_result[i] for i in range(len(df))]

    # Calculate task-level average scores
    task_scores: Dict[str, float] = {}
    for task in task_predictions:
        avg_score, _ = get_score_and_success(
            task_predictions[task], task_answers[task], task
        )
        task_scores[task] = avg_score

    # Overall score
    overall_score = sum(task_scores.values()) / len(task_scores) if task_scores else 0.0

    return results, task_scores, overall_score


# 6.3 Save the results


# Dummy model for testing
def model_fn(question: str) -> str:
    return query_model(client, system_message, few_shot_examples, question)


# subset_df = df.head(20)  # First 20 rows only
with mlflow.start_run(run_name="gene_turing_run"):
    # Log basic config
    mlflow.log_param("deployment_name", AZURE_OPENAI_DEPLOYMENT_NAME)
    mlflow.log_param("model", "Azure GPT-4.1")
    mlflow.log_param("num_questions", len(df))

    # Run evaluation
    results, task_scores, overall = evaluate_dataset(df, model_fn)
    save_results(results, "gene_turing_openai_results.csv")

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

# 7.3 Create a bar chart of the scores
# by task with a horizontal line for the overall score


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
plt.title("Geneturing Scores by Task")
plt.legend()
plt.tight_layout()
chart_filename = "scores_by_task.png"
plt.savefig(chart_filename)  # Save BEFORE plt.show()
plt.show()
plt.close()

# Log it as an artifact
mlflow.log_artifact(chart_filename)
