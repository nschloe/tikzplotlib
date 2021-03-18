import pathlib

import exdown
import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

this_dir = pathlib.Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "string,lineno",
    exdown.extract(this_dir.parent / "README.md", syntax_filter="python"),
)
def test_readme(string, _):
    exec(string)

    # Close figure and reset defaults
    plt.close()
    mpl.rcParams.update(mpl.rcParamsDefault)
