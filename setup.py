# -*- coding: utf-8 -*-
#
import codecs
import os

from setuptools import setup, find_packages

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "matplotlib2tikz", "__about__.py"), "rb") as f:
    exec(f.read(), about)


def read(fname):
    return codecs.open(os.path.join(base_dir, fname), encoding="utf-8").read()


setup(
    name="matplotlib2tikz",
    version=about["__version__"],
    packages=find_packages(),
    url="https://github.com/nschloe/matplotlib2tikz",
    author=about["__author__"],
    author_email=about["__email__"],
    install_requires=["matplotlib >= 1.4.0", "numpy", "Pillow", "six"],
    extras_require={
        "all": ["pipdate >= 0.3.0, <0.4.0"],
        "update": ["pipdate >= 0.3.0, <0.4.0"],
    },
    description="Convert matplotlib figures into TikZ/PGFPlots",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license=about["__license__"],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
