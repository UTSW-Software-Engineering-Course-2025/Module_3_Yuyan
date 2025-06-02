# Day 2: Structured Data

## Background

### Why Structured Output?

* Unstructured text (like clinical notes, reports) is hard for computers to analyze directly.
* Structured data (like tables, JSON) is easily processed, queried, and used in databases or analysis pipelines.
* **Goal:** Increase consistency, enable downstream analysis, improve data usability.

### Target Formats

* **JSON (JavaScript Object Notation):** Very common for web applications and APIs. Key-value pairs.
  
    ```json
    {
        "patient_id": "PID123",
        "visit_date": "2025-04-23",
        "vitals": {
        "hr": 75,
        "bp": "120/80"
        },
        "diagnosis": ["Hypertension", "Type 2 Diabetes"]
    }
    ```

### Techniques for Consistent Extraction

1. **Explicit Instructions:** Clearly tell the LLM *what* to extract and *how* to format it.
2. **Provide Examples (Few-Shot):** Show the LLM exactly what the desired output looks like for a similar input text.
3. **Specify the Format:** Use phrases like "Extract the following information in JSON format:", "Output a markdown table with columns:", "Provide the output as CSV:".
4. **Define the Schema (Keys/Columns):** List the exact field names or column headers you want (e.g., "Extract 'patient_name', 'dob', 'chief_complaint' into a JSON object").
5. **Provide necessary context:** If you are needing to do any conversions or inference from nuanced text, provide the necessary context to the LLM. For example, "MiT translocation RCC" is now referred to as "TFEB altered RCC"

## Exercise 1: Structured Output Basics

* **Goal:** Understand how to prompt for structured output.

### 1.1 Getting a Basic Structured Output

* **Instructions:**
  
1. Open Google AI Studio.
2. Use the provided clinical note snippet and example prompt to generate structured output.

* **Example Report Text 1**

    ```markdown {.wrap}
    Prostatectomy preparation with infiltration of a moderately differentiated adenocarcinoma of the. prostate on both sides. 
    Maximum diameter of a single tumor focus: 2.1 cm. 
    No identifiable invasion of the vessels. 
    Tumor-free and regular seminal vesicles and seminal ducts. 
    Tumor in contact with (artefactual, yellow-labeled) preparation margin, other (genuine). 
    preparation margins tumor-free. 
    Tumor classification: pT2c pN0, L0, V0; 
    Gleason 3+3 = 6 (less than 5% Gleason 4 as tertiary. Gleason score).
    ```

* **Example Prompt 1.1**

    ```markdown {.wrap}
    Extract the the maximum tumor focus diameter in cm. 
    Format your response as a JSON with the key "maximum_diameter" and the value as a decimal number.
    Your full response should be entirely contained within the JSON. 
    Here is the report text: 
    {{Paste Text Here}}
    ```

### 1.2 Exploring different data types

* **Instructions:**
  
  1. Use the same clinical note snippet.
  2. Experiment with adding more data types to the prompt.

   **Example Prompt 1.2**

    ```markdown {.wrap}
    We need to extract and format data from a clinical report.
    The entities we are interested in are:
    *   Maximum diameter of a single tumor focus in cm, key "maximum_diameter" value as a decimal number
    *   Pathological T stage, key "pT_stage", value as a string
    *   Invasion of vessels, key "vessel_invasion", value as a boolean
    Format your response as a JSON with the appropriate keys and values.
    Your full response should be entirely contained within the JSON.
    Here is the report text: 
    {{Paste Text Here}}
    ```

### 1.3 Providing Your Own Schema

* **Instructions:**
    1. Use the same clinical note snippet.
    2. Experiment with adding a 'schema' to the prompt.
    3. See if the LLM followed the standardization to **Adenocarcinoma**

* **Example Prompt 1.3**

    ```markdown {.wrap}
    We need to extract and format data from a clinical report.
    The entities we are interested in are:
    *   Maximum diameter of a single tumor focus in cm, key "maximum_diameter" value as a decimal number
    *   Histology, key "histology", value as a string, standardized from the provided list below
        *   "Adenocarcinoma"
        *   "Squamous cell carcinoma"
        *   "Neuroendocrine carcinoma"
        *   "Benign tissue"
    For histology, ensure that the option you select is standardized **exactly** to the list above.
    Format your response as a JSON with the appropriate keys and values.
    Your full response should be entirely contained within the JSON.
    Here is the report text: 
    {{Paste Text Here}}
    ```

### 1.4 Providing Background Information

