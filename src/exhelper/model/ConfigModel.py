from pathlib import Path
import sqlite3
import customtkinter as ctk

from .. import assets


class ConfigModel:
    def __init__(self, datafile: Path | str = assets.DATA) -> None:
        self._datafile = datafile

        self.font_family = "SimHei"
        self.font_size = 16
        self.text_spacing2 = 7
        self.text_spacing3 = 15
        self.check_items = {
            "摘要及其他缺陷": ["发明名称是否修改", "发明名称字数", "摘要字数"],
            "权利要求书缺陷": [
                "缺乏引用基础",
                "非择一引用",
                "疑似不清楚措辞",
            ],
            "说明书及附图缺陷": ["图号一致性", "附图标记错误", "说明书敏感词"],
        }
        self.original_text_color = "red"
        self.modified_text_color = "blue"

        self.init_database()

        self.unclear_words = self.load_unclear_words()

    @property
    def font_bold(self):
        return ctk.CTkFont(family=self.font_family, size=self.font_size, weight="bold")

    @property
    def font_text(self):
        return ctk.CTkFont(family="SimSun", size=self.font_size)

    def init_database(self) -> None:
        conn = sqlite3.connect(self._datafile)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS unclear_words(
            words TEXT UNIQUE NOT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS check_pattern(
            kind TEXT UNIQUE NOT NULL DEFAULT "",
            pattern TEXT UNIQUE NOT NULL DEFAULT "")""")
        cur.execute("""CREATE TABLE IF NOT EXISTS sensitive_words(
            words TEXT UNIQUE NOT NULL)""")
        conn.close()

    def load_unclear_words(self) -> list[str]:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        words = [item[0] for item in cur.execute("SELECT words FROM unclear_words")]
        conn.close()
        return words

    def save_unclear_words(self, words: list[str]) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR IGNORE INTO unclear_words (words) VALUES(?)",
            [(w,) for w in words],
        )
        conn.commit()
        conn.close()

    def remove_unclear_words(self) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.execute("DELETE FROM unclear_words")
        conn.commit()
        conn.close()

    def load_check_pattern(self, kind: str) -> list[str]:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        pattern = [
            item[0]
            for item in cur.execute(
                "SELECT pattern FROM check_pattern WHERE kind==(?)", [kind]
            )
        ]
        conn.close()
        return pattern

    def save_check_pattern(self, kind: str, pattern: str) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO check_pattern VALUES (?,?)", [kind, pattern]
        )
        conn.commit()
        conn.close()

    def remove_check_pattern(self) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.execute("DELETE FROM check_pattern")
        conn.commit()
        conn.close()

    def load_sensitive_words(self) -> list[str]:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        words = [item[0] for item in cur.execute("SELECT words FROM sensitive_words")]
        conn.close()
        return words

    def save_sensitive_words(self, words: list[str]) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR IGNORE INTO sensitive_words (words) VALUES(?)",
            [(w,) for w in words],
        )
        conn.commit()
        conn.close()

    def remove_sensitive_words(self) -> None:
        conn = sqlite3.connect(assets.DATA)
        cur = conn.cursor()
        cur.execute("DELETE FROM sensitive_words")
        conn.commit()
        conn.close()
