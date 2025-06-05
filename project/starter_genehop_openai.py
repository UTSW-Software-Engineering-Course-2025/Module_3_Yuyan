# 1.1 Place imports here
import difflib
import json
import os
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from Bio import Entrez
from Bio.Blast import NCBIWWW, NCBIXML
from dotenv import load_dotenv
from gene_hop_no_ncbi import compute_cosine_similarity
from ncbi_info import dispatch_ncbi_data, format_ncbi_data
from openai import AzureOpenAI
from sklearn.metrics import f1_score
from tqdm import tqdm

# 2.1 Data Configuration


# 2.2 Model Configuration

# 2.3 Evaluation and Logging Configuration
os.environ["no_proxy"] = "*"
mlflow.set_tracking_uri("http://198.215.61.34:8153")
mlflow.set_experiment("s440914_1")

load_dotenv()
Entrez.email = os.getenv("Entrez.email")  # Replace with your email
Entrez.api_key = os.getenv("Entrez.api_key")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")


MODEL_CONFIG = {
    "max_tokens": 800,
    "temperature": 1.0,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "model": AZURE_OPENAI_DEPLOYMENT_NAME,  # Loaded from env
}

# 3.1 Load the JSON file
with open("../data/genehop.json", "r") as f:
    data = json.load(f)


# Build the TASKS variable here
TASKS = set(data)
print(TASKS)

# 3.2 Iterate through the JSON data recursively to collect each of the rows into a list
#     Each row should have a dictionary with keys of the columsn in the table above
rows = []

# Recursively iterate through each task and its Q&A pairs
for task, qas in data.items():
    for question, answer in qas.items():
        rows.append({"task": task, "question": question, "answer": answer})

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
        "If multiple genes are associated, list all their names and chromosome locations. Separate by comma."
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


# 4.4 Implement THE model function
def model_fn(question: str, task: str) -> str:
    """
    Main function to get the model prediction based on task and question.
    """
    # Get NCBI info (raw dict format)
    ncbi_data = dispatch_ncbi_data(task, question)
    return query_model(
        client=client,
        system_message=system_message,
        few_shot_examples=few_shot_examples,
        user_query=question,
        ncbi_data=ncbi_data,
    )


def query_model(
    client,
    system_message: List[Dict[str, Any]],
    few_shot_examples: List[Dict[str, str]],
    user_query: str,
    ncbi_data: Optional[Dict] = None,
) -> str:
    """
    Query the language model with NCBI data prepended and few-shot examples.
    """
    # Format NCBI data if present and attach to query
    if ncbi_data:
        ncbi_text = format_ncbi_data(ncbi_data)
        user_query = f"NCBI Data: {ncbi_text}\nQuestion: {user_query}"

    # Compose the message payload
    messages = (
        system_message + few_shot_examples + [{"role": "user", "content": user_query}]
    )

    # Call the model
    response = client.chat.completions.create(messages=messages, **MODEL_CONFIG)

    # Extract and clean answer
    content = response.choices[0].message.content
    response_content = content.strip() if content else ""

    # Try to parse "Answer: ..." from model output
    match = re.search(r"(?i)answer\s*:\s*(.*)", response_content)
    return match.group(1).strip() if match else response_content


# 5.1 Implement metrics


def token_overlap(pred: str, true: str) -> float:
    pred_tokens = set(pred.lower().split())
    true_tokens = set(true.lower().split())
    return len(pred_tokens & true_tokens) / len(true_tokens) if true_tokens else 1.0


def normalized_levenshtein(pred: str, true: str) -> float:
    return difflib.SequenceMatcher(
        None, pred.strip().lower(), true.strip().lower()
    ).ratio()


def f1_score_set(pred: Union[str, List[str]], true: Union[str, List[str]]) -> float:
    if isinstance(pred, str):
        pred = re.split(r"[,;]", pred)
    if isinstance(true, str):
        true = re.split(r"[,;]", true)

    pred_set = set(map(str.strip, pred))
    true_set = set(map(str.strip, true))

    if not pred_set and not true_set:
        return 1.0
    if not pred_set or not true_set:
        return 0.0

    tp = len(pred_set & true_set)
    precision = tp / len(pred_set)
    recall = tp / len(true_set)
    return (
        2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    )


import re
from typing import List


