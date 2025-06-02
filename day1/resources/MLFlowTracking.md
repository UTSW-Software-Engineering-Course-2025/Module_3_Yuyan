# MLFlow logging Basics

## Getting started

This logs it to your local folder.

**IMPORTANT** Put your `start_run` in a `with` statement so it always closes it out when the code finishes!

```python
import mlflow

with mlflow.start_run(run_name="hello-world") as run:
    # 3 - Log a couple of dummy parameters
    mlflow.log_param("greeting", "hello_mlflow")
    mlflow.log_param("year", 2025)
```

You can view the results by running a local server via the command line

```bash
# might have to change the port!
mlflow ui
```

## Setting experiment and run names

A **run** is a trial within an **experiment**

```python
import mlflow

mlflow.set_experiment("Howdy")

with mlflow.start_run(run_name="hello-world") as run:
    # 3 - Log a couple of dummy parameters
    mlflow.log_param("greeting", "hello_mlflow")
    mlflow.log_param("year", 2025)
```

You can also use tags to help filter runs (See API cheat sheet below)

## Connecting to a remote server

This is running remotly and uses a database backend so it is a lot more scalable, and you can log into the UI from anywhere on the VPN

```python
import mlflow

mlflow.set_tracking_uri("http://198.215.61.34:8153")
mlflow.set_experiment("Howdy")

with mlflow.start_run(run_name="hello-world") as run:
    # 3 - Log a couple of dummy parameters
    mlflow.log_param("greeting", "hello_mlflow")
    mlflow.log_param("year", 2025)
```

Vist the server in your browser by navigating to [http://198.215.61.34:8153](http://198.215.61.34:8153)

## MLFlow API Cheat Sheet

| **Call**                                            | **When to use it**                                                    |
| --------------------------------------------------- | --------------------------------------------------------------------- |
| `mlflow.log_param(key, value)`                      | Hyper-parameters, config flags, dataset ID                            |
| `mlflow.log_metric(key, value, step=None)`          | Scalar metrics (loss, accuracy). Use `step` for epochs                |
| `mlflow.log_artifact(path, artifact_path=None)`     | Files (plots, configs, checkpoints)                                   |
| `mlflow.log_dict(obj, ...) / log_text / log_figure` | Quick one-liners for small JSON, YAML, plain text, or matplotlib figs |
| `mlflow.set_tag(key, value)`                        | Metadata for filtering ('stage\:dev', 'team\:nlp')                    |
| `mlflow.autolog()`                                  | Turnkey logging for many popular libraries                            |
