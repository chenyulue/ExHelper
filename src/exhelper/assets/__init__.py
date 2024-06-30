from pathlib import Path

CUR_DIR = Path(__file__).parent
EXAMINATION_ICON = CUR_DIR / "文件内容审查.png"
COMPARISON_ICON = CUR_DIR / "比较器.png"
DEADLINE_ICON = CUR_DIR / "日历.png"
ARCHIVE_ICON = CUR_DIR / "结案.png"
LOGIN_ICON = CUR_DIR / "登录.png"
SETTING_ICON = CUR_DIR / "设置.png"
ABOUT_ICON = CUR_DIR / "关于.png"

if __name__ == '__main__':
    print(type(EXAMINATION_ICON))