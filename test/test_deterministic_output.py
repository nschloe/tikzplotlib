# assert repeated exports of the same plot produce the same output file

import subprocess
import sys
import tempfile

# We create the tikz files in separate subprocesses, as when producing those in
# the same process, the order of axis parameters is deterministic.
plot_code = """
import sys
import numpy as np
from matplotlib import pyplot as plt
import tikzplotlib

t = np.arange(0.0, 2.0, 0.1)
s = np.sin(2 * np.pi * t)
plt.plot(t, s, label="a")
plt.legend()
tikzplotlib.save(sys.argv[1])
"""


def test():
    _, tmp_base = tempfile.mkstemp()
    # trade-off between test duration and probability of false negative
    n_tests = 4
    tikzs = []
    for i in range(n_tests):
        tikz_file = tmp_base + "_tikz.tex"
        try:
            mpltt_out = subprocess.check_output(
                [sys.executable, "-", tikz_file],
                input=plot_code.encode(),
                stderr=subprocess.STDOUT,
            )
            sp = subprocess.Popen(
                ["python3", "-", tikz_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            (mpltt_out, _) = sp.communicate(plot_code.encode())
        except subprocess.CalledProcessError as e:
            print("Command output:")
            print("=" * 70)
            print(e.output)
            print("=" * 70)
            raise
        with open(tikz_file) as f:
            tikzs.append(f.read())
    for t in tikzs[1:]:
        assert t == tikzs[0]
