# matplotlib2tikz

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/matplotlib2tikz/master.svg)](https://circleci.com/gh/nschloe/matplotlib2tikz/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/matplotlib2tikz.svg)](https://codecov.io/gh/nschloe/matplotlib2tikz)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Documentation Status](https://readthedocs.org/projects/matplotlib2tikz/badge/?version=latest)](https://readthedocs.org/projects/matplotlib2tikz/?badge=latest)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg)](https://github.com/nschloe/matplotlib2tikz)
[![PyPi Version](https://img.shields.io/pypi/v/matplotlib2tikz.svg)](https://pypi.org/project/matplotlib2tikz)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1173089.svg)](https://doi.org/10.5281/zenodo.1173089)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/matplotlib2tikz.svg?logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/matplotlib2tikz)

This is matplotlib2tikz, a Python tool for converting matplotlib figures into
[PGFPlots](https://www.ctan.org/pkg/pgfplots) ([PGF/TikZ](https://www.ctan.org/pkg/pgf))
figures like

![](https://nschloe.github.io/matplotlib2tikz/example.png)

for native inclusion into LaTeX documents.

The output of matplotlib2tikz is in
[PGFPlots](http://pgfplots.sourceforge.net/pgfplots.pdf), a LaTeX library that sits on
top of [PGF/TikZ](https://en.wikipedia.org/wiki/PGF/TikZ) and describes graphs in terms
of axes, data etc. Consequently, the output of matplotlib2tikz

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

import matplotlib2tikz

matplotlib2tikz.save("test.tex")
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

matplotlib2tikz is [available from the Python Package
Index](https://pypi.org/project/matplotlib2tikz/), so simply type
```
pip3 install matplotlib2tikz --user
```
to install/update.


### Usage

1. Generate your matplotlib plot as usual.

2. Instead of `pyplot.show()`, invoke matplotlib2tikz by
    ```python
    import matplotlib2tikz
    matplotlib2tikz.save("mytikz.tex")
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
matplotlib2tikz can do, or if you are just looking for more information, then please
visit [matplotlib2tikz's GitHub page](https://github.com/nschloe/matplotlib2tikz).


### Testing

matplotlib2tikz has automatic unit testing to make sure that the software doesn't
accidentally get worse over time. In `test/`, a number of test cases are specified.
Those run through matplotlib2tikz and compare the output with a previously stored
reference TeX file.

To run the tests, just check out this repository and type
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

matplotlib2tikz is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
