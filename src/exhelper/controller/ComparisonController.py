from ..model import ComparisonModel, ConfigModel
from ..view import ComparisonFrame

class ComparisonController:
    def __init__(self, model: ComparisonModel, view: ComparisonFrame) -> None:
        self.model = model
        self.view = view
        self.setting = ConfigModel()

    def clear_texts(self) -> None:
        self.view.text_left.delete("1.0", "end")
        self.view.text_right.delete("1.0", "end")
        self.view.text_bottom.delete("1.0", "end")

    def compare_texts(self) -> None:
        text_modified = self.view.text_left.get("1.0", "end").rstrip()
        text_original = self.view.text_right.get("1.0", "end").rstrip()
        self.model.reset_texts(text_modified, text_original)

        self.clear_texts()

        for result in self.model.get_comparison_sequence():
            if result.tag == "equal":
                self.view.text_left.insert("end", result.b, result.tag)
                self.view.text_right.insert("end", result.a, result.tag)
                self.view.text_bottom.insert("end", result.a, result.tag)
            else:
                self.view.text_left.insert("end", result.b, "modified")
                self.view.text_right.insert("end", result.a, "original")
                self.view.text_bottom.insert(
                    "end", result.a, (f"{result.tag}-original", "original"))
                self.view.text_bottom.insert(
                    "end", result.b, (f"{result.tag}-modified", "modified")
                )

        self.view.text_left.tag_config(
            "modified", foreground=self.setting.modified_text_color
        )
        self.view.text_right.tag_config(
            "original", foreground=self.setting.original_text_color
        )
        for tag in ("replace-original", "delete-original", "replace-modified", "insert-modified"):
            if tag.endswith("original"):
                self.view.text_bottom.tag_config(
                    tag, overstrike=True, foreground=self.setting.original_text_color,
                )
            elif tag.endswith("modified"):
                self.view.text_bottom.tag_config(
                    tag, underline=True, foreground=self.setting.modified_text_color
                )

    


