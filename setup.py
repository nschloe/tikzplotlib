# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import codecs
import pandoc

from matplotlib2tikz import __version__


def convert_to_rst(md_file):
    print('md_file', md_file)
    pandoc.core.PANDOC_PATH = '/usr/bin/pandoc'
    doc = pandoc.Document()
    doc.markdown = open(md_file, 'r').read()
    return doc.rst

print(__file__)
print(os.path.realpath(__file__))
print(os.path.dirname(os.path.realpath(__file__)))


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
    long_description=convert_to_rst(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
        ),
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion'
        ]
    )
