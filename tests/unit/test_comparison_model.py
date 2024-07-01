import pytest

from exhelper.model.ComparisonModel import ComparisonModel, ComparisonResult

@pytest.fixture
def model():
    return ComparisonModel("我们是中国人", "我们来自中国")

def test_new_model(model):
    assert model.text_modified == "我们是中国人"
    assert model.text_original == "我们来自中国"

def test_reset_texts(model):
    model.reset_texts("我们是伟大的中国人", "我们来自东方")
    assert model.text_modified == "我们是伟大的中国人"
    assert model.text_original == "我们来自东方"

def test_get_comparison_sequence(model):
    expected = [
        ComparisonResult("equal", "我们", "我们"),
        ComparisonResult("replace", "来自", "是"),
        ComparisonResult("equal", "中国", "中国"),
        ComparisonResult("insert", "", "人")
    ]
    assert list(model.get_comparison_sequence()) == expected