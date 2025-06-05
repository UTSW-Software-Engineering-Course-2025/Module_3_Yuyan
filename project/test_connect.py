# script for testing connect with client
import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
print("KEY:", os.getenv("AZURE_OPENAI_KEY"))
print("ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("DEPLOYMENT:", os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"))
print("VERSION:", os.getenv("AZURE_OPENAI_API_VERSION"))

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    messages=[{"role": "user", "content": "Hi!"}],
    max_tokens=10,
)

print(response.choices[0].message.content)
