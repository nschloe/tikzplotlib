# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import codecs

from matplotlib2tikz import __version__, __license__, __author__, __email__


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content

setup(
    name='matplotlib2tikz',
    version=__version__,
    packages=['matplotlib2tikz'],
    url='https://github.com/nschloe/matplotlib2tikz',
    download_url='https://pypi.python.org/pypi/matplotlib2tikz',
    author=__author__,
    author_email=__email__,
    requires=['matplotlib (>=1.4.0)', 'numpy'],
    description='convert matplotlib figures into TikZ/PGFPlots',
    long_description=read('README.rst'),
    license=__license__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: Visualization'
        ]
    )
