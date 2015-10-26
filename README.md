# matplotlib2tikz

[![Build Status](https://travis-ci.org/nschloe/matplotlib2tikz.svg?branch=master)](https://travis-ci.org/nschloe/matplotlib2tikz)
[![Code Health](https://landscape.io/github/nschloe/matplotlib2tikz/master/landscape.png)](https://landscape.io/github/nschloe/matplotlib2tikz/master)
[![Coverage Status](https://coveralls.io/repos/nschloe/matplotlib2tikz/badge.svg?branch=master&service=github)](https://coveralls.io/github/nschloe/matplotlib2tikz?branch=master)
[![Documentation Status](https://readthedocs.org/projects/matplotlib2tikz/badge/?version=latest)](https://readthedocs.org/projects/matplotlib2tikz/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/matplotlib2tikz.svg)](https://pypi.python.org/pypi/matplotlib2tikz)
[![PyPi Downloads](https://img.shields.io/pypi/dm/matplotlib2tikz.svg)](https://pypi.python.org/pypi/matplotlib2tikz)

This is matplotlib2tikz, a Python tool for converting matplotlib figures into
[PGFPlots](https://www.ctan.org/pkg/pgfplots)
([TikZ](https://www.ctan.org/pkg/pgf)) figures like

![](https://nschloe.github.io/matplotlib2tikz/latex3.png)

for native inclusion into LaTeX.

The output of matplotlib2tikz is in
[PGFPlots](http://pgfplots.sourceforge.net/pgfplots.pdf), a LaTeX library that
sits on top of TikZ and describes graphs in terms of axes, data etc.
Consequently, the output of matplotlib2tikz retains more information, can be
more easily understood, and is more easily editable than [raw TikZ output](http://matplotlib.org/users/whats_new.html#pgf-tikz-backend). For
example, the matplotlib figure
```python
from matplotlib import pyplot as pp
from matplotlib import style
import numpy as np
fig = pp.figure()
style.use('ggplot')
t = np.arange(0.0, 2.0, 0.1)
s = np.sin(2*np.pi*t)
s2 = np.cos(2*np.pi*t)
pp.plot(t, s, 'o-', lw=4.1)
pp.plot(t, s2, 'o-', lw=4.1)
pp.xlabel('time(s)')
pp.ylabel('Voltage (mV)')
pp.title('Simple plot $\\frac{\\alpha}{2}$')
pp.grid(True)
```
(see above) gives
```latex
% This file was created by matplotlib2tikz.
\begin{tikzpicture}

\definecolor{color1}{rgb}{0.203921568627451,0.541176470588235,0.741176470588235}
\definecolor{color0}{rgb}{0.886274509803922,0.290196078431373,0.2}

\begin{axis}[
title={Simple plot $\frac{\alpha}{2}$},
xlabel={time(s)},
ylabel={Voltage (mV)},
xmin=0, xmax=2,
ymin=-1, ymax=1,
width=7.5cm,
tick align=outside,
xmajorgrids,
x grid style={white},
ymajorgrids,
y grid style={white},
axis line style={white},
axis background/.style={fill=white!89.803921568627459!black}
]
\addplot [line width=1.64pt, color0, mark=*, mark size=3, mark options={draw=black}]
coordinates {
(0,0)
(0.1,0.587785252292473)
% [...]
(1.9,-0.587785252292473)
};
\addplot [line width=1.64pt, color1, mark=*, mark size=3, mark options={draw=black}]
coordinates {
(0,1)
(0.1,0.809016994374947)
% [...]
(1.9,0.809016994374947)
};
\end{axis}

\end{tikzpicture}
```
Tweaking the plot is straightforward and can be done as part of your LaTeX
work flow.
[The fantastic PGFPlots manual](http://pgfplots.sourceforge.net/pgfplots.pdf)
contains great examples of how to make your plot look even better.

### Installation

#### Python Package Index

matplotlib2tikz is [available from the Python Package
Index](https://pypi.python.org/pypi/matplotlib2tikz/), so simply type
```
pip install matplotlib2tikz
```

#### Manual installation

Download matplotlib2tikz from
[the Python Package Index](https://pypi.python.org/pypi/matplotlib2tikz/).
Place the matplotlib2tikz script in a directory where Python can find it (e.g.,
`$PYTHONPATH`).  You can install it system-wide with
```
python setup.py install
```
or place the script `matplotlib2tikz.py` into the directory where you intend to
use it.

#### Dependencies

matplotlib2tikz needs [matplotlib](http://matplotlib.org/) and
[NumPy](http://www.numpy.org/) to work. matplotlib2tikz works both with
Python 2 and Python 3.

To use the resulting TikZ/PGFPlots figures, your LaTeX installation needs

  * TikZ (aka PGF, >=2.00), and
  * PGFPlots (>=1.3).


### Usage

1. Generate your matplotlib plot as usual.

2. Instead of `pyplot.show()`, invoke matplotlib2tikz by
    ```python
    tikz_save('mytikz.tex');
    ```
   to store the TikZ file as `mytikz.tex`. Load the library with:
    ```python
    from matplotlib2tikz import save as tikz_save
    ```
   _Optional:_
   The scripts accepts several options, for example `height`, `width`,
   `encoding`, and some others. Invoke by
    ```python
    tikz_save('mytikz.tex', figureheight='4cm', figurewidth='6cm')
    ```
   Note that height and width must be set large enough; setting it too low may
   result in a LaTeX compilation failure along the lines of `Dimension Too Large` or `Arithmetic Overflow`;
   see information about these errors in [the PGFPlots manual](http://pgfplots.sourceforge.net/pgfplots.pdf).
   To specify the dimension of the plot from within the LaTeX document, try
    ```python
    tikz_save(
        'mytikz.tex',
        figureheight = '\\figureheight',
        figurewidth = '\\figurewidth'
        )
    ```
    and in the LaTeX source
    ```latex
    \newlength\figureheight
    \newlength\figurewidth
    \setlength\figureheight{4cm}
    \setlength\figurewidth{6cm}
    \input{mytikz.tex}
    ```

3. Add the contents of `mytikz.tex` into your LaTeX source code; a convenient
   way of doing so is via `\input{/path/to/mytikz.tex}`. Also make sure that
   in the header of your document the packages for PGFPlots and proper Unicode
   support and are included:
    ```latex
    \usepackage[utf8]{inputenc}
    \usepackage{pgfplots}
    ```
   Additionally, with LuaLaTeX
    ```latex
    \usepackage{fontspec}
    ```
   is needed to typeset Unicode characters.
   Optionally, to use the latest PGFPlots features, insert
    ```latex
    \pgfplotsset{compat=newest}
    ```

### Contributing

If you experience bugs, would like to contribute, have nice examples of what
matplotlib2tikz can do, or if you are just looking for more information, then
please visit
[matplotlib2tikz's GitHub page](https://github.com/nschloe/matplotlib2tikz).


### Testing

matplotlib2tikz has automatic unit testing to make sure that the software
doesn't accidentally get worse over time. In `test/testfunctions/`, a number of
test cases are specified. Those are

 * run through matplotlib2tikz,
 * the resulting LaTeX file is compiled into a PDF (`pdflatex`),
 * the PDF is converted into a PNG (`pdftoppm`),
 * a perceptual hash is computed from the PNG and compared to a previously
   stored version.

To run the tests, just check out this repository and type
```
nosetests
```
or
```
nose2 -s test
```

The final pHash may depend on any of the tools used during the process. For
example, if your version of [Pillow](https://pypi.python.org/pypi/Pillow/3.0.0)
is too old, the pHash function might operate slightly differently and produce a
slightly different pHash, resulting in a failing test. If tests are failing on
your local machine, you should first make sure to have an up-to-date Pillow, .

If you would like to contribute a test, just take a look at the examples in
`test/testfunctions/`. Essentially a test consists of three things:

  * a description,
  * a function that creates the image in matplotlib, and
  * a pHash.

Just add your file, add it to `test/testfunction/__init__.py`, and run the
tests. A failing test will always print out the pHash, so you can leave it
empty in the first run and fill it in later to make the test pass.

### Distribution

To create a new release

1. bump the `__version__` number,

2. create a Git tag,
    ```
    $ git tag -a v0.3.1
    $ git push --tags
    ```
    and

3. upload to PyPi:
    ```
    $ make upload
    ```

### License

matplotlib2tikz is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
