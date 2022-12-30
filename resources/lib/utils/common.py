import xbmcaddon

from .config import CONFIG


class Common:
    def __init__(self) -> None:
        pass
    
    def lang(self, id):
        return xbmcaddon.Addon(CONFIG["id"]).getLocalizedString(id)