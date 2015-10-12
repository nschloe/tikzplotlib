# matplotlib2tikz

[![Build Status](https://travis-ci.org/nschloe/matplotlib2tikz.svg?branch=test-failures)](https://travis-ci.org/nschloe/matplotlib2tikz)
[![Code Health](https://landscape.io/github/nschloe/matplotlib2tikz/master/landscape.png)](https://landscape.io/github/nschloe/matplotlib2tikz/master)
[![Coverage Status](https://coveralls.io/repos/nschloe/matplotlib2tikz/badge.svg?branch=test-failures&service=github)](https://coveralls.io/github/nschloe/matplotlib2tikz?branch=test-failures)
[![Documentation Status](https://readthedocs.org/projects/matplotlib2tikz/badge/?version=latest)](https://readthedocs.org/projects/matplotlib2tikz/?badge=latest)


This is matplotlib2tikz, a Python tool for converting matplotlib figures into
[PGFPlots](https://www.ctan.org/pkg/pgfplots)
([TikZ](https://www.ctan.org/pkg/pgf)) figures for native inclusion into LaTeX.

Since version 1.4, [matplotlib has a native
TikZ backend](http://matplotlib.org/users/whats_new.html#pgf-tikz-backend).
The output of matplotlib2tikz is in
[PGFPlots](http://pgfplots.sourceforge.net/pgfplots.pdf) an abstraction of TikZ
into the world of Graphs. Consequently, the output of matplotlib2tikz retains
more information, can be easier understood, and is much easier editable. For
example, the matplotlib figure
```

```
gives
```
% This file was created by matplotlib2tikz.
\begin{tikzpicture}

\definecolor{color0}{rgb}{0.886274509803922,0.290196078431373,0.2}
\definecolor{color1}{rgb}{0.203921568627451,0.541176470588235,0.741176470588235}

\begin{axis}[
title={Easier than easy $\frac{1}{2}$},
xlabel={time(s)},
ylabel={Voltage (mV)},
xmin=0, xmax=2,
ymin=-1, ymax=1,
width=7.5cm,
xmajorgrids,
ymajorgrids
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
\path [draw=white, fill opacity=0] (axis cs:13,0)--(axis cs:13,0);

\path [draw=white, fill opacity=0] (axis cs:0,13)--(axis cs:0,13);

\path [draw=white, fill opacity=0] (axis cs:1,13)--(axis cs:1,13);

\path [draw=white, fill opacity=0] (axis cs:13,1)--(axis cs:13,1);

\end{axis}

\end{tikzpicture}
```
Tweaking the plot becomes easy and can be done as part of your LaTeX workflow.
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

Download matplotlibtikz from https://github.com/nschloe/matplotlib2tikz.
Place the matplotlib2tikz script in a directory where Python can find it (e.g.,
`$PYTHONPATH`).  You can install it systemwide with
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
```
tikz_save('myfile.tikz');
```
   to store the TikZ file as `myfile.tikz`. Load the libary with:
```
from matplotlib2tikz import save as tikz_save
```

      _Optional:_
      The scripts accepts several options, for example `height`, `width`,
      `encoding`, and some others. Invoke by
```
tikz_save( 'myfile.tikz', figureheight='4cm', figurewidth='6cm' )
```

     IMPORTANT:
     Height and width must be set large enough; setting it too low it may
     result in a LaTeX compilation failure such as
        - Dimension Too Large, or
        - Arithmetic Overflow
      (see information about these errors in the manual of PGFPlots)

      To specify the dimension of the plot from within the LaTeX document, try

        tikz_save('myfile.tikz',
                  figureheight = '\\figureheight',
                  figurewidth = '\\figurewidth'
                  )

      and in the LaTeX source

        \newlength\figureheight
        \newlength\figurewidth
        \setlength\figureheight{4cm}
        \setlength\figurewidth{6cm}
        \input{myfile.tikz}

3. Add the contents of `myfile.tikz` into your LaTeX source code; a convenient
   way of doing so is to use `\input{/path/to/myfile.tikz}`. Also make sure
   that at the header of your document the packages TikZ and PGFPlots are
   included:

        \usepackage{tikz}
        \usepackage{pgfplots}

   Optionally, to use features of the latest PGFPlots package (as of
   PGFPlots 1.3), insert

        \pgfplotsset{compat=newest}

### Contributing

If you experience bugs, would like to contribute, have nice examples of what
matplotlib2tikz can do, or if you are just looking for more information, then
please visit [matplotlib2tikz's GitHub page]
(https://github.com/nschloe/matplotlib2tikz).


### Testing

matplotlib2tikz has automatic unit testing to make sure that the software
doesn't accidentally get worse over time. In `test/testfunctions/`, a number of
test cases are specified. Those are

 * run through matplotlib2tikz,
 * the resulting LaTeX file is compiled into a PDF (`pdflatex`),
 * the PDF is converted into a PNG
   ([`pdftoppm`](http://poppler.freedesktop.org/)),
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


### License

matplotlib2tikz is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
