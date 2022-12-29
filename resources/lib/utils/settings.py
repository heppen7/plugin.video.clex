import xbmcaddon

from .config import CONFIG


class Settings:
    def __init__(self) -> None:
        self.settings = xbmcaddon.Addon(CONFIG['id'])
    
    def get_settings(self):
        return self.settings.getSettings()
    
    def get_setting(self, key):
        return self.settings.getSetting(key)
    
    def set_setting(self, key, value):
        self.settings.setSetting(key, value)
        return self.get_setting(key)