* **Instructions:**
    1. Use the same clinical note snippet.
    2. Experiment with adding background information to the prompt.
    3. See if the LLM utilizes the background information to improve the output.

* **Example Prompt 1.4**

    ```markdown {.wrap}
    We need to extract and format data from a clinical report.
    We are interested in inferring and extracting the pathological AJCC stage
    For these reports they are prostate adenocarcinoma reports and should be between stage I and II
    *   For this item, we want a JSON with the key "ajcc_stage", and the value as a string, taken from the following list:
        *   "I"
        *   "IIA"
        *   "IIB"
        *   "IIC"

    Instructions for inferring the AJCC stage:
    *   stage I
        *    cT1, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA less than 10
        *    cT2a, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA less than 10
        *    pT2, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA less than 10
    *  stage IIA
        *    cT1, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA at least 10 but less than 20
        *    cT2a or pT2, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA at least 10 but less than 20
        *    cT2b or cT2c, N0, M0Grade Group 1 (Gleason score 6 or less) PSA less than 20
    *   stage IIB
        *    T1 or T2, N0, M0 Grade Group 2 (Gleason score 3+4=7) PSA less than 20
    *   stage IIC
        *    T1 or T2, N0, M0 Grade Group 3 or 4 (Gleason score 4+3=7 or 8) PSA less than 20
    
    Ensure the option you select is standardized **exactly** to the list above.
    Format your response as a JSON with the appropriate key and value.
    Your full response should be entirely contained within the JSON.
    Here is the report text: 
    {{Paste Text Here}}
    ```

### 1.5 Asking for Structured Reasoning

* **Instructions:**
    1. Use the same clinical note snippet.
    2. Experiment with asking for structured reasoning in the prompt.
    3. See if the LLM provides a more detailed output.

* **Example Prompt 1.5**

    ```markdown {.wrap}
    # Goal
    We need to extract and format data from a clinical report.
    We are interested in inferring and extracting the pathological AJCC stage.
    Your full respose should be entirely contained within the a JSON.

    # Basic Information
    For these reports they are prostate adenocarcinoma reports and should be between stage I and II
    *   For this item, we want a JSON with the key "ajcc_stage", and the value as a string, taken from the following list:
        *   "I"
        *   "IIA"
        *   "IIB"
        *   "IIC"
    Ensure the option you select is standardized **exactly** to the list above.

    # Clinical Background
    Background for inferring the AJCC stage:
    *   stage I
        *    cT1, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA less than 10
        *    cT2a, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA less than 10
        *    pT2, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA less than 10
    *  stage IIA
        *    cT1, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA at least 10 but less than 20
        *    cT2a or pT2, N0, M0 Grade Group 1 (Gleason score 6 or less) PSA at least 10 but less than 20
        *    cT2b or cT2c, N0, M0Grade Group 1 (Gleason score 6 or less) PSA less than 20
    *   stage IIB
        *    T1 or T2, N0, M0 Grade Group 2 (Gleason score 3+4=7) PSA less than 20
    *   stage IIC
        *    T1 or T2, N0, M0 Grade Group 3 or 4 (Gleason score 4+3=7 or 8) PSA less than 20
    
    # Reasoning
    The first item of your response should be under the key "reasoning"
    The value should contain your reasoning for how the stage was determined.
     - In this section, include a detailed explanation of the staging, as if explaining to a medical student.
    
    # Formatting
    Format your response as a JSON with the appropriate key and value.
    The second part of your response should be under the key "ajcc_stage" and the value should be the AJCC stage.
    Ensure that the keys are in double quotes, and the values are in double quotes as well.
    Ensure that the JSON is valid and well-formed.
    Your full response should be entirely contained within the JSON.

    # Report Text
    Here is the report text: 
    {{Paste Text Here}}
    ```

## Exercise 2: Advanced Structured Output Considerations

* **Goal:** Explore advanced considerations for structured output generation.

* **Example Report Text 2**

    ```markdown {.wrap}
    A. Right kidney, radical nephrectomy:
    - Renal cell carcinoma, clear-cell type
    B. Left atrial mass:
    - Poorly differentiated carcinoma, suggestive of metastatic renal cell carcinoma
    ```

