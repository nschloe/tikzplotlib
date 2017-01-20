# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'matplotlib2tikz', '__about__.py')) as f:
    exec(f.read(), about)


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
    version=about['__version__'],
    packages=['matplotlib2tikz'],
    url='https://github.com/nschloe/matplotlib2tikz',
    download_url='https://pypi.python.org/pypi/matplotlib2tikz',
    author=about['__author__'],
    author_email=about['__email__'],
    install_requires=[
        'matplotlib >=1.4.0',
        'numpy',
        'Pillow >= 3.0.0'
        ],
    test_require=[
        'ImageHash'
        ],
    description='convert matplotlib figures into TikZ/PGFPlots',
    long_description=read('README.rst'),
    license=about['__license__'],
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
