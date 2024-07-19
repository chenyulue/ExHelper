import tempfile
import os
import pytest

from exhelper.model import ConfigModel
from exhelper import assets

@pytest.fixture
def config():
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    yield ConfigModel(path), path
    os.close(fd)
    os.remove(path)

def text_new_config_model(config):
    assert config[0]._datafile == config[1]

def test_save_and_load_unclear_words(config):
    expected = ["等", "左右", "约", "可以", "可"]
    config[0].remove_unclear_words()
    config[0].save_unclear_words(expected)
    saved = config[0].load_unclear_words()
    assert saved == expected

def test_remove_unclear_words(config):
    config[0].save_unclear_words(["等", "左右"])
    config[0].remove_unclear_words()
    saved = config[0].load_unclear_words()
    assert saved == []

def test_save_duplicated_words(config):
    expected = ["等", "左右", "约", "可以", "可"]
    config[0].save_unclear_words(expected)
    config[0].save_unclear_words(expected)
    saved = config[0].load_unclear_words()
    assert saved == expected

def test_save_and_load_check_pattern(config):
    expected = [("figure_number", "图[0-9]+"), ("abstract_word", "[a-zA-Z]+|[^a-zA-Z]")]
    config[0].remove_check_pattern()
    for item in expected:
        config[0].save_check_pattern(*item)
    pattern1 = config[0].load_check_pattern("figure_number")
    pattern2 = config[0].load_check_pattern("abstract_word")
    assert pattern1 + pattern2 == ["图[0-9]+", "[a-zA-Z]+|[^a-zA-Z]"]

def test_update_check_pattern(config):
    config[0].remove_check_pattern()
    config[0].save_check_pattern("figure_number", "图[0-9]+")
    new_pattern = r"图\d+"
    config[0].save_check_pattern("figure_number", new_pattern)
    assert config[0].load_check_pattern("figure_number") == [new_pattern]
    