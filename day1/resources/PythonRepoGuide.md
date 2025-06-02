# BME Software Engineering: Python Code Repo Guidelines 🐍

This document provides a set of guidelines for creating and maintaining clean, organized, and understandable Python code repositories for bioinformatics projects. Following these practices will make your code more accessible to collaborators (and your future self!).

- [BME Software Engineering: Python Code Repo Guidelines 🐍](#bme-software-engineering-python-code-repo-guidelines-)
  - [Making Your README Shine with Markdown ✨](#making-your-readme-shine-with-markdown-)
  - [Structure Your Repository 📂](#structure-your-repository-)
  - [Naming Stuff Wisely ✍️](#naming-stuff-wisely-️)
  - [Keep Secrets and Data Out with `.gitignore` 🤫](#keep-secrets-and-data-out-with-gitignore-)
  - [Using pydantic secret string for API keys](#using-pydantic-secret-string-for-api-keys)
  - [Using Git Gracefully 🙏](#using-git-gracefully-)
  - [Setting Up Virtual Environments 🧱](#setting-up-virtual-environments-)
  - [Using `requirements.txt` for Dependencies 📦](#using-requirementstxt-for-dependencies-)
  - [Type Hints and Docstrings for Clarity 📜](#type-hints-and-docstrings-for-clarity-)
  - [Pydantic for Complex Data Structures 🏗️](#pydantic-for-complex-data-structures-️)
  - [De-nest your code 🐣](#de-nest-your-code-)
  - [Using a context manager](#using-a-context-manager)
  - [Using a try except block](#using-a-try-except-block)

## Making Your README Shine with Markdown ✨

A well-crafted README is the front door to your project. Markdown offers several features to make it visually appealing and informative.

- Headings: Use # for titles, ## for major sections, and ### for sub-sections.
- Emphasis: Use *italic* or _italic_ and **bold** or __bold__.
- Lists: Create ordered (1.) or unordered (* or -) lists.
- Links: [Link Text](URL)
- Images: ![Alt Text](Image_URL)
- Code Blocks: Use triple backticks (```) to enclose code snippets. Specify the language for syntax highlighting (e.g., ```python).
- Table of Contents: You can use a nice VS Code plug in like **yzhang.markdown-all-in-one** to make table of contents
- Linter: You can use a nice linter to help catch places where style formatting is broken, **DavidAnson.vscode-markdownlint**

## Structure Your Repository 📂

```plaintext
my_bio_project/
├── data/
│   ├── raw/                 # Original, immutable data
│   └── processed/           # Cleaned and transformed data
├── notebooks/               # Jupyter notebooks for exploration
├── scripts/                 # Reusable scripts for data processing, analysis, etc.
├── src/                     # Source code for your project (modules, packages)
│   └── my_project/
│       ├── init.py
│       └── data_processing.py
├── tests/                   # Unit and integration tests
├── .gitignore               # Files and folders to ignore
├── README.md                # Project overview
├── .env                     # Store your secrets (like API keys) Here!
├── pyproject.toml           # Configuration for python (if using it)
└── requirements.txt         # Project dependencies
```

Some nice guidelines:

- It ends up being easier to have a bunch of python files that contain smaller amounts of code than a handful of enormous python files!
- If you have a lot of docs, you can make an extra /docs folder to put them in so that way the main READEME does not get overwhelming! You can also put READMEs in sub folders!
- If you have a pipeline that takes in a large number of variable inputs, you can save those inputs in a `yaml` file or `json` so you can go back to them later.

## Naming Stuff Wisely ✍️

Use descriptive and consistent names. If anything **avoid using spaces and special characters**

* **Files:** Use lowercase with underscores (`snake_case.py`). Be specific (e.g., `calculate_gene_expression.py`). Or if they are just text/md files you can be a little more lax. 
* **Folders:** Use lowercase with underscores or hyphens (`data_processing` or `data-processing`).
* **Functions:** Use lowercase with underscores (`snake_case_function`). Be descriptive (e.g., `calculate_average_expression`).
* **Classes:** Use CamelCase (e.g., `GeneExpressionCalculator`).
* **Variables:** Use lowercase with underscores (`snake_case_variable`). Be descriptive (e.g., `gene_expression_data`).
* **Constants & Enviroment Vars:** Use uppercase with underscores (`OPENAI_API_KEY`).

## Keep Secrets and Data Out with `.gitignore` 🤫

Your `.gitignore` file tells Git which files and directories to ignore. This is crucial for keeping sensitive information (like API keys) and large data files out of your repository.
Can use regex matching to help keep out all files that match a specific pattern.

**IMPORTANT**: Do not put your API keys or other sensitive info in your python code or in your code repo!

```gitignore
# Secrets
*.env
credentials.json

# Data
data/raw/
data/processed/

# Archives
*.zip
*.tar.gz

# Python virtual environment
venv/
*.pyc
__pycache__/
```

## Using pydantic secret string for API keys

This is a handy way to store an API key so it wont get printed to code output or console.

```python
from pydantic import BaseModel, SecretStr

class User(BaseModel):
    username: str
    password: SecretStr

# here you would use os to get the string from your env NOT hard code it lol
user = User(username='scolvin', password='password1')

print(user)
#> username='scolvin' password=SecretStr('**********')
print(user.password.get_secret_value())
#> password1
print((SecretStr('password'), SecretStr('')))
#> (SecretStr('**********'), SecretStr(''))
```

## Using Git Gracefully 🙏

Git is your version control powerhouse. Use it effectively:

- Commit Often, Push Often: Make small, logical commits with clear messages.
- Write Meaningful Commit Messages: Use the imperative mood (e.g., Add feature to parse FASTA files).
- Use Branches: Create branches for new features or bug fixes (git checkout -b feature/new-analysis).
- Pull Before You Push: Update your local repository before pushing changes (git pull origin main).

## Setting Up Virtual Environments 🧱

Use virtual environments to manage dependencies. This keeps your project isolated and avoids conflicts with other projects.

```bash
# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```


## Using `requirements.txt` for Dependencies 📦

List your project dependencies in a `requirements.txt` file. This allows others to easily set up the same environment.

```plaintext
# requirements.txt
numpy==1.21.0
pandas==1.3.0
scikit-learn==0.24.2
matplotlib==3.4.2
```

## Type Hints and Docstrings for Clarity 📜

Type hints improve code readability and help catch errors. They also assist IDEs in providing better code completion, and helping remember what stuff does. This become **extremely** helpfull when you start getting into larger code bases, or are developing on code other people wrote. 

```python
def align_sequences(seq1: str, seq2: str) -> tuple[str, str]:
    """Aligns two DNA sequences."""
    # ...
    return aligned_seq1, aligned_seq2
```

Docstrings explain what your functions and classes do. Use a standard format like Google or NumPy style. Not all functions need them, but they are very useful for complex functions.

```python
def calculate_tm(sequence: str) -> float:
    """Calculates the melting temperature (Tm) of a DNA sequence.

    Args:
        sequence: The DNA sequence as a string.

    Returns:
        The estimated melting temperature in Celsius.
    """
    # ...
    return tm
```

Also, comments are nice but should be used to explain why something is done, not what is done. The code should be self-explanatory for the most part. Use comments to clarify complex logic or decisions.

So not like this:

```python
# Calculates the mean of a list of numbers
def calculate_mean(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)
```

But like this:

```python
# download in a separate thread to avoid freezing gui
for index in self.items:
    threading.Thread(
        target=self._download_thread, args=(index,), daemon=True
    ).start()
```

You can also leave comments with keywords like TODO, BUG, FIXME to indicate areas that need attention or improvement.

```python
# FIXME: This is getting the date so should be renamed, and it should combine date + room for the folder name
learner = row.locator("td:nth-child(3)").inner_text().strip()
```

## Pydantic for Complex Data Structures 🏗️

Pydantic provides data validation and settings management using Python type hints. It's excellent for defining and validating complex data structures often encountered in bioinformatics.

```python
from pydantic import BaseModel
from typing import List

class Gene(BaseModel):
    id: str
    sequence: str
    annotations: List[str]

gene_data = {"id": "GENE001", "sequence": "ATGCGT", "annotations": ["promoter", "exon"]}
my_gene = Gene(**gene_data)
print(my_gene.id)
```

## De-nest your code 🐣

This is hard to read:

```python

def print_data_list(id:int, data: list[tuple[str,int]], max_print: int = 10)->None:
    """For each item name and int pair in data, prints the item name int number of times, with max print as the upper limit
    For example, if the item is "A" and the int is 3, it prints "A" 3 times.
    The id must be an int, and the data must be a list of tuples with the first value an str and the second an int > 0
    """

    if type(id) == int:
        for pair in data:
            if type(pair[0]) == str:
                if pair[1] > 0:
                    for i in range(pair[1]):
                        if i >= max_print:
                            print(f"Maxed out at {max_print}")
                            break
                        print(pair[0])
                else:
                    print("Int must be >1")
            else:
                print("The first item in the tuple must be an str")
    else:
        print("Invalid ID, must be an integer")
    
```

This is much easier to read & understand the flow of the code:

```python
def print_data_list(id: int, data: list[tuple[str, int]], max_print:int=10) -> None:

    # guard clause that exits early if the id is invalid
    if type(id) != int:
        print("Invalid ID: must be an integer")
        return

    for item in data:
        if type(item[0]) != str:
            print("The first item in the tuple must be an str")
            # the continue statement skips the rest of the loop and goes to the next iteration
            continue

        if pair[1] <=0:
            print("Int must be >1")
            continue

        for i in range(min(pair[1], max_print)):
            print(pair[0])
        
        if pair[1] > max_print:
            print(f"Maxed out at {max_print}")
```

Try to aim for only 3 tab indents, if it is seeming like that is not possible, you might need to break the single function down into multiple smaller functions.

## Using a context manager

When you are opening external connections to a database, file, or mlflow server etc, it is good to put it after a `with` statement so that the connection closes gracefully when the code ends or errors out.

```python
import mlflow

with mlflow.start_run(run_name="hello-world") as run:
    # 3 - Log a couple of dummy parameters
    mlflow.log_param("greeting", "hello_mlflow")
    mlflow.log_param("year", 2025)
```

## Using a try except block

When you are doing something that might fail, like opening a file or connecting to a database, it is good to put it in a try except block so that you can handle the error gracefully and not crash the program.

```python

from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError, Field
import random
import time

# 1) Define the shape you expect from the LLM:
class User(BaseModel):
    username: str = Field(..., description="The unique username")
    password: str = Field(..., min_length=8, description="A secure password, at least 8 characters")

# 2) A stub that 'calls' your LLM and sometimes omits or mal‐formats fields:
def call_model_api(user_input: str, validation_errors: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Simulates an LLM response. On the first call it randomly omits or corrupts
    one of the fields; if validation_errors is provided, it “fixes” those.
    """
    # Base 'good' response
    good = {
        "username": "alice_in_wonderland",
        "password": "s3cur3P@ssw0rd"
    }

    # If retrying, pretend the model read the errors and fixes them:
    if validation_errors:
        print("Retrying with feedback:", validation_errors)
        time.sleep(1)  # simulate latency
        return good

    # First‐pass: randomly drop or corrupt a field
    bad = good.copy()
    if random.choice([True, False]):
        bad.pop("password", None)            # missing password
    else:
        bad["password"] = "short"            # too short
    print("First pass model output:", bad)
    return bad

def get_validated_user(user_input: str, max_retries: int = 2) -> User:
    """
    Attempts to parse the LLM output into a User. On ValidationError,
    it retries up to max_retries, passing the errors back to the model.
    """
    attempt = 0
    validation_errors = None

    while attempt <= max_retries:
        try:
            raw = call_model_api(user_input, validation_errors)
            user = User(**raw)           # may raise ValidationError
            print(f"✅ Success on attempt #{attempt + 1}")
            return user

        except ValidationError as e:
            attempt += 1
            validation_errors = e.errors()
            print(f"⚠️ Validation failed on attempt #{attempt}:")
            for err in validation_errors:
                loc = ".".join(str(x) for x in err["loc"])
                print(f"  - field `{loc}`: {err['msg']} (type={err['type']})")

            if attempt > max_retries:
                print("❌ Max retries exceeded. Unable to validate.")
                raise

        except Exception as e:
            # Catch-all for other errors (network, JSON decode, etc.)
            print(f"🚨 Unexpected error: {e!r}")
            raise

if __name__ == "__main__":
    user_input = "Please generate a JSON with username and password."
    try:
        user = get_validated_user(user_input)
        print("Final validated user object:", user.json())
    except ValidationError:
        print("Failed to produce valid user data after retries.")
    except Exception as e:
        print("A non-validation error occurred:", e)

```
