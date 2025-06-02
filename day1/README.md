# Day 1: Ollama + GeneTuring

## 0. Setup

1. Clone this repository
2. Install dependencies
3. Start Ollama server
4. Download GeneTuring dataset
5. Start `starter_geneturing.ipynb`

## 1. Task

1. Implement the missing code in the GeneTuring harness notebook
2. Run the notebook and collect results
3. Convert the notebook to a script, implement unit tests, and document the sections and logic
4. Add MLFlow logging to script and log results
5. Use precommit to format code and run mypy before logging Day 1 code

## 2.Rubric

**Possible Points: 25**

| Task | Objective | Possible Points | 
| --- | --- | --- |
| 1 | Implement the GeneTuring harness notebook | 5 |
| 2 | Run the notebook and collect results | 5 |
| 3 | Convert the notebook to a script, implement unit tests, and document the sections and logic | 5 |
| 4 | Add MLFlow logging to script and log results | 5 |
| 5 | Use precommit to format code and run mypy | 5 |

### 2.1 Task 1

**Objective:** Implement the GeneTuring harness notebook

**Possible Points: 5**

| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | Attempt more than 25% of sections                                                   |
| 2      | Attempt more than 50% of sections  |
| 3      | Attempt more than 75% of sections  |
| 4      | Attempt all sections            |
| 5      | Successfully run all sections |

### 2.2 Task 2

**Objective:** Run the notebook and collect results

**Recommendation:** On implemented, run `nbconvert` with `execute` to run the notebook and collect results and save the output to an HTML file. Commit the HTML file to the repository.

**Possible Points: 5**

| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | More than 50% of the run results collected                                 |
| 2      | More than 75% of the run results collected                                 |
| 3      | More than 90% of the run results collected                                 |
| 4      | All of the run results collected                                         |
| 5      | All of the run results collected, more than 5% exact match                 |

### 2.3 Task 3

**Objective:** Convert the notebook to a script, implement unit tests, and document the sections and logic

**Possible Points: 5**

| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | Successfully converted the notebook to a script                                                   |
| 2      | + implemented at least one unit test for the script  |
| 3      | + implemented at least three unit tests for the script  |
| 4      | + added minimal documentation for the sections and logic  |
| 5      | + added comprehensive documentation for the sections and logic  |


### 2.4 Task 4

**Objective:** Add MLFlow logging to script and log results

**Possible Points: 5**

| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 1      | Attempted to add MLFlow logging to script of overall score   |
| 2      | + per-task scores to local MLFlow run |
| 3      | + Added bar chart of per-task score artifact to local MLFlow run |
| 4      | + logged predictions CSV artifact to local MLFlow run  |
| 5      | All of the above with remote MLFlow logging |

### 2.5 Task 5

**Objective:** Use precommit to format code and run mypy before logging Day 1 code

**Possible Points: 5**

| Points | Criteria |
|--------|--------------------------------------------------------------------------|
| 3      | Used at least two tools to format code and run mypy before logging Day 1 code   |
| 4      | Used 3 or more tools to format code before logging Day 1 code |
| 5      | + mypy before logging Day 1 code |


## 3. Resources

### 3.1 ExternalResources

* [GeneTuring](https://github.com/ncbi/GeneGPT)
* [MLFlow](https://mlflow.org/)
* [precommit](https://pre-commit.com/)  
* [Black](https://black.readthedocs.io/en/stable/)
* [isort](https://pycqa.github.io/isort/)
* [mypy](https://mypy.readthedocs.io/en/stable/)
* [flake8](https://flake8.pycqa.org/en/stable/)
* [pytest](https://docs.pytest.org/en/stable/)
* [Ollama](https://ollama.com/)
* [Qwen 3](https://qwenlm.github.io/blog/qwen3/)
* [nbconvert](https://nbconvert.readthedocs.io/en/latest/)

### 3.2 Internal Resources

* [Starter notebook](day1/gene_turing.ipynb) - A starter notebook that implements the GeneTuring harness
* [Download Geneturing](download_geneturing.sh) - A script that downloads the Geneturing dataset into `data/geneturing.json`
* [Python Repo General Guidlines](./resources/PythonRepoGuide.md) - Guide to general Python repo and coding tips
* [Ollama server setup guide]()
* [MLFlow logging guide](/day1/resources/MLFlowTracking.md) - Guide to tracking experiments with MLFlow
* [NBConvert guide](resources/Nbconvert.md)
* [precommit guide](day1/resources/PreCommitGuide.md) - Guide to setting up pre commit hooks for auto formatting and linting
* [Pytest guide](resources/Pytest.md)
* [Handy VS Code Plugins](day1/resources/HandyPlugins.md) - Some super handy plug ins for VS Code