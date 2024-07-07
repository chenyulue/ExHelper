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
        self.view.tabview_check.configure(command=self._on_tab_changed)

    def _on_regex_changed(self, *args):
        self.simple_search_result = None
        self.simple_search_result_num = 0

    def _on_tab_changed(self) -> None:
        self.simple_search_result = None
        self.simple_search_result_num = 0

    def _on_pattern_change(self, *args) -> None:
        self.simple_search_result = None
        self.simple_search_result_num = 0
        
    def simple_search(self) -> None:
        top, _ = self.view.get_current_tabs()
        textbox = top.grid_slaves(column=0)[0]
        
        if textbox.edit_modified(): # type: ignore
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
            self._highlight_text(textbox, (start, end)) # type: ignore
            self.simple_search_result_num += 1
        except StopIteration:
            if self.simple_search_result_num:
                msg = CTkMessagebox(
                    self.view,
                    title="继续搜索？",
                    message="已搜索到该文档的末尾，从头继续搜索吗？",
                    icon="warning",
                    option_1="继续", option_2="取消",
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
                    option_1="好的"
                )
            
        textbox.edit_modified(False) # type: ignore

    def _highlight_text(self, textbox: ctk.CTkTextbox, index: tuple[int,int]):
        textbox.focus()
        textbox.tag_remove("sel", "1.0", "end")
        
        textbox.see(f"1.0+{index[0]}c")
        textbox.mark_set("insert", f"1.0+{index[1]}c")
        
        textbox.tag_add("sel", f"1.0+{index[0]}c", f"1.0+{index[1]}c")

