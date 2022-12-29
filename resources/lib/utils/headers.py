import platform

from .config import CONFIG
from .device import Device

device = Device()


class Headers:
    def __init__(self) -> None:
        self.headers = {}
        
    def plex_identification(self):
        return {
            'X-Plex-Device': device.get_device(),
            'X-Plex-Client-Platform': 'Kodi',
            'X-Plex-Device-Name': CONFIG['name'],
            'X-Plex-Language': CONFIG['language'],
            'X-Plex-Platform': device.get_platform(),
            'X-Plex-Product': CONFIG['name'],
            'X-Plex-Client-Identifier': device.return_client_id(),
            'X-Plex-Platform-Version': platform.uname()[2],
            'X-Plex-Version': CONFIG['version'],
            'X-Plex-Provides': 'player,controller'
        }