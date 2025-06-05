import argparse

from nbformat import NotebookNode, read


def export_code_only(ipynb_path: str, output_path: str) -> None:
    with open(ipynb_path, "r", encoding="utf-8") as f:
        nb: NotebookNode = read(f, as_version=4)

    with open(output_path, "w", encoding="utf-8") as f:
        for cell in nb.cells:
            if cell.cell_type == "code":
                f.write(cell.source + "\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebook to .py file, ignoring markdown cells."
    )
    parser.add_argument(
        "-ipynb", type=str, required=True, help="Path to input .ipynb file"
    )
    parser.add_argument("-py", type=str, required=True, help="Path to output .py file")
    args = parser.parse_args()

    export_code_only(args.ipynb, args.py)
