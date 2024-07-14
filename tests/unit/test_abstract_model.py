import pytest
from exhelper.model import AbstractModel, ConfigModel

@pytest.fixture
def model():
    return AbstractModel("这是摘要测试，包括英文单词Word以及数字123，其中一个英文单词记为一个字数，其他均为一个字符记为一个字数。", ConfigModel())

def test_count_abstract_words_number(model):
    assert model.count_abstract_words_number() == 52