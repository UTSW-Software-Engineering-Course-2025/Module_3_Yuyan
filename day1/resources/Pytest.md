# Pytest for Data Science: A Practical Guide

## Introduction

[pytest](https://docs.pytest.org/) is a powerful and user-friendly testing framework for Python. It is widely used in both software engineering and data science for its simplicity, flexibility, and rich plugin ecosystem. For data science projects, where code correctness and reproducibility are crucial, using pytest can help ensure that data pipelines, feature engineering, and model evaluation work as expected.

## Why Use Pytest?
- **Simple syntax:** Write tests as regular Python functions.
- **Auto-discovery:** pytest automatically finds files and functions prefixed with `test_`.
- **Rich assertions:** No need for self.assert* methods; use plain `assert` statements.
- **Fixtures:** Easily set up and tear down test data or environments.
- **Plugins:** Extend functionality (e.g., coverage, parallel runs).

## Installing Pytest
Install pytest with pip:
```bash
pip install pytest
```

## What to Unit Test in Data Science Code?
Not every line of data science code needs a test, but consider tests for:
- **Data cleaning functions:** e.g., functions that fill missing values or filter rows.
- **Feature engineering:** Custom transformations, encoders, or aggregations.
- **Utility functions:** Anything that parses, formats, or validates data.
- **Model evaluation:** Metrics calculations, thresholding, or post-processing.
- **Pipeline steps:** Each major step in a pipeline (e.g., data loading, preprocessing, prediction).

> **Tip:** Avoid testing code that just calls external libraries unless you add logic on top.

## Example: Testing a Data Cleaning Function
Suppose you have a function that fills missing values:
```python
def fill_missing(df, value=0):
    return df.fillna(value)
```
A simple test:
```python
def test_fill_missing():
    import pandas as pd
    df = pd.DataFrame({'a': [1, None, 3]})
    result = fill_missing(df, value=-1)
    assert result.isnull().sum().sum() == 0
    assert (result['a'] == pd.Series([1, -1, 3])).all()
```
Save this in a file named `test_utils.py` (or similar). Run pytest from the command line:
```bash
pytest
```

## Persisting Pytest Results to Disk
To save test results, use the `--junitxml` option, which writes results in XML (compatible with CI tools):
```bash
pytest --junitxml=pytest_results.xml
```
You can also output results in a more human-readable format using plugins like `pytest-html`:
```bash
pip install pytest-html
pytest --html=pytest_report.html
```

## Organizing Your Tests and Autodiscovery
For larger projects, it is a best practice to organize your tests in a dedicated `tests/` directory at the root of your repository. Place your test files inside this folder (e.g., `tests/test_utils.py`). Pytest will automatically discover all files named `test_*.py` or `*_test.py` and execute functions prefixed with `test_`. If your tests need to import code from your main project, make sure your project root is on the `PYTHONPATH`, or use relative imports. You can run pytest from the project root to ensure imports resolve correctly. If you encounter import errors, try running:
```bash
PYTHONPATH=. pytest
```
This ensures that pytest can find your source code modules during test execution.

## Tips for Data Science Testing
- **Use fixtures** to set up sample dataframes or test files:
  ```python
  import pytest
  import pandas as pd

  @pytest.fixture
def sample_df():
      return pd.DataFrame({'a': [1, 2, None]})
  ```
- **Parametrize tests** to check multiple scenarios:
  ```python
  @pytest.mark.parametrize("val,expected", [(0, 0), (1, 1)])
  def test_identity(val, expected):
      assert val == expected
  ```
- **Test edge cases:** Empty data, nulls, out-of-range values.
- **Automate tests:** Use pre-commit hooks or CI to run tests before merging code.

## Summary
pytest makes it easy to write, run, and persist tests for your data science code. Focus on testing custom logic and data transformations. Persist results to disk for reproducibility and reporting. For more, see the [pytest documentation](https://docs.pytest.org/).
