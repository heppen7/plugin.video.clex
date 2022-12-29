import xbmc
import uuid
import platform

from .settings import Settings

settings = Settings()


class Device:
    def __init__(self) -> None:
        pass
    
    def get_device(self):
        device = None
        if xbmc.getCondVisibility('system.platform.windows'):
            device = 'Windows'
        if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.android'):
            device = 'Linux'
        if xbmc.getCondVisibility('system.platform.osx'):
            device = 'Darwin'
        if xbmc.getCondVisibility('system.platform.android'):
            device = 'Android'
            
        if device is None:
            device = platform.system()
            
        return device

    def client_id(self):
        return str(uuid.uuid4())
    
    def return_client_id(self):
        if settings.get_setting('client_id') != '':
            return settings.get_setting('client_id')
        else:
            return settings.set_setting('client_id', self.client_id())

    def get_platform(self):
        platform = 'Unknown'

        if xbmc.getCondVisibility('system.platform.osx'):
            platform = 'MacOSX'
        if xbmc.getCondVisibility('system.platform.atv2'):
            platform = 'AppleTV2'
        if xbmc.getCondVisibility('system.platform.tvos'):
            platform = 'tvOS'
        if xbmc.getCondVisibility('system.platform.ios'):
            platform = 'iOS'
        if xbmc.getCondVisibility('system.platform.windows'):
            platform = 'Windows'
        if xbmc.getCondVisibility('system.platform.raspberrypi'):
            platform = 'RaspberryPi'
        if xbmc.getCondVisibility('system.platform.linux'):
            platform = 'Linux'
        if xbmc.getCondVisibility('system.platform.android'):
            platform = 'Android'

        return platform