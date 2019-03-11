# -*- coding: utf-8 -*-
#
import os
import importlib.util

import matplotlib2tikz as m2t
import matplotlib.pyplot as plt


def _main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(this_dir):
        if filename.startswith("test_") and filename.endswith(".py"):
            spec = importlib.util.spec_from_file_location("plot", filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.plot()

            code = m2t.get_tikz_code(include_disclaimer=False)
            plt.close()

            tex_filename = filename[:-3] + "_reference.tex"
            with open(os.path.join(this_dir, tex_filename), "w") as f:
                f.write(code)
    return


if __name__ == "__main__":
    _main()
