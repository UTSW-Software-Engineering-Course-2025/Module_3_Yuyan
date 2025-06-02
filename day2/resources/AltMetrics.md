# Alt metrics to exact match

## Lev distance

```bash
pip install python-Levenshtein
```

```python
import Levenshtein

s1 = "POC1B-GALNT4"
s2 = "GALNT4"

s1 = "B3GNT8"
s2 = "MMP2"

s1 = "GALNT5"
s2 = "GALNT4"

s1 = "SRC"
s2 = "MM"


# compute the Levenshtein distance
dist = Levenshtein.distance(s1, s2)

print(f"Levenshtein distance between {s1!r} and {s2!r} is {dist}")
```

## Cosine similarity

**Note:** If you are on biohpc set your hf home to a place you can store large files

```bash
exoprt HF_HOME=some/path

# or put this in your .bashrc
```

```python
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F


# https://huggingface.co/FremyCompany/BioLORD-2023
# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[
        0
    ]  # First element of model_output contains all token embeddings
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


# This is for the gene hop "SNP gene function"
# Sentences we want sentence embeddings for

sentences = [
    "This is not a protein coding gene. it is located on the 6th chromosome.",
    "Located on the 6th chromosome, this gene is protein coding",
    "This is a protein coding gene. it is located on the 6th chromosome.",
]

# Load model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained("FremyCompany/BioLORD-2023")
model = AutoModel.from_pretrained("FremyCompany/BioLORD-2023")
encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")

# Compute token embeddings
with torch.no_grad():
    model_output = model(**encoded_input)
# Perform pooling
sentence_embeddings = mean_pooling(model_output, encoded_input["attention_mask"])
# Normalize embeddings
sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

cosine_sim = F.cosine_similarity(sentence_embeddings[0], sentence_embeddings[1], dim=0)
# fix the dimension out of range error
print(cosine_sim)
cosine_sim = F.cosine_similarity(sentence_embeddings[0], sentence_embeddings[2], dim=0)
print(cosine_sim)

cosine_sim = F.cosine_similarity(sentence_embeddings[1], sentence_embeddings[2], dim=0)
print(cosine_sim)

```

## Using the embedding API

The url is `http://198.215.61.34:8152/embed`

```python
import requests
import json

# Define the URL endpoint
url = "http://198.215.61.34:8152/embed"

# Define the data payload as a Python dictionary
data = {
    "sentences": [
        "This is the first sentence.",
        "Here is another one."
    ]
}

# Define the headers (though `requests` often handles this when using `json=`)
headers = {
    "Content-Type": "application/json"
}

try:
    # Make the POST request
    # Using the `json` parameter automatically sets the Content-Type header
    # and handles JSON encoding.
    response = requests.post(url, json=data)

    # You could also send it this way, explicitly setting headers and encoding:
    # response = requests.post(url, headers=headers, data=json.dumps(data))

    # Raise an exception for bad status codes (4xx or 5xx)
    response.raise_for_status()

    # Print the response status code
    print(f"Status Code: {response.status_code}")

    # Print the response content (assuming it's JSON)
    print("Response JSON:")
    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
```