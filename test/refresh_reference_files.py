import argparse
import importlib.util
import os

import matplotlib.pyplot as plt

import tikzplotlib as tpl


def _main():
    parser = argparse.ArgumentParser(description="Refresh the reference TeX files.")
    parser.add_argument("files", nargs="+", help="Files to refresh")
    args = parser.parse_args()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_list = ["test_rotated_labels.py", "test_deterministic_output.py"]

    for filename in args.files:
        if filename in exclude_list:
            continue
        if filename.startswith("test_") and filename.endswith(".py"):
            spec = importlib.util.spec_from_file_location("plot", filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.plot()

            code = tpl.get_tikz_code(include_disclaimer=False)
            plt.close()

            tex_filename = filename[:-3] + "_reference.tex"
            with open(os.path.join(this_dir, tex_filename), "w") as f:
                f.write(code)
    return


if __name__ == "__main__":
    _main()
