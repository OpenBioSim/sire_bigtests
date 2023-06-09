try:
    import sire as sr

    sr.use_old_api()
except ImportError:
    pass

from Sire.IO import *
from Sire.Mol import *

from nose.tools import assert_equal, assert_almost_equal

# check that we have Gro87 support in this version of Sire
has_gro87 = True

try:
    p = Gro87()
except:
    # No Gro87 support
    has_gro87 = False


def _assert_strings_equal(x, y):
    assert_equal(len(x), len(y))

    for i in range(0, len(x)):
        assert_equal(x[i], y[i])


def _assert_equal(x, y, diff):
    if abs(x - y) > diff:
        assert_equal(x, y)


def _assert_almost_equal(v0, v1):
    assert_equal(len(v0), len(v1))

    is_vec = False

    try:
        v0[0].x()
        is_vec = True
    except:
        pass

    if is_vec:
        for i in range(0, len(v0)):
            _assert_equal(v0[i].x(), v1[i].x(), 0.01)
            _assert_equal(v0[i].y(), v1[i].y(), 0.01)
            _assert_equal(v0[i].z(), v1[i].z(), 0.01)
    else:
        for i in range(0, len(v0)):
            _assert_equal(v0[i], v1[i], 0.01)


def test_gro_rst(verbose=False):
    if not has_gro87:
        return

    # read in the system using a different format
    if verbose:
        print("Reading in rst/top file...")

    s = MoleculeParser.read("../io/NA16.rst", "../io/NA16.top")

    # Convert the data to Gro87
    if verbose:
        print("Converting...")

    g = Gro87(s)

    # Ensure that the numbers of atoms etc. are all correct
    if verbose:
        print("Converting to RST...")

    a = AmberRst(s)

    if verbose:
        print("Comparing...")

    assert_equal(g.nAtoms(), a.nAtoms())

    if verbose:
        print("Writing...")

    g.writeToFile("test.gro")

    if verbose:
        print("Re-reading...")

    g2 = Gro87("test.gro")

    if verbose:
        print("Comparing...")

    assert_equal(g.nAtoms(), g2.nAtoms())


def test_gro87(verbose=False):
    if not has_gro87:
        return

    if verbose:
        print("Reading the Gro87 file using the Gro87 parser...")

    grofile = "../io/water.gro"
    # grofile = "../io/urea.gro"

    gro87 = Gro87(grofile)

    if verbose:
        print(gro87)


if __name__ == "__main__":
    test_gro87(True)
    test_gro_rst(True)