* **Example Base Prompt**

    ```markdown {.wrap}
    # Goal
    We need to extract and format data from kidney tumor pathology reports.
    The items we are interested in are histology and procedure.
    Your full response should be entirely contained within a JSON

    # Basic Information

    ## Histology

    The histology should be provided under the key "histology" and the value should be a string from the following list:

    *   "Clear cell renal cell carcinoma"
    *   "Papillary renal cell carcinoma"
    *   "Benign tissue, negative for malignancy"

    ## Procedure

    The procedure should be provided under the key "procedure" and the value should be a string from the following list:

    *   "Radical nephrectomy"
    *   "Partial nephrectomy"
    *   "Biopsy"

    # Reasoning
    The first item of your response should be under the key "reasoning"
    The value should contain your explanation for how you properly utilized the standardized terminology.
     - In this section, include a detailed explanation, as if explaining to a medical student.

    # Formatting
    Format your response as a JSON with the appropriate keys and values.
    The first part of your response should be under the key "reasoning"
    And the value should be your reasoning for how the histology and procedure were determined.
    The second part of your response should be under the key "histology" and the value should be the histology.
    The third part of your response should be under the key "procedure" and the value should be the procedure.
    Ensure that the keys are in double quotes, and the values are in double quotes as well.
    Ensure that the JSON is valid and well-formed.
    
    # Report Text
    Here is the report text: 
    {{Paste Text Here}}
    ```

### 2.1 Complex Data Types/Mulitple Labels

* **Question:**
    1. How would you modify a prompt to provide the histology, anatomical site, and procedure for both specimens?

### 2.2 Missing Data

* **Question:**
    1. How would you modify a prompt to handle the missing procedure for the second item?

### 2.3 Borderline Characteristics

* **Question:**
    1. How would you modify a prompt to account for the use of **suggestive**?

### 2.5 Specification & Granularity

* **Question:**
    1. Lets pretend we are also interested in extracting a basic anatomical site. So simply 'kidney' and 'heart'.
    2. How can we add an example of standardizing to this level of specification without providing the answer in the prompt?

## Exercise 3: Using Structured Output Generation

* **Goal:** Explore the use of the structured output tool in AI studio.

* **Example Text 3**

    ```markdown {.wrap}
    Patient John Doe (DOB 01/15/1965) presented to clinic on 2025-03-10 with complaint of persistent cough for 3 weeks. 
    Vitals: HR 88 bpm, BP 130/85.
     Current meds include Metformin 1000mg BID and Atorvastatin 20mg daily. 
     Plan: Chest X-ray ordered. Follow up in 1 week.
    ```

* **Example Prompt 3**

    ```markdown {.wrap}
    # Instructions
    Please extract the heart rate from this clinical text and provide it in a structured JSON schema response.

    # Report Text
    Patient John Doe (DOB 01/15/1965) presented to clinic on 2025-03-10 with complaint of persistent cough for 3 weeks. 
    Vitals: HR 88 bpm, BP 130/85.
     Current meds include Metformin 1000mg BID and Atorvastatin 20mg daily. 
     Plan: Chest X-ray ordered. Follow up in 1 week.
    ```

### 3.1 Using a JSON Schema

* **Instructions:**
    1. Open Google AI Studio.
    2. Use the provided clinical note snippet and example prompt.
    3. Go to the Setting and select the "Structured Output" option.
    4. Click **Edit** and paste the JSON schema below into the editor.
    5. Save and run the prompt with the report text.

* **Example JSON Schema 3.1**
* Basic JSON schema for heart rate extraction, uses a number type for heart rate.
* This schema is very basic and does not include units or reasoning.

```json
{
  "type": "object",
  "properties": {
    "heart_rate": {
      "type": "number",
      "description": "The heart rate extracted from the clinical report",
    }
  },
  "required": [
    "heart_rate"
  ]
}
```

### 3.2 Editing the JSON Schema

* **Example JSON Schema 3.2**
* This schema includes string matching options for heart rate so we can capture the units.
* However, this resulting data entry will need to be cleaned downstream if we want to do numerical analysis.

```json
{
  "type": "object",
  "properties": {
    "heart_rate": {
      "type": "string",
      "description": "The heart rate extracted from the clinical report, including numeric value and units (e.g., \"72 bpm\" or \"80 beats per minute\").",
      "pattern": "^[0-9]+\\s?(?:bpm|beats per minute|not identified|beats per second|bps)$"
    }
  },
  "required": [
    "heart_rate"
  ]
}
```

### 3.3 Optimizing the JSON Schema

* **Example JSON Schema 3.3**
* This schema includes a number type for heart rate and a string type for units.
* The units are now limited to a specific set of values with an enum, helping to standardize the output.

