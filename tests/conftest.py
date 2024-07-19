def pytest_collection_modifyitems(items):
    for item in items:
        # 重新编码name和nodeid，以正确显示中文字符
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")