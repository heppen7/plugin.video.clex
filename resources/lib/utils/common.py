import xbmcaddon

from .config import CONFIG


class Common:
    
    def lang(self, id):
        return xbmcaddon.Addon(CONFIG["id"]).getLocalizedString(id)
    
    def merge_dict(self, dict1, dict2):
        dict2.update(dict1)
        return dict2