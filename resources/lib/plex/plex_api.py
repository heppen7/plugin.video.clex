from ..utils.config import get_setting


class PlexApi:
    def __init__(self) -> None:
        self.base_plex = 'https://plex.tv'
        self.pms_ip = get_setting('pms_ip')
        self.pms_token = get_setting('pms_token')

    def metadata(self, url):
        return {
            'url': '{}'.format(url),
            'meth': 'get'
        }

    def pins(self):
        return {
            'url': '{}/api/v2/pins'.format(self.base_plex),
            'meth': 'post'
        }

    def token(self, id):
        return {
            'url': '{}/api/v2/pins/{}'.format(self.base_plex, id),
            'meth': 'get'
        }

    def signin(self):
        return {
            'url': '{}/api/v2/users/signin'.format(self.base_plex),
            'meth': 'post'
        }

    def resources(self):
        return {
            'url': '{}/api/v2/resources'.format(self.base_plex),
            'meth': 'get'
        }

    # pms
    def playlists(self):
        return {
            'url': '{}/playlists?X-Plex-Token={}'.format(
                self.pms_ip, self.pms_token),
            'meth': 'get'
        }

    def hubs(self):
        return {
            'url': '{}/hubs?X-Plex-Token={}'.format(
                self.pms_ip, self.pms_token),
            'meth': 'get'
        }

    def hub(self, hub_key):
        return {
            'url': '{}{}?X-Plex-Token={}'.format(
                self.pms_ip, hub_key, self.pms_token),
            'meth': 'get'
        }

    def genres(self):
        return {
            'url': '{}/library/sections/1/genre?X-Plex-Token={}'.format(
                self.pms_ip, self.pms_token),
            'meth': 'get'
        }

    def genre(self):
        return {
            'url': '{}/library/sections/1/all?X-Plex-Token={}'.format(
                self.pms_ip, self.pms_token),
            'meth': 'get'
        }

    def libraries(self):
        return {
            'url': '{}/library/sections/?X-Plex-Token={}'.format(
                self.pms_ip, self.pms_token),
            'meth': 'get'
        }

    def library(self, lib_id):
        return {
            'url': '{}/library/sections/{}/all?X-Plex-Token={}'.format(
                self.pms_ip, lib_id, self.pms_token),
            'meth': 'get'
        }

    def media(self, url):
        return '{}{}?X-Plex-Token={}'.format(self.pms_ip, url, self.pms_token)
