from collections import defaultdict
from typing import Callable

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from ..model import CheckDefectModel, ConfigModel
from ..view import CheckDefectFrame


class CheckDefectController:
    def __init__(
        self, model: CheckDefectModel, view: CheckDefectFrame, setting: ConfigModel
    ) -> None:
        self.model = model
        self.view = view
        self.setting = setting

        # Simple Search
        self.simple_search_result = None
        self.simple_search_result_num = 0

        self.view.simple_search_pattern.trace_add("write", self._on_pattern_change)
        self.view.regex_is_on.trace_add("write", self._on_regex_changed)
        self.view.tabview_check.configure(command=self._on_checkview_tab_changed)
        self.view.tabview_result.configure(command=self._on_resultview_tab_changed)

        # Abstract or other defect check
        self._abstract_textbox: ctk.CTkTextbox = self.view.tabview_check.tab(
            "摘要"
        ).grid_slaves()[0]  # type: ignore

        # Claim check
        self.claim_unclear_words_result = None
        self._claim_textbox: ctk.CTkTextbox = self.view.tabview_check.tab(
            "权利要求书"
        ).grid_slaves()[0]  # type: ignore

        # Description check
        self.description_sensitive_words_result = None
        self._description_textbox: ctk.CTkTextbox = self.view.tabview_check.tab(
            "说明书及附图"
        ).grid_slaves(row=1, column=0)[0] # type: ignore
        self._fignumber_textbox: ctk.CTkTextbox = self.view.tabview_check.tab(
            "说明书及附图"
        ).grid_slaves(row=1, column=1)[0] # type: ignore

        # All Check Methods for all defects
        self.check_defects_method = {
            "摘要字数": self._abstract_check_word_number,
            "疑似不清楚措辞": self._claim_check_unclear_words,
            "说明书敏感词": self._description_check_sensitive_words,
            "图号一致性": self._description_check_figure_numbers_consistency
        }

    def _get_selected_check_items(self, defect_category: str) -> list[str]:
        checked = self.view.defect_check_items[
            defect_category
        ].get_checked_children_items()
        return checked

    def _on_regex_changed(self, *args):
        self.simple_search_result = None
        self.simple_search_result_num = 0

    def _on_checkview_tab_changed(self) -> None:
        self.simple_search_result = None
        self.simple_search_result_num = 0
        name = self.view.tabview_check.get()
        if name == "说明书及附图":
            self.view.tabview_check.tab(name).grid_slaves(row=1, column=0)[
                0
            ].focus_set()
        else:
            self.view.tabview_check.tab(name).grid_slaves()[0].focus_set()

    def _on_resultview_tab_changed(self) -> None:
        name = self.view.tabview_result.get()
        self.view.tabview_result.tab(name).grid_slaves()[0].focus_set()

    def _on_pattern_change(self, *args) -> None:
        self.simple_search_result = None
        self.simple_search_result_num = 0

    def simple_search(self) -> None:
        top, _ = self.view.get_current_tabs()
        textbox = top.grid_slaves(column=0)[0]

        if textbox.edit_modified():  # type: ignore
            self.simple_search_result = None
            self.simple_search_result_num = 0

        if self.simple_search_result is None:
            search_text = textbox.get("1.0", "end")  # type: ignore
            pattern = self.view.simple_search_pattern.get()
            self.model.search.reset_search_model(
                search_text,
                self.view.regex_is_on.get(),
            )
            self.model.search.set_search_pattern(pattern)

            self.simple_search_result = self.model.search.search()

        try:
            _, start, end = next(self.simple_search_result)
            self._highlight_text(textbox, (start, end))  # type: ignore
            self.simple_search_result_num += 1
        except StopIteration:
            if self.simple_search_result_num:
                msg = CTkMessagebox(
                    self.view,
                    title="继续搜索？",
                    message="已搜索到该文档的末尾，从头继续搜索吗？",
                    icon="warning",
                    option_1="继续",
                    option_2="取消",
                )
                if msg.get() == "继续":
                    self.simple_search_result = None
                    self.simple_search_result_num = 0
                    self.simple_search()
            else:
                CTkMessagebox(
                    self.view,
                    title="搜索结果",
                    message="未搜索到相关结果",
                    icon="info",
                    option_1="好的",
                )

        textbox.edit_modified(False)  # type: ignore

    def _highlight_text(self, textbox: ctk.CTkTextbox, index: tuple[int, int]):
        textbox.focus()
        textbox.tag_remove("sel", "1.0", "end")

        textbox.see(f"1.0+{index[0]}c")
        textbox.mark_set("insert", f"1.0+{index[1]}c")

        textbox.tag_add("sel", f"1.0+{index[0]}c", f"1.0+{index[1]}c")

    def clear_text(self) -> None:
        for _, tab in self.view.tabview_check._tab_dict.items():
            for text_widget in tab.grid_slaves():
                if isinstance(text_widget, ctk.CTkTextbox):
                    text_widget.delete("1.0", "end")
        self._clear_result_text()

    def _clear_result_tags(self) -> None:
        for _, tab in self.view.tabview_check._tab_dict.items():
            for text_widget in tab.grid_slaves():
                if isinstance(text_widget, ctk.CTkTextbox):
                    for tag in text_widget.tag_names():
                        text_widget.tag_remove(tag, "1.0", "end")

    def _clear_result_text(self) -> None:
        for _, tab in self.view.tabview_result._tab_dict.items():
            for text_widget in tab.grid_slaves():
                if isinstance(text_widget, ctk.CTkTextbox):
                    text_widget.configure(state="normal") # type: ignore
                    text_widget.delete("1.0", "end") # type: ignore

    ###### Abstract or other defects check ########
    def _abstract_check_word_number(self) -> None:
        self.model.abstract.reset_abstract(
            self._abstract_textbox.get("1.0", "end").strip()
        )
        count = self.model.abstract.count_abstract_words_number()

        self._abstract_check_word_number_show_result(count)
        
    def _abstract_check_word_number_show_result(self, n: int) -> None:
        if n > 300:
            result_textbox: ctk.CTkTextbox = self.view.tabview_result.tab(
                "摘要及其他缺陷"
            ).grid_slaves()[0] # type: ignore
            result_textbox.configure(state="normal")

            result_textbox.insert("end", "【摘要字数】\n    ")
            result_textbox.insert("end", f"摘要字数为{n}个字，请注意是否需要申请人补正")

            result_textbox.configure(state="disabled")

    ###### Claim defects check ##########################
    def _claim_check_unclear_words(self) -> None:
        self.model.claim.reset_claims(self._claim_textbox.get("1.0", "end"))
        self._claim_textbox.tag_remove("unclear-words", "1.0", "end")
        self._claim_textbox.tag_remove("current", "1.0", "end")
        self.claim_unclear_words_result = defaultdict(list)

        for match, start, end in self.model.claim.check_unclear_words():
            self._claim_textbox.tag_add("unclear-words", f"1.0+{start}c", f"1.0+{end}c")
            self.claim_unclear_words_result[match.group()].append((start, end))

        self._claim_textbox.tag_config("unclear-words", background="yellow")

        self._claim_check_unclear_words_show_result()

    def _claim_check_unclear_words_show_result(self) -> None:
        if bool(self.claim_unclear_words_result):
            result_textbox: ctk.CTkTextbox = self.view.tabview_result.tab(
                "权利要求书缺陷"
            ).grid_slaves()[0]  # type: ignore
            result_textbox.configure(state="normal")

            result_textbox.insert("end", "【疑似不清楚措辞】\n    ")
            for word, index in self.claim_unclear_words_result.items():
                result_textbox.insert("end", word, tags=(word, "unclear-words"))
                result_textbox.insert("end", "  ")
                result_textbox.tag_bind(
                    word, "<Button-1>", self._focus_words(index, "权利要求书")
                )
            result_textbox.tag_config(
                "unclear-words", underline=True, foreground="blue"
            )
            result_textbox.tag_bind(
                "unclear-words",
                "<Enter>",
                lambda event: result_textbox.configure(cursor="hand2"),
            )
            result_textbox.tag_bind(
                "unclear-words",
                "<Leave>",
                lambda event: result_textbox.configure(cursor="arrow"),
            )

            result_textbox.configure(state="disabled")

    def _focus_words(self, index: list[tuple[int, int]], name: str, row:int=0, column:int=0) -> Callable:
        size = len(index)
        i = 0

        def skip_to_word(event):
            nonlocal i
            self.view.tabview_check.set(name)
            textbox: ctk.CTkTextbox = self.view.tabview_check.tab(name).grid_slaves(row=row, column=column)[0]  # type: ignore
            # textbox.tag_remove("sel", "1.0", "end")
            textbox.tag_remove("current", "1.0", "end")

            idx = i % size
            start, end = index[idx]

            textbox.see(f"1.0+{start}c")

            textbox.tag_add("current", f"1.0+{start}c", f"1.0+{end}c")
            textbox.tag_config("current", background="orange")

            i += 1

        return skip_to_word

    #### Description defect check #####
    def _description_check_sensitive_words(self) -> None:
        self.model.description.reset_description(
            self._description_textbox.get("1.0", "end"),
            self._fignumber_textbox.get("1.0", "end"),
        )
        self._description_textbox.tag_remove("sensitive-words", "1.0", "end")
        self._description_textbox.tag_remove("current", "1.0", "end")
        self.description_sensitive_words_result = defaultdict(list)

        for match, start, end in self.model.description.check_sensitive_words():
            self._description_textbox.tag_add("sensitive-words", f"1.0+{start}c", f"1.0+{end}c")
            self.description_sensitive_words_result[match.group()].append((start, end))

        self._description_textbox.tag_config("sensitive-words", background="red")

        self._description_check_sensitive_words_show_result()

    def _description_check_sensitive_words_show_result(self) -> None:
        if bool(self.description_sensitive_words_result):
            result_textbox: ctk.CTkTextbox = self.view.tabview_result.tab(
                "说明书及附图缺陷"
            ).grid_slaves()[0]  # type: ignore
            result_textbox.configure(state="normal")

            result_textbox.insert("end", "【说明书敏感词】\n    ")
            for word, index in self.description_sensitive_words_result.items():
                result_textbox.insert("end", word, tags=(word, "sensitive-words"))
                result_textbox.insert("end", "  ")
                result_textbox.tag_bind(
                    word, "<Button-1>", self._focus_words(index, "说明书及附图", row=1)
                )
            result_textbox.tag_config(
                "sensitive-words", underline=True, foreground="blue"
            )
            result_textbox.tag_bind(
                "sensitive-words",
                "<Enter>",
                lambda event: result_textbox.configure(cursor="hand2"),
            )
            result_textbox.tag_bind(
                "sensitive-words",
                "<Leave>",
                lambda event: result_textbox.configure(cursor="arrow"),
            )

            result_textbox.configure(state="disabled")

    def _description_check_figure_numbers_consistency(self) -> None:
        self.model.description.reset_description(
            self._description_textbox.get("1.0", "end"),
            self._fignumber_textbox.get("1.0", "end"),
        )
        
        self._description_textbox.tag_remove("figure_numbers", "1.0", "end")
        self._description_textbox.tag_remove("current", "1.0", "end")
        self._fignumber_textbox.tag_remove("figure_numbers", "1.0", "end")
        self._fignumber_textbox.tag_remove("current", "1.0", "end")

        extra_in_description, extra_in_drawing = self.model.description.check_figure_numbers_consistency()
        for _, positions in extra_in_description.items():
            for start, end in positions:
                self._description_textbox.tag_add("figure_numbers", f"1.0+{start}c", f"1.0+{end}c")
        self._description_textbox.tag_config("figure_numbers", background="yellow")
        self._description_check_figure_numbers_consistency_show_result(extra_in_description, "说明书中多余图号", 1, 0)

        for _, positions in extra_in_drawing.items():
            for start, end in positions:
                self._fignumber_textbox.tag_add("figure_numbers", f"1.0+{start}c", f"1.0+{end}c")
        self._fignumber_textbox.tag_config("figure_numbers", background="yellow")
        self._description_check_figure_numbers_consistency_show_result(extra_in_drawing, "附图中多余图号", 1, 1)

    def _description_check_figure_numbers_consistency_show_result(self, result: dict[str, list[tuple[int, int]]], label: str, bind_row: int, bind_column: int) -> None:
        if result:
            result_textbox: ctk.CTkTextbox = self.view.tabview_result.tab(
                "说明书及附图缺陷"
            ).grid_slaves()[0]  # type: ignore
            result_textbox.configure(state="normal")

            result_textbox.insert("end", f"【{label}】\n    ")
            for word, index in result.items():
                result_textbox.insert("end", word, tags=(word, "figure_numbers"))
                result_textbox.insert("end", "  ")
                result_textbox.tag_bind(
                    word, "<Button-1>", self._focus_words(index, "说明书及附图", row=bind_row, column=bind_column)
                )
            else:
                result_textbox.insert("end", "\n")
                
            result_textbox.tag_config(
                "figure_numbers", underline=True, foreground="blue"
            )
            result_textbox.tag_bind(
                "figure_numbers",
                "<Enter>",
                lambda event: result_textbox.configure(cursor="hand2"),
            )
            result_textbox.tag_bind(
                "figure_numbers",
                "<Leave>",
                lambda event: result_textbox.configure(cursor="arrow"),
            )

            result_textbox.configure(state="disabled")

    # Check entry
    def check_defects(self) -> None:
        abstract_other_defects = self._get_selected_check_items("摘要及其他缺陷")
        claims_defects = self._get_selected_check_items("权利要求书缺陷")
        description_defects = self._get_selected_check_items("说明书及附图缺陷")

        self._clear_result_text()
        self._clear_result_tags()
        for item in abstract_other_defects:
            self.check_defects_method.get(item, lambda: None)()

        for item in claims_defects:
            self.check_defects_method.get(item, lambda: None)()

        for item in description_defects:
            self.check_defects_method.get(item, lambda: None)()
