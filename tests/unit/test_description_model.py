import pytest

from exhelper.model import DescriptionModel, ConfigModel

@pytest.fixture
def model():
    return DescriptionModel("这是说明书，其中有图1和图4至5","图1、图2、图3、图4、图5",ConfigModel())

def test_new_model(model):
    assert model._description == "这是说明书，其中有图1和图4至5"
    assert model._figure_numbers == "图1、图2、图3、图4、图5"
    assert model._figure_numbers_pattern == r"图\s*([0-9]+[a-zA-Z']*[(（]?[0-9a-zA-Z']*[)）]?([和至或到,、，-][0-9]+[a-zA-Z']*[(（]?[0-9a-zA-Z']*[)）]?)*)"
    assert model._figure_separator_pattern == "[和至或到,、，-]"
    assert "中共" in model._sensitive_words
    assert model._description_fignum == {}
    assert model._drawing_fignum == {}

def test_reset_description(model):
    model.reset_description("这是说明书", "这是附图")
    assert model._description == "这是说明书"
    assert model._figure_numbers == "这是附图"

def test_description_figure_numbers_are_obtained(model):
    model.check_figure_numbers_consistency()
    assert model._description_fignum == {
        "图1": [(9,11)],
        "图4": [(12,16)],
        "图5": [(12,16)]
    }
def test_drawing_figure_numbers_are_obtained(model):
    model.check_figure_numbers_consistency()
    assert model._drawing_fignum == {
        "图1": [(0, 2)],
        "图2": [(3, 5)],
        "图3": [(6, 8)],
        "图4": [(9, 11)],
        "图5": [(12, 14)]
    }

def test_check_figure_numbers_consistency_all_same(model):
    result = model.check_figure_numbers_consistency()
    assert result == ({}, {"图2":[(3,5)], "图3":[(6,8)]})

def test_split_compound_figure_numbers(model):
    model.reset_description("这是说明书，其中有图1和图4至5, 图6-4没有分成图6和图4","图1、图2、图3、图4、图5、图3-2")
    result = model.check_figure_numbers_consistency()
    assert result == (
        {"图6-4": [(18, 22)], "图6": [(26, 28)]},
        {"图2":[(3,5)], "图3":[(6,8)], "图3-2": [(15, 19)]}
    )

@pytest.mark.parametrize("fignum", [
    "图1", "图3(a)", "图34A", "图34A'", "图5（A）"
])
def test_all_kinds_of_figure_numbers(model, fignum):
    model.reset_description(
        f"这是说明书，其中有图1和图4至5, 包括可变图号{fignum}和其他图号", 
        "图1、图2、图3、图4")
    model.check_figure_numbers_consistency()
    assert fignum in model._description_fignum