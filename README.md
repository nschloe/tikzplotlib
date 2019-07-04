<p align="center">
  <img alt="tikzplotlib" src="https://nschloe.github.io/tikzplotlib/logo-tikzplotlib.svg" width="60%">
</p>

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/tikzplotlib/master.svg?style=flat-square)](https://circleci.com/gh/nschloe/tikzplotlib/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/tikzplotlib.svg?style=flat-square)](https://codecov.io/gh/nschloe/tikzplotlib)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![Documentation Status](https://readthedocs.org/projects/tikzplotlib/badge/?version=latest&style=flat-square)](https://readthedocs.org/projects/tikzplotlib/?badge=latest)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg?style=flat-square)](https://github.com/nschloe/tikzplotlib)
[![PyPi Version](https://img.shields.io/pypi/v/tikzplotlib.svg?style=flat-square)](https://pypi.org/project/tikzplotlib)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1173089.svg?style=flat-square)](https://doi.org/10.5281/zenodo.1173089)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/tikzplotlib.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/tikzplotlib)
[![PyPi downloads](https://img.shields.io/pypi/dd/tikzplotlib.svg?style=flat-square)](https://pypistats.org/packages/tikzplotlib)

This is tikzplotlib, a Python tool for converting matplotlib figures into
[PGFPlots](https://www.ctan.org/pkg/pgfplots) ([PGF/TikZ](https://www.ctan.org/pkg/pgf))
figures like

![](https://nschloe.github.io/tikzplotlib/example.png)

for native inclusion into LaTeX documents.

The output of tikzplotlib is in
[PGFPlots](http://pgfplots.sourceforge.net/pgfplots.pdf), a LaTeX library that sits on
top of [PGF/TikZ](https://en.wikipedia.org/wiki/PGF/TikZ) and describes graphs in terms
of axes, data etc. Consequently, the output of tikzplotlib

  * retains more information,
  * can be more easily understood, and
  * is more easily editable

than [raw TikZ output](https://matplotlib.org/users/whats_new.html#pgf-tikz-backend).
For example, the matplotlib figure
```python,test
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")

t = np.arange(0.0, 2.0, 0.1)
s = np.sin(2 * np.pi * t)
s2 = np.cos(2 * np.pi * t)
plt.plot(t, s, "o-", lw=4.1)
plt.plot(t, s2, "o-", lw=4.1)
plt.xlabel("time (s)")
plt.ylabel("Voltage (mV)")
plt.title("Simple plot $\\frac{\\alpha}{2}$")
plt.grid(True)

import tikzplotlib

tikzplotlib.save("test.tex")
```
(see above) gives
```latex
\begin{tikzpicture}

\definecolor{color0}{rgb}{0.886274509803922,0.290196078431373,0.2}
\definecolor{color1}{rgb}{0.203921568627451,0.541176470588235,0.741176470588235}

\begin{axis}[
axis background/.style={fill=white!89.80392156862746!black},
axis line style={white},
tick align=outside,
tick pos=left,
title={Simple plot $\frac{\alpha}{2}$},
x grid style={white},
xlabel={time (s)},
xmajorgrids,
xmin=-0.095, xmax=1.995,
y grid style={white},
ylabel={Voltage (mV)},
ymajorgrids,
ymin=-1.1, ymax=1.1
]
\addplot [line width=1.64pt, color0, mark=*, mark size=3, mark options={solid}]
table {%
0 0
0.1 0.587785252292473
% [...]
1.9 -0.587785252292473
};
\addplot [line width=1.64pt, color1, mark=*, mark size=3, mark options={solid}]
table {%
0 1
0.1 0.809016994374947
% [...]
1.9 0.809016994374947
};
\end{axis}

\end{tikzpicture}
```
(Use `get_tikz_code()` instead of `save()` if you want the code as a string.)

Tweaking the plot is straightforward and can be done as part of your LaTeX work flow.
[The fantastic PGFPlots manual](http://pgfplots.sourceforge.net/pgfplots.pdf) contains
great examples of how to make your plot look even better.

Of course, not all figures produced by matplotlib can be converted without error.
Notably, [3D plots don't work](https://github.com/matplotlib/matplotlib/issues/7243).

### Installation

tikzplotlib is [available from the Python Package
Index](https://pypi.org/project/tikzplotlib/), so simply type
```
pip3 install tikzplotlib --user
```
to install/update.


### Usage

1. Generate your matplotlib plot as usual.

2. Instead of `pyplot.show()`, invoke tikzplotlib by
    ```python
    import tikzplotlib
    tikzplotlib.save("mytikz.tex")
    ```
   to store the TikZ file as `mytikz.tex`.

3. Add the contents of `mytikz.tex` into your LaTeX source code. A convenient way of
   doing so is via
    ```latex
    \input{/path/to/mytikz.tex}
    ```
   Also make sure that the packages for PGFPlots and proper Unicode support and are
   included in the header of your document:
    ```latex
    \usepackage[utf8]{inputenc}
    \usepackage{fontspec}  % optional
    \usepackage{pgfplots}
    \pgfplotsset{compat=newest}
    \usepgfplotslibrary{groupplots}
    \usepgfplotslibrary{dateplot}
    ```

### Contributing

If you experience bugs, would like to contribute, have nice examples of what
tikzplotlib can do, or if you are just looking for more information, then please
visit [tikzplotlib's GitHub page](https://github.com/nschloe/tikzplotlib).


### Testing

tikzplotlib has automatic unit testing to make sure that the software doesn't
accidentally get worse over time. In `test/`, a number of test cases are specified.
Those run through tikzplotlib and compare the output with a previously stored
reference TeX file.

To run the tests, just check out this repository and type
```
pytest
```

### License

tikzplotlib is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
