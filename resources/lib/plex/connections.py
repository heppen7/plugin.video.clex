import xbmc
import requests
import xml.etree.ElementTree as xml

from ..utils.config import plex_identification, plex_token, set_setting
from .plex_api import PlexApi
from ..super_info import Super_Info

session = requests.Session()

class Connections(PlexApi, Super_Info):
    def __init__(self) -> None:
        super().__init__()
        
    def _get(self, url, params=None, headers=None):
        return session.get(url, params=params, headers=headers)
    
    def _post(self, url, payload=None, headers=None):
        return session.post(url=url, data=payload, headers=headers)
    
    def request(self, method, url, headers=None, params=None, payload=None):
        if method == 'get':
            return self._get(url=url, params=params, headers=headers)
        elif method == 'post':
            return self._post(url=url, payload=payload, headers=headers)
    
    def merge_dict(self, dict1, dict2):
        dict2.update(dict1)
        return dict2
    
    def get_pms_res(self):
        heads = self.merge_dict(plex_identification(), plex_token())
        data = self.request(self.resources()['method'], self.resources()['url'], headers=heads)
        
        if data.status_code == 200:
            for resource in xml.fromstring(data.content):
                public_adress = resource.attrib.get('publicAddress')
                access_token = resource.attrib.get('accessToken')
                pms = [{'uri': c.attrib["uri"], 'token': access_token} for con in resource for c in con if c.attrib['address'] == public_adress]
                set_setting('pms_ip', pms[0]['uri'])
                set_setting('pms_token', pms[0]['token'])
                return pms
                            
    def get_playlists(self):
        data = self.request(self.playlists()['method'], self.playlists()['url'])
        xbmc.log(f'{data.content}', level=1)
        
    def get_libraries(self):
        libraries = []
        data = self.request(self.libraries()['method'], self.libraries()['url'])
        if data.status_code == 200:
            for directory in xml.fromstring(data.content):
                for location in directory:
                    libraries.append({'title': directory.attrib.get('title'), 'id': location.attrib.get('id')})
            return libraries
        
    def get_library(self, lib_id):
        data = self.request(self.library(lib_id)['method'], self.library(lib_id)['url'])
        if data.status_code == 200:
            return self.extract_info(data.content)
    
    def get_seasons(self, url):
        data = self.request('get', url)
        if data.status_code == 200:
            return self.extract_info(data.content)
    
    def get_episodes(self, url):
        data = self.request('get', url)
        if data.status_code == 200:
            return self.extract_info(data.content)