import pathlib

import duplicates
import settings

import test_base


TEST_DIR = ""


def setup_module(module):
    test_base.setup_module(module)


def setup_function(function):
    global TEST_DIR
    TEST_DIR = test_base.get_test_folder(function.__name__)
    TEST_DIR.mkdir(parents=True)


def test_find_duplicates_one_root():
    pathlib.Path(TEST_DIR, "pic1.jpg").touch()
    pathlib.Path(TEST_DIR, "pic2.jpg").touch()
    pathlib.Path(TEST_DIR, "subfolder1").mkdir()
    pathlib.Path(TEST_DIR, "subfolder1", "pic1.png").touch()
    pathlib.Path(TEST_DIR, "subfolder1", "pic2.jpg").touch()

    settings.SETTINGS_DIR = pathlib.Path(TEST_DIR, ".picorg")
    settings.get("pic_paths", [str(pathlib.Path(TEST_DIR))])

    result = duplicates.find_duplicates()

    expected = {
        "pic2.jpg": [
            pathlib.Path(TEST_DIR, "pic2.jpg"),
            pathlib.Path(TEST_DIR, "subfolder1", "pic2.jpg"),
        ]
    }
    assert len(result) == len(expected)
    assert sorted(result) == sorted(expected)


def test_find_duplicates_multiple_roots():
    pathlib.Path(TEST_DIR, "root1").mkdir()
    pathlib.Path(TEST_DIR, "root1", "pic1.jpg").touch()
    pathlib.Path(TEST_DIR, "root1", "pic2.jpg").touch()
    pathlib.Path(TEST_DIR, "root1", "subfolder1").mkdir()
    pathlib.Path(TEST_DIR, "root1", "subfolder1", "pic1.png").touch()
    pathlib.Path(TEST_DIR, "root1", "subfolder1", "pic2.jpg").touch()

    pathlib.Path(TEST_DIR, "root2").mkdir()
    pathlib.Path(TEST_DIR, "root2", "pic2.jpg").touch()
    pathlib.Path(TEST_DIR, "root2", "subfolder1").mkdir()
    pathlib.Path(TEST_DIR, "root2", "subfolder1", "pic1.jpg").touch()
    pathlib.Path(TEST_DIR, "root2", "subfolder1", "pic1.png").touch()

    settings.SETTINGS_DIR = pathlib.Path(TEST_DIR, ".picorg")
    settings.get("pic_paths", [str(pathlib.Path(TEST_DIR))])

    result = duplicates.find_duplicates()

    expected = {
        "pic1.jpg": [
            pathlib.Path(TEST_DIR, "root1", "pic1.jpg"),
            pathlib.Path(TEST_DIR, "root2", "subfolder1", "pic1.jpg"),
        ],
        "pic2.jpg": [
            pathlib.Path(TEST_DIR, "root1", "pic2.jpg"),
            pathlib.Path(TEST_DIR, "root1", "subfolder1", "pic2.jpg"),
            pathlib.Path(TEST_DIR, "root2", "pic2.jpg"),
        ],
    }
    assert len(result) == len(expected)
    assert sorted(result) == sorted(expected)
