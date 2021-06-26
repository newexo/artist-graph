import os


def qualifyname(directoryname, filename=None):
    if filename is None:
        return directoryname
    return os.path.join(directoryname, filename)


def code(filename=None):
    codepath = os.path.dirname(__file__)
    return qualifyname(codepath, filename)


def base(filename=None):
    basepath = os.path.abspath(code(".."))
    return qualifyname(basepath, filename)


def data(filename=None):
    return qualifyname(base("data"), filename)


def tests(filename=None):
    return qualifyname(code("tests"), filename)


def test_data(filename=None):
    return qualifyname(tests("test_data"), filename)
