# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import codecs

from matplotlib2tikz import __version__


def read(fname):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname),
        encoding='utf-8'
        ).read()

setup(
    name='matplotlib2tikz',
    version=__version__,
    py_modules=['matplotlib2tikz'],
    url='https://github.com/nschloe/matplotlib2tikz',
    download_url='https://github.com/nschloe/matplotlib2tikz/downloads',
    author='Nico Schlömer',
    author_email='nico.schloemer@gmail.com',
    requires=['matplotlib (>=1.4.0)', 'numpy'],
    description='convert matplotlib figures into TikZ/PGFPlots',
    long_description=read('README.md'),
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion'
        ]
    )
