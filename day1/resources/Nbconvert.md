# Tutorial: Using nbconvert to Convert Jupyter Notebooks and Skip Tagged Cells

Jupyter notebooks are a popular way to develop and share code, documentation, and results in a single interactive document. Sometimes, you may want to convert your `.ipynb` notebook to a different format (such as a Python script or HTML) while skipping certain cells. For example, you might want to skip cells containing experimental code, long outputs, or sensitive information. This tutorial will guide you through using `nbconvert` to convert a notebook and skip all cells with a specific tag, such as `skip`.

## What is nbconvert?

[`nbconvert`](https://nbconvert.readthedocs.io/en/latest/) is a command-line tool and Python library that allows you to convert Jupyter notebooks to various formats, including Python scripts, HTML, PDF, and more. It is highly customizable, supporting preprocessors and exporters to control how notebooks are converted.

## Why Use Cell Tags?

Cell tags are a feature in Jupyter notebooks that let you add metadata to individual cells. Tags can be used by tools like `nbconvert` to identify and process cells in specific ways. For example, you can tag cells with `skip` to indicate that they should be omitted from the output during conversion.

## Step-by-Step Guide

### 1. Install nbconvert

If you don't already have `nbconvert`, install it via pip:

```bash
pip install nbconvert
```

### 2. Add the "skip" Tag to Cells

Open your notebook in JupyterLab or Jupyter Notebook. To tag a cell:

1. Click on the cell you want to tag.
2. In the menu, select `View > Cell Toolbar > Tags` (in classic Jupyter Notebook) or open the "Tags" sidebar in JupyterLab.
3. Add the tag `skip` (or any tag you prefer) to the cell.

You can add multiple tags to a cell, but for this tutorial, we will use `skip`.

### 3. Convert the Notebook and Skip Tagged Cells

To skip cells with the `skip` tag during conversion, use the `TagRemovePreprocessor` provided by `nbconvert`. This preprocessor can remove cells with specific tags from the output.

#### Example: Convert to Python Script (Recommended: Suppress Cell Markers)

To also suppress cell markers like `# In[6]:`, add the `--no-prompt` flag:

```bash
jupyter nbconvert \
  --to script your_notebook.ipynb \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags='["skip"]' \
  --no-prompt
```

This will remove both the cells tagged with `skip` and the cell input prompts from the exported script.
#### Example: Convert to HTML

```bash
jupyter nbconvert \
  --to html your_notebook.ipynb \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags='["skip"]'
```

### Note on Notebook Execution

By default, nbconvert does NOT execute the notebook when converting to HTML (or other formats). It simply exports the notebook as-is, using the outputs already present in the file.

If you want nbconvert to run all cells and update outputs before exporting, use the `--execute` flag:

```bash
jupyter nbconvert --to html your_notebook.ipynb --execute
```

- Without `--execute`: nbconvert uses existing outputs in the notebook.
- With `--execute`: nbconvert runs all cells in order, updates outputs, and then exports.

#### Explanation of the Command
- `--to script` or `--to html`: Output format.
- `--TagRemovePreprocessor.enabled=True`: Enables the tag removal preprocessor.
- `--TagRemovePreprocessor.remove_cell_tags='["skip"]'`: Specifies which tags to remove. Cells with the `skip` tag will be omitted from the output.

### 4. Advanced: Using a Configuration File

You can also create a configuration file (e.g., `nbconvert_config.py`) to avoid typing long commands:

```python
# nbconvert_config.py
c = get_config()
c.TagRemovePreprocessor.enabled = True
c.TagRemovePreprocessor.remove_cell_tags = ["skip"]
```

Then run:

```bash
jupyter nbconvert --to script your_notebook.ipynb --config nbconvert_config.py
```

### 5. Verifying the Output

After conversion, open the generated script or HTML file. You should see that all cells tagged with `skip` are omitted from the output.

## Summary

- Use cell tags in Jupyter to mark cells you want to skip.
- Use `nbconvert` with the `TagRemovePreprocessor` to skip those cells during conversion.
- This workflow helps you create clean, shareable outputs without manual cell removal.

For more details, see the [nbconvert documentation](https://nbconvert.readthedocs.io/en/latest/removing-cells.html).
