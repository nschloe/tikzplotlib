# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import pypandoc

from matplotlib2tikz import __version__, __license__

longdesc = pypandoc.convert(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md'),
    'rst'
    )

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
    long_description=longdesc,
    license=__license__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion'
        ]
    )
