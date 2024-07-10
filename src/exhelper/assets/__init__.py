from pathlib import Path

CUR_DIR = Path(__file__).parent
EXAMINATION_ICON = CUR_DIR / "icons" / "文件内容审查.png"
COMPARISON_ICON = CUR_DIR / "icons" / "比较器.png"
DEADLINE_ICON = CUR_DIR / "icons" / "日历.png"
ARCHIVE_ICON = CUR_DIR / "icons" / "结案.png"
LOGIN_ICON = CUR_DIR / "icons" / "登录.png"
SETTING_ICON = CUR_DIR / "icons" / "设置.png"
ABOUT_ICON = CUR_DIR / "icons" / "关于.png"
SEARCH_ICON = CUR_DIR / "icons" / "查找.png"
REGEX_ON_ICON = CUR_DIR / "icons" / "正则表达式-on.png"
REGEX_OFF_ICON = CUR_DIR / "icons" / "正则表达式-off.png"
APP_ICON = CUR_DIR / "icons" / "APP-ICON.ico"

DEFAULT_THEME = CUR_DIR / "themes" / "Default.json"

DATA = CUR_DIR / "data.sqlite3"

if __name__ == '__main__':
    print(type(EXAMINATION_ICON))