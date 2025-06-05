#!/usr/bin/env python
# coding: utf-8

import json
import os
import random
from typing import Dict, List, Optional

import mlflow
import pandas as pd
import torch
import torch.nn.functional as F
from dotenv import load_dotenv
from openai import AzureOpenAI
from pydantic import BaseModel, Field
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

# === Load ENV and Configs ===
load_dotenv()
os.environ["no_proxy"] = "*"

AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

data_config = {
    "dataset_path": "./data/genehop.json",
    "output_path": "/project/GCRB/Hon_lab/s440914/MODULE_3_MATERIALS/outputs/",
    "dataset_name": "genehop_noncbi",
}

model_config = {
    "api": "OpenAI",
    "model_name": AZURE_OPENAI_DEPLOYMENT_NAME,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
    "temperature": 1.0,
    "max_tokens": 800,
    "top_p": 1.0,
}


# === Schema & Prompts ===
class GeneHopAnswer(BaseModel):
    task: str
    question: str
    answer: str
    explanation: Optional[str] = None


system_message = (
    "You are a genomics assistant that returns structured answers. "
    "You will be provided with a gene-related question and should return your answer "
    "in structured JSON format following a schema including task, "
    "question, answer, and explanation."
)


# === Load Dataset ===
def load_geneturing(path: str) -> List[Dict[str, str]]:
    with open(path, "r") as f:
        raw_data = json.load(f)

    flat_data = []
    for i, (task_name, qa_pairs) in enumerate(raw_data.items()):
        for question, answer in qa_pairs.items():
            flat_data.append(
                {
                    "id": i,
                    "task": task_name,
                    "question": question,
                    "answer": answer,
                }
            )
    return flat_data


# === LLM Query ===
def query_model(system_message: str, query: dict, api: str) -> dict:
    messages = [
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": (
                f'Here is a question: "{query["question"]}".\n'
                f"Return the answer in valid JSON format matching this schema:\n"
                '{"task": str, "question": str, "answer": str, "explanation": Optional[str]}.\n'
                f'The "task" should be "{query["task"]}".'
            ),
        },
    ]
    if api == "OpenAI":
        client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            timeout=10,
            max_retries=3,
        )
        response = client.beta.chat.completions.parse(
            model=model_config["model_name"],
            messages=messages,
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"],
            response_format=GeneHopAnswer,
        )
        return response.model_dump()


# === Structured Output Collection ===
def collect_structured_output(dataset: List[Dict], system_message: str) -> List[Dict]:
    results = []
    with mlflow.start_run(run_name="geneturing-eval"):
        for param, val in model_config.items():
            mlflow.log_param(param, val)

        for item in tqdm(dataset, desc="Evaluating"):
            try:
                ans = query_model(
                    system_message,
                    {"task": item["task"], "question": item["question"]},
                    model_config["api"],
                )
                ans.update({"success": True, "id": item["id"]})
            except Exception:
                ans = {
                    "id": item["id"],
                    "task": item["task"],
                    "question": item["question"],
                    "answer": "",
                    "explanation": "",
                    "success": False,
                }
            results.append(ans)

        # Save results
        result_json_path = os.path.join(
            data_config["output_path"],
            f"{data_config['dataset_name']}_{model_config['api']}_rawresults.json",
        )
        with open(result_json_path, "w") as f:
            json.dump(results, f, indent=2)
        mlflow.log_artifact(result_json_path)
        mlflow.log_metric("success_rate", pd.DataFrame(results)["success"].mean())

    return results


# === Cosine Similarity Scoring ===
def mean_pooling(output, mask):
    emb = output[0]
    mask = mask.unsqueeze(-1).expand(emb.size()).float()
    return torch.sum(emb * mask, 1) / torch.clamp(mask.sum(1), min=1e-9)


def compute_cosine_similarity(pred_data: List[Dict], gold_data: Dict) -> pd.DataFrame:
    tokenizer = AutoTokenizer.from_pretrained("FremyCompany/BioLORD-2023")
    model = AutoModel.from_pretrained("FremyCompany/BioLORD-2023")
    model.eval()

    gold_flat = []
    for task, qa in gold_data.items():
        for q, a in qa.items():
            gold_flat.append({"task": task, "question": q.strip(), "gold": a})

    results = []
    for i, pred in enumerate(pred_data):
        pred_ans = pred["answer"].strip()
        gold_ans = gold_flat[i]["gold"]
        if isinstance(gold_ans, list):
            gold_ans = " ".join(gold_ans)

        inp = tokenizer([pred_ans, gold_ans], padding=True, return_tensors="pt")
        with torch.no_grad():
            emb = mean_pooling(model(**inp), inp["attention_mask"])
            emb = F.normalize(emb, p=2, dim=1)
            sim = F.cosine_similarity(emb[0], emb[1], dim=0).item()

        results.append(
            {
                "task": gold_flat[i]["task"],
                "question": gold_flat[i]["question"],
                "predicted_answer": pred_ans,
                "gold_answer": gold_ans,
                "cosine_similarity": sim,
            }
        )

    df = pd.DataFrame(results)
    print("Average cosine similarity:", df["cosine_similarity"].mean())
    df.to_csv(
        os.path.join(
            data_config["output_path"],
            f"{data_config['dataset_name']}_{model_config['api']}_cosine_results.csv",
        ),
        index=False,
    )
    return df


# === Run ===
if __name__ == "__main__":
    dataset = load_geneturing(data_config["dataset_path"])
    print(f"Loaded {len(dataset)} examples.")
    structured_outputs = collect_structured_output(dataset, system_message)

    with open(data_config["dataset_path"], "r") as f:
        gold = json.load(f)

    compute_cosine_similarity(structured_outputs, gold)
