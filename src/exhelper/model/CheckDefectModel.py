from . import SearchModel, ConfigModel
from .ClaimModel import ClaimModel
from .AbstractModel import AbstractModel
from .DescriptionModel import DescriptionModel

class CheckDefectModel:
    def __init__(self, setting: ConfigModel):
        self.search = SearchModel("")
        self.claim = ClaimModel("", setting)
        self.abstract = AbstractModel("", setting)
        self.description = DescriptionModel("", "", setting)
        

    