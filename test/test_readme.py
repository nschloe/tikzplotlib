import pathlib

import pytest

import exdown

this_dir = pathlib.Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "string",
    exdown.extract(
        this_dir.parent / "README.md", syntax_filter="python", skip=[1, 2, 3]
    ),
)
def test_readme(string):
    exec(string)
