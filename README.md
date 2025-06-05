# GeneTuring & GeneHop with OpenAI and NCBI API

This project demonstrates a pipeline that combines biomedical APIs and large language models (LLMs) to perform gene-related question answering, verification, and annotation assistance.

## 🔍 What This Project Does

We built two major tools:

### 🧠 1. GeneTuring (LLM-Based QA & Verification)
- **Input**: A dataset of biomedical question-answer pairs involving gene knowledge.
- **Function**: Uses OpenAI's LLM (`gpt-4`) to:
  - Predict gene-related answers
  - Check the correctness of given answers
  - Explain or rephrase answers in natural language
- **LLM Tasks**:
  - Zero-shot answer generation
  - Explanation generation
  - Binary classification (`success = True/False`)

### 🔄 2. GeneHop (NCBI + LLM Hybrid)
- **Input**: A gene name (may be outdated or alias)
- **Function**: 
  - Calls **NCBI Gene API** to find the current official gene symbol and related metadata
  - Uses OpenAI’s LLM to interpret and refine ambiguous results
  - Optionally compares predicted vs. gold answer for downstream QA evaluation
- **Features**:
  - NCBI Entrez API usage with fallback matching
  - LLM handles unrecognized or messy gene symbols
  - Outputs enriched information like gene description, aliases, and Entrez ID

---

## ✅ Highlights

- 🔁 **NCBI API Integration** for reliable biomedical knowledge
- 🤖 **OpenAI LLM** for natural language understanding and explanation
- 🧪 **Cosine similarity computation** using mean-pooled BERT-style embeddings for answer validation
- 🧹 Non-NCBI versions implemented 
- 🔧 Reproducible setup with `mlflow` and logging enabled for experiments

---

## Setup

### Requirements

- `openai`
- `transformers`
- `torch` or `numpy` + `sklearn` (for no-torch version)
- `pandas`, `tqdm`
- `mlflow` (optional, for experiment tracking)
```bash

git clone <this repo>
cd Module_3_materials
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```