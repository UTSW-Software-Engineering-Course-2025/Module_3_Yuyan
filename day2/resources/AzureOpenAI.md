# This is a quick reference for using Azure OpenAI with Python.

## Pre first step, add `*.env` file to your `.gitignore`

## First your .env file

```plaintext
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your_endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=your_api_version
```

## Install the required packages

```bash
pip install openai python-dotenv
```

## Example code to use Azure OpenAI

```python
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API client

# NOTE: HERE we dont ever save the API key as a variable so it never gets printed
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
api_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"), # Always use it just in time
    api_version=api_version,
    azure_endpoint=api_base,
    timeout=10,
    max_retries=3,
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Howdy"},
]

response = client.chat.completions.create(
    model=api_deployment,
    messages=messages
)

parsed_response = response.choices[0].message.content

print(parsed_response)
```