```json
{
  "type": "object",
  "properties": {
    "heart_rate_value": {
      "type": "number",
      "description": "The numeric value of the heart rate."
    },
    "heart_rate_units": {
      "type": "string",
      "description": "The units for the heart rate measurement.",
      "enum": [
        "bpm",
        "unit not identified",
        "bps"
      ]
    }
  },
  "required": [
    "heart_rate_value",
    "heart_rate_units"
  ]
}
```

### 3.4 Adding in a "reasoning" field

* **Example JSON Schema 3.4**
* This schema includes a reasoning field to explain how the heart rate was extracted.
* Note that the explanation field is listed first, we need it to be generated first to benefit from the LLM's reasoning.

```json
{
  "type": "object",
  "properties": {
    "explanation": {
      "type": "string",
      "description": "Where in the report the heart rate was found (e.g. 'from the vitals section, line 3')."
    },
    "heart_rate_value": {
      "type": "number",
      "description": "The numeric value of the heart rate."
    },
    "heart_rate_units": {
      "type": "string",
      "description": "The units for the heart rate measurement.",
      "enum": [
        "bpm",
        "unit not identified",
        "bps"
      ]
    }
  },
  "required": [
    "explanation",
    "heart_rate_value",
    "heart_rate_units"
  ]
}
```

**Tip:** JSON itself doesn't guarantee object key order (per RFC 8259), but in practice, most serializers—including the OpenAI function‐calling output—preserve the order you define in your schema. If you ever need strict ordering you could instead return an array of field‐objects, but for most LLM workflows this property‐ordering trick suffices.

### 3.3 Creating your own JSON Schema w/ Pydantic

We'll use pydantic to make this much easier!

```python
import os
from enum import Enum
from typing import Optional
import pprint as pp

from openai import AzureOpenAI
from pydantic import BaseModel, Field


class StandardDiagnosisOptions(str, Enum):
    COMMON_COLD = "COMMON_COLD"
    INFLUENZA = "INFLUENZA"
    OTHER = "OTHER"
    

class Diagnosis(BaseModel):
    """
    Represents a patient's diagnosis, allowing for selection from a
    standard list or a custom entry if not listed.
    """
    reasoning_summary: str = Field(
        ..., # Ellipsis indicates it's a required field with no default
        description="A summary of your reasoning for how you chose the correct diagnosis."
    )
    standard_diagnosis_code: StandardDiagnosisOptions = Field(
        ...,
        description=(
            "Select the diagnosis from the standard list. "
            "If the diagnosis is not in this list, select 'OTHER'."
        )
    )
    custom_diagnosis_description: Optional[str] = Field(
        default=None, # Makes it optional, will be None if not provided
        description=(
            "If 'OTHER' was selected for standard_diagnosis_code, "
            "provide the specific uncommon diagnosis here as free text. "
            "Otherwise, this field should be omitted or left null."
        )
    )

system_prompt = "You are a medical proffesional who helps create structured data, you will be provided with a clinical report and you will extract the diagnosis information in a structured format. You should follow the JSON schema provided and always provide the reasoning_summary field first."

report_text = """patient presents with fever, cough, and sore throat. 
The patient has a history of asthma and is currently taking albuterol. 
The physical examination reveals a red throat and swollen lymph nodes. 
A rapid test for influenza is positive. 
The patient is advised to rest, stay hydrated, and take over-the-counter medications for symptom relief. 
No antibiotics are prescribed as this is likely a viral infection."""

prompt = f"Here is the original report text: <report_text> {report_text} </report_text>. Consider the most appropriate diagnosis and return formated as a JSON object according to the schema provided. Your response should be a valid JSON object. The reasoning_summary should be the first field you provide."

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": prompt},
]

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
    timeout=10,
    max_retries=3,
)

# NOTE: Here we are using the parse function instead of the typical chat completion function.
response = client.beta.chat.completions.parse(
    model=os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
    messages=messages,
    temperature=0,
    max_tokens=4096,
    response_format=Diagnosis,
)

pp.pprint(response.model_dump())
```

### 3.4 Using vLLM or Ollama

To use structured output with vLLM or Ollama, you can define a Pydantic model and then use it to parse the response from the LLM. The difference is we have to dump the schema and then re validate it after the response is returned.

```python
from ollama import chat
from pydantic import BaseModel

# need to set up the connection to ollama too

response = chat(
  messages=messages,
  model='llama3.1',
  format=Diagnosis.model_json_schema(),
)

diagnosis = Diagnosis.model_validate_json(response.message.content)
pp.pprint(diagnosis.model_dump())
```
