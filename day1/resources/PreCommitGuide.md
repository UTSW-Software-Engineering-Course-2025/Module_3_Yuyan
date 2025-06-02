# Pre Commit Hooks

In this guide we'll be exploring how to use pre-commit hooks to auto format and type check code!

## Step 1: Install tools if not already installed

```bash
pip install pre-commit black mypy flake8 isort
```

## Step 2: Edit the the pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.isort]
profile = "black"                   # makes isort + Black play nicely
line_length = 88

[tool.flake8]
max-line-length = 88                # stay consistent
extend-ignore = ["E203", "W503"]    # also matches Black's opinions
per-file-ignores = [
  "__init__.py:F401",               # silence 'unused import' in package inits
]

[tool.mypy]
python_version = "3.11"
strict = true                       # OR choose some flags
plugins = [
  "pydantic.mypy",                  # example: extra plugin support
]
ignore_missing_imports = true       # keep CI green while you iterate
```

## Step 3: Create a hooks config

Save as `.pre-commit-config.yaml`

```yaml
repos:
  # 1:  Sort imports first (so Black formats the result)
  - repo: https://github.com/pycqa/isort
    rev: 6.0.1
    hooks:
      - id: isort
        # run only on staged Python files
        files: \.py$
        # tell isort to respect your pyproject settings
        additional_dependencies: []

  # 2: Format
  - repo: https://github.com/psf/black
    rev:  24.4.2        # pin!  (check latest tag)
    hooks:
      - id: black
        language_version: python3.11    # match your runtime

  # 3:  Lint for style / simple bugs
  - repo: https://github.com/pycqa/flake8
    rev: 7.2.0
    hooks:
      - id: flake8

  # 4: Static type checks (runs last; formatting doesn't affect it)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        # rely on pyproject for flags; add requirements if needed
        additional_dependencies: [] # e.g. ["pydantic"] if plugins need runtime deps
        # Optional args; leave blank if using pyproject.toml
        # args: ["--strict"]

```

## Step 4: Enable the hooks with git

```bash
pre-commit install
pre-comit run --all-files
```

## Now the flow after this

```bash
git add .
git commit -m "blah blah"
# Now it will run and tell you all the errors, you can fix them
```

Now you have to fix the errors and **re-add your changes**

```bash
git add .
git commit -m "blah blah"
```
