import xbmc
import xml.etree.ElementTree as xml

from ..utils.common import Common
from ..utils.headers import Headers
from ..utils.request import Request
from ..utils.settings import Settings
from .api import PlexApi

headers = Headers()
s = Request() # session
com = Common()
settings = Settings()

class Connections(PlexApi):
    def __init__(self) -> None:
        super(PlexApi).__init__()
        self.base_plex = 'https://plex.tv'
        self.pms_ip = self.get_resources()[0]['uri']
        if isinstance(self.pms_ip, str) and self.pms_ip != '':
            settings.set_setting('pms_ip', self.pms_ip)
        if settings.get_setting('access_token') == '':
            self.pms_token = None
        else:
            self.pms_token = settings.get_setting('access_token')
    
    def get_resources(self):
        heads = com.merge_dict(headers.plex_identification(), headers.plex_token())
        data = s.request(self.resources()['method'], self.resources()['url'], headers=heads)
        
        if data.status_code == 200:
            for resource in xml.fromstring(data.content):
                public_adress = resource.attrib.get('publicAddress')
                access_token = settings.set_setting('access_token', resource.attrib.get('accessToken'))
                return [{'uri': c.attrib["uri"], 'token': access_token} for con in resource for c in con if c.attrib['address'] == public_adress]
                            
    def get_playlists(self):
        data = s.request(self.playlists()['method'], self.playlists()['url'])
        xbmc.log(f'{data.content}', level=1)
        
    def get_libraries(self):
        libraries = []
        data = s.request(self.libraries()['method'], self.libraries()['url'])
        if data.status_code == 200:
            for directory in xml.fromstring(data.content):
                for location in directory:
                    libraries.append({'title': directory.attrib.get('title'), 'id': location.attrib.get('id')})
            return libraries
        
    def get_library(self, lib_id):
        videos = []
        data = s.request(self.library(lib_id)['method'], self.library(lib_id)['url'])
        if data.status_code == 200:
            for video in xml.fromstring(data.content):
                videos.append({
                    'title': video.attrib.get("title"),
                    'poster': self.art(video.attrib.get("thumb")),
                    'fanart': self.art(video.attrib.get("art"))
                })
            return videos