from ..utils.settings import Settings
from .connections import Connections

settings = Settings()

import xbmc

class PlexApi:
    def __init__(self) -> None:
        self.base_plex = 'https://plex.tv'
        xbmc.log(f'{Connections().get_resources()}', level=1)
        self.pms_ip = Connections().get_resources()[0]['uri']
        if settings.get_setting('access_token') == '':
            self.pms_token = None
        else:
            self.pms_token = settings.get_setting('access_token')
            
    
    # plex
    def pins(self):
        return {
            'url': '{}/api/v2/pins'.format(self.base_plex),
            'method': 'post'
        }
    
    def token(self, id):
        return {
            'url': '{}/api/v2/pins/{}'.format(self.base_plex, id),
            'method': 'get'
        }
    
    def signin(self):
        return {
            'url': '{}/api/v2/users/signin'.format(self.base_plex),
            'method': 'post'
        }
    
    def resources(self):
        return {
            'url': '{}/api/v2/resources'.format(self.base_plex),
            'method': 'get'
        }
        
    # pms
    def playlists(self):
        return {
            'url': '{}/playlists?X-Plex-Token={}'.format(self.pms_ip, self.pms_token),
            'method': 'get'
        }