def extract_chrom_loci(text: str) -> List[str]:
    """
    Extract all chromosome loci strings like '17q21.31' or '6p12' from a text.
    """
    return re.findall(r"\d{1,2}[pq]\d+(\.\d+)?", text)


def fuzzy_location_score(pred: str | List[str], true: List[str]) -> float:
    """
    Scoring function for 'Disease gene location'. Gives credit for correct loci,
    penalizes extra irrelevant loci.

    Args:
        pred (str | List[str]): predicted string or list of loci
        true (List[str]): gold standard loci

    Returns:
        float: score in [0, 1]
    """
    if isinstance(pred, str):
        pred_loci = extract_chrom_loci(pred)
    else:
        pred_loci = pred

    pred_loci = set(pred_loci)
    true_loci = set(true)

    true_positives = len(pred_loci & true_loci)
    false_positives = len(pred_loci - true_loci)

    if len(true_loci) == 0:
        return 1.0 if len(pred_loci) == 0 else 0.0

    precision = true_positives / (true_positives + false_positives + 1e-8)
    recall = true_positives / len(true_loci)

    # F1 score with soft penalty for hallucination
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


# Define metrics per task
metric_task_map: Dict[
    str, Callable[[Union[str, List[str]], Union[str, List[str]]], float]
] = defaultdict(
    lambda: token_overlap,  # use token overlap as default
    {
        "sequence gene alias": f1_score_set,
        "Disease gene location": fuzzy_location_score,
        "SNP gene function": compute_cosine_similarity,
    },
)


def preprocess_answer(answer: str) -> str:
    if isinstance(answer, list):
        answer = ", ".join(answer)
    elif not isinstance(answer, str):
        answer = str(answer)
    answer = answer.strip()
    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()
    return answer


def get_answer(answer: str, task: str) -> List[str]:
    answer = preprocess_answer(answer)

    if task == "sequence gene alias":
        try:
            answer_list = ast.literal_eval(answer)
            return answer_list if isinstance(answer_list, list) else [answer]
        except Exception:
            return [answer]

    elif task == "Disease gene location":
        matches = re.findall(r"\d{1,2}[pq]\d+(?:\.\d+)?", answer)
        return matches or [answer]

    elif task == "SNP gene function":
        match = re.findall(r"(chr)?[0-9XY]+[pq]?\d*(\.\d+)?", answer)
        keys = ["".join([x for x in m if x]).strip() for m in match]
        mapped = [snp_function_map.get(k, k) for k in keys]
        return [answer]


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

# * Do not forget to add the results to our Result list,
#  both successful and failed predictions
# * API calls will not always work,
# so make sure we capture the exceptions from failed calls
#    and add them to the Result list with a `status=False`


def evaluate_dataset(
    df: pd.DataFrame, model_fn: Callable[[str], str]
) -> Tuple[List[Result], Dict[str, float], float]:
    results: List[Result] = []
    task_scores: Dict[str, float] = {}
    task_counts: Dict[str, int] = {}

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        task = row["task"]
        question = row["question"]
        true_answer = row["answer"]

        try:
            # Call the model
            raw_pred = model_fn(question, task)

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
            metric_fn: Callable[[str, str], float] = metric_task_map[task]
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


# subset_df = df.head(20)  # First 20 rows only
with mlflow.start_run(run_name="gene_hop_run"):
    # Log basic config
    mlflow.log_param("deployment_name", AZURE_OPENAI_DEPLOYMENT_NAME)
    mlflow.log_param("model", "Azure GPT-4.1")
    mlflow.log_param("num_questions", len(df))

    # Run evaluation
    subset_df = (
        df.groupby("task", group_keys=False)
        .apply(lambda x: x.head(5))
        .reset_index(drop=True)
    )
    results, task_scores, overall = evaluate_dataset(subset_df, model_fn)
    save_results(results, "gene_hop_openai_results.csv")

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
    mlflow.log_artifact("gene_hop_openai_results.csv")

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
plt.title("Scores by Task")
plt.legend()
plt.tight_layout()
chart_filename = "scores_by_task_gene_hop.png"
plt.savefig(chart_filename)  # Save BEFORE plt.show()
plt.show()
plt.close()

# Log it as an artifact
mlflow.log_artifact(chart_filename)
