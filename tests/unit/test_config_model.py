import tempfile
import os
import pytest

from exhelper.model import ConfigModel

@pytest.fixture
def config():
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    yield ConfigModel(path)
    os.close(fd)
    os.remove(path)

def test_save_and_load_unclear_words(config):
    expected = ["等", "左右", "约", "可以", "可"]
    config.remove_unclear_words()
    config.save_unclear_words(expected)
    saved = config.load_unclear_words()
    assert saved == expected

def test_remove_unclear_words(config):
    config.save_unclear_words(["等", "左右"])
    config.remove_unclear_words()
    saved = config.load_unclear_words()
    assert saved == []

def test_save_duplicated_words(config):
    expected = ["等", "左右", "约", "可以", "可"]
    config.save_unclear_words(expected)
    config.save_unclear_words(expected)
    saved = config.load_unclear_words()
    assert saved == expected

def test_save_and_load_check_pattern(config):
    expected = [("figure_number", "图[0-9]+"), ("abstract_word", "[a-zA-Z]+|[^a-zA-Z]")]
    config.remove_check_pattern()
    for item in expected:
        config.save_check_pattern(*item)
    pattern1 = config.load_check_pattern("figure_number")
    pattern2 = config.load_check_pattern("abstract_word")
    assert pattern1 + pattern2 == ["图[0-9]+", "[a-zA-Z]+|[^a-zA-Z]"]

def test_update_check_pattern(config):
    config.remove_check_pattern()
    config.save_check_pattern("figure_number", "图[0-9]+")
    new_pattern = r"图\d+"
    config.save_check_pattern("figure_number", new_pattern)
    assert config.load_check_pattern("figure_number") == [new_pattern]
    