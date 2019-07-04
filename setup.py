import codecs
import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "tikzplotlib", "__about__.py"), "rb") as f:
    exec(f.read(), about)


def read(fname):
    return codecs.open(os.path.join(base_dir, fname), encoding="utf-8").read()


setup(
    name="tikzplotlib",
    version=about["__version__"],
    packages=find_packages(),
    url="https://github.com/nschloe/tikzplotlib",
    author=about["__author__"],
    author_email=about["__email__"],
    install_requires=["matplotlib >= 1.4.0", "numpy", "Pillow"],
    description="Convert matplotlib figures into TikZ/PGFPlots",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license=about["__license__"],
    python_requires=">=3",
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
