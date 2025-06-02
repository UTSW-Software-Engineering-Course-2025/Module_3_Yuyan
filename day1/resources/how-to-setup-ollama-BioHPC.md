---
title: "Setup Ollama on BioHPC"
date: "May 2025"
author: "S228627"
geometry: margin=1in
fontsize: 11pt
---

# What is Ollama?

Ollama is a lightweight, open-source model server for running Large Language Models (LLMs) locally. 
This short guide will show you how to serve and use the Qwen3:4b parameter model on BioHPC using `ollama`.

## Pre-requisites
- You are on a suitable BioHPC node (you will need to install `ollama` first if you trying this on your personal computer)
- **Do not do this on your login node!**


## Step 1: Load Ollama module

```bash
# Latest version of Ollama available on BioHPC
module avail ollama
module load ollama/0.7.0-img
```

## Step 2: Create a directory to download model weights


```bash
mkdir -p /work/bioinformatics/[your-student-id]/ollama/models
export OLLAMA_MODELS=/work/bioinformatics/[your-student-id]/ollama/models
```

**Notes:** 
1. This location is where the model weights will be downloaded.
2. Add the export to your `~/.bashrc` or `~/.zshrc` to persist across sessions.
3. Remember to clean up the directory when you are done.


## Step 3: Start a `screen` session

```bash
# If you are not familiar with screen - you can safely ignore this
screen -S ollama
```

## Step 3: Start the Ollama server and download a model

Make sure you are using the (right!) GPU
```bash
export CUDA_VISIBLE_DEVICES=0
```

The server uses port `11434` by default, so make sure nothing else is using this port.
You can also change the port (refer to the cheatsheet). 
```bash
# Start server in background
ollama serve &

# Download and run qwen3:4b model
ollama run qwen3:4b
```

### Health check

Verify your server is working with a simple health check:

```bash
# Use http://localhost:11434/api/generate if on same node as the server

# If you are calling from a different node, use the IP address of the node where the server is running.

# Get your node's IP address
hostname -I

# Quick inference test
curl http://[your-ip-address]:11434/api/generate -d '{
  "model": "qwen3:4b",
  "prompt": "Say hello from the course instructors!"
}'
```

You should see something like this:

```
{"model":"qwen3:4b","created_at":"2025-05-23T21:54:35.341911257Z","response":"Hello","done":false}
{"model":"qwen3:4b","created_at":"2025-05-23T21:54:35.359988798Z","response":" from","done":false}
{"model":"qwen3:4b","created_at":"2025-05-23T21:54:35.3798263Z","response":" the","done":false}
{"model":"qwen3:4b","created_at":"2025-05-23T21:54:35.398020979Z","response":" home","done":false}
..... (and so on)
```

## API Usage

### Method 1: Use Python Ollama library
Full docs: [ollama-python](https://github.com/ollama/ollama-python)

```python
from ollama import Client
client = Client(
  host='http://localhost:11434',
)
response = client.chat(model='qwen3:4b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
```

### Method 2: OpenAI-compatible API
Full docs: [Ollama OpenAI-compatible API](https://github.com/ollama/ollama/blob/main/docs/openai.md)

**This is the main approach we will use in the course!**

The Ollama server provides an OpenAI-compatible API which is somewhat of an industry standard for interacting with LLMs. 

This is especially useful if you are using an existing workflow that utilizes OpenAI API, or to seamlessly swap out the model to OpenAI models. 
Refer to [OpenAI API documentation](https://platform.openai.com/docs/quickstart?api-mode=chat&lang=python) for more details.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://[your-ip-address]:11434/v1",
    api_key="ollama"  # Required but not used
)

response = client.chat.completions.create(
    model="qwen3:4b",
    messages=[{"role": "user", "content": "Describe the mechanism of PCR"}]
)

print(response.choices[0].message.content)
```

## Step 4: Stop the Ollama server

Once done, you can stop the server with:

```bash
pkill -f "ollama serve"
```