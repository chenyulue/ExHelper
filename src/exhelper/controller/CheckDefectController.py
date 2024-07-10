import itertools

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from ..model import CheckDefectModel, ConfigModel
from ..view import CheckDefectFrame


class CheckDefectController:
    def __init__(self, model: CheckDefectModel, view: CheckDefectFrame) -> None:
        self.model = model
        self.view = view
        self.setting = ConfigModel()

        self.simple_search_result = None
        self.simple_search_result_num = 0

        self.view.simple_search_pattern.trace_add("write", self._on_pattern_change)
        self.view.regex_is_on.trace_add("write", self._on_regex_changed)
        self.view.tabview_check.configure(command=self._on_checkview_tab_changed)
        self.view.tabview_result.configure(command=self._on_resultview_tab_changed)

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
            self.view.tabview_check.tab(name).grid_slaves(row=1, column=0)[0].focus_set()
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
        for _, tab in itertools.chain(
            self.view.tabview_check._tab_dict.items(),
            self.view.tabview_result._tab_dict.items(),
        ):
            for text_widget in tab.grid_slaves():
                if isinstance(text_widget, ctk.CTkTextbox):
                    text_widget.delete("1.0", "end")

    def check_defects(self) -> None:
        abstract_other_defects = self._get_selected_check_items("摘要及其他缺陷")
        claims_defects = self._get_selected_check_items("权利要求书缺陷")
        description_defects = self._get_selected_check_items("说明书及附图缺陷")
        print(abstract_other_defects, claims_defects, description_defects)
