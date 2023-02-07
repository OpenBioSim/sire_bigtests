try:
    import sire as sr
    sr.use_old_api()
except Exception:
    pass

import os
import sys
import glob
import subprocess
import shlex

import Sire.Config

from nose.tools import assert_almost_equal


def test_analyse_freenrg(verbose=False):
    analyse_freenrg = os.path.join(Sire.Config.share_directory, "scripts", "analyse_freenrg.py")

    if verbose:
        print(analyse_freenrg)

    if not os.path.exists(analyse_freenrg):
        raise ValueError(f"Cannot find script {analyse_freenrg}")

    iopath = os.path.join("..", "io", "simfiles", "simfile_*.dat")

    if verbose:
        print(iopath)

    files = glob.glob(iopath)

    if len(files) == 0:
        raise ValueError(f"Cannot find simifles {iopath}")

    if len(files) != 9:
        raise ValueError(f"Didn't find all the simfiles in {iopath}. There should be 9. {files}")

    # python analyse_freenrg.py mbar -i "simfile_*.dat" -o freenrg-MBAR.dat --temperature 298.0 --percent 95 --overlap
    cmd = f"{sys.executable} {analyse_freenrg} mbar -i \"{iopath}\" -o freenrg-MBAR.dat --temperature 298.0 --percent 95 --overlap"

    if verbose:
        print(cmd)

    output = subprocess.check_output(shlex.split(cmd))

    if verbose:
        print(output.decode())

    # check the output file
    if not os.path.exists("freenrg-MBAR.dat"):
        raise ValueError(f"Job failed to run - no output!")

    lines = open("freenrg-MBAR.dat", "r").readlines()

    # check the free energies on the last lines
    mbar = float(lines[-3].split()[0].replace(",", ""))
    ti = float(lines[-1].split()[0].replace(",", ""))

    if verbose:
        print(f"freenrgs: {mbar} {ti}")

    assert_almost_equal(mbar, 4.695, 2)
    assert_almost_equal(ti, 4.695, 2)

    # remove the output file
    os.unlink("freenrg-MBAR.dat")


if __name__ == "__main__":
    test_analyse_freenrg(True)

