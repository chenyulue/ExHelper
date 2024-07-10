from pathlib import Path
import sqlite3
import customtkinter as ctk

from .. import assets


class ConfigModel:
    def __init__(self) -> None:
        self.init_database()

        self.font_bold = ctk.CTkFont(family="SimHei", size=16, weight="bold")
        self.font_text = ctk.CTkFont(family="SimSun", size=16)
        self.text_spacing2 = 7
        self.text_spacing3 = 15
        self.check_items = {
            "摘要及其他缺陷": [
                "发明名称是否修改",
                "发明名称字数",
            ],
            "权利要求书缺陷": [
                "缺乏引用基础",
                "非择一引用",
                "疑似不清楚措辞",
            ],
            "说明书及附图缺陷": ["图号一致性", "附图标记错误"],
        }
        self.original_text_color = "red"
        self.modified_text_color = "blue"

        self.unclear_words = self.load_unclear_words()

    def init_database(self) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS unclear_words(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            words TEXT UNIQUE)""")
        conn.close()

    def load_unclear_words(self) -> list[str]:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        words = [item[0] for item in cur.execute("SELECT * FROM unclear_words")]
        conn.close()
        return words

    def save_unclear_words(self, words: list[str]) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.executemany("INSERT OR IGNORE INTO unclear_words(?)", words)
        conn.commit()
        conn.close()
