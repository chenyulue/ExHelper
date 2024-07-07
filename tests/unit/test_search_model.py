import pytest
import exhelper.model as mod

@pytest.fixture
def model():
    return mod.SearchModel("这是图1，在后面还有图2，所以有两个图号") # type: ignore

def test_new_model(model):
    assert model.content == "这是图1，在后面还有图2，所以有两个图号"
    assert model.pattern is None
    assert model.use_regex

def test_set_search_pattern(model):
    model.set_search_pattern(r"图\d+")
    assert model.pattern is not None

def test_set_search_malformed_pattern(model):
    with pytest.raises(ValueError):
        model.set_search_pattern(r"图[0-9")

def test_reset_search_model(model):
    model.reset_search_model("abc", False)
    assert model.content == "abc"
    assert model.pattern is None
    assert model.use_regex is False

def test_search(model):
    model.set_search_pattern(r"图\d+")
    expected = [("图1", 2, 4), ("图2", 10, 12)]
    for r, e in zip(model.search(), expected):
        assert r.match.group(0) == e[0]
        assert r.start == e[1]
        assert r.end == e[2]