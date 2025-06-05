import argparse
import os
import time

import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def llm_judge(question, answer, prediction):
    prompt = f"""
You are an expert evaluator. Given the following:

Question: {question}
Expected Answer: {answer}
Model's Prediction: {prediction}

Determine if the prediction correctly answers the question. Respond with 'Yes' or 'No' followed by a brief explanation.
"""

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error"


def main():
    parser = argparse.ArgumentParser(
        description="LLM-as-a-Judge evaluation for CSV results."
    )
    parser.add_argument(
        "--input_csv", required=True, help="Path to input result CSV file"
    )
    parser.add_argument(
        "--output_csv",
        default="judge_output.csv",
        help="Path to output judged CSV file",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    judgments = []
    for idx, row in df.iterrows():
        print(f"Judging example {idx}...")
        judgment = llm_judge(row["question"], row["answer"], row["prediction"])
        judgments.append(judgment)
        time.sleep(1)  # Be polite

    df["llm_judgment"] = judgments
    df.to_csv(args.output_csv, index=False)
    print(f"✅ Judged results saved to {args.output_csv}")


if __name__ == "__main__":
    main()
