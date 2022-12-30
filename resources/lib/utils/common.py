import xbmcaddon

from .config import CONFIG


class Common:
    def __init__(self) -> None:
        pass
    
    def lang(self, id):
        return xbmcaddon.Addon(CONFIG["id"]).getLocalizedString(id)
    
    def merge_dict(self, dict1, dict2):
        dict2.update(dict1)
        return dict2