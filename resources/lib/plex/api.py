from ..utils.settings import Settings

settings = Settings()


class PlexApi:
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
        
    def libraries(self):
        return {
            'url': '{}/library/sections/?X-Plex-Token={}'.format(self.pms_ip, self.pms_token),
            'method': 'get'
        }
    
    def library(self, lib_id):
        return {
            'url': '{}/library/sections/{}/all?X-Plex-Token={}'.format(self.pms_ip, lib_id, self.pms_token),
            'method': 'get'
        }
        
    def art(self, url):
        return '{}{}?X-Plex-Token={}'.format(self.pms_ip, url, self.pms_token)