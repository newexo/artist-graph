import os

from art_graph import directories


class TestDirectories:
    def test_directories_exist(self):
        assert os.path.isdir(directories.base())
        assert os.path.isdir(directories.code())
        assert os.path.isdir(directories.tests())
        assert os.path.isdir(directories.test_data())

    def test_filenames(self):
        assert os.path.exists(directories.base("README.md"))
        assert os.path.exists(directories.code("__init__.py"))
        assert os.path.exists(directories.tests("__init__.py"))
        assert os.path.exists(directories.test_data("README.md"))
