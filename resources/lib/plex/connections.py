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

class Connections:
    def __init__(self) -> None:
        pass
    
    def get_resources(self):
        heads = com.merge_dict(headers.plex_identification(), headers.plex_token())
        data = s.request(PlexApi().resources()['method'], PlexApi().resources()['url'], headers=heads)
        
        if data.status_code == 200:
            for resource in xml.fromstring(data.content):
                public_adress = resource.attrib.get('publicAddress')
                access_token = settings.set_setting('access_token', resource.attrib.get('accessToken'))
                return [{'uri': c.attrib["uri"], 'token': access_token} for con in resource for c in con if c.attrib['address'] == public_adress]
                            
    def get_playlists(self):
        data = s.request(PlexApi().playlists()['method'], PlexApi().playlists()['url'])
        xbmc.log(f'{data.content}', level=1)