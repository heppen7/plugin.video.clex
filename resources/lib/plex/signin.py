import xbmc

from resources.lib.utils.headers import Headers
from resources.lib.utils.requests import Request
from .api import PlexApi

headers = Headers()
api = PlexApi()
s = Request() # session

class SignIn:
    def __init__(self) -> None:
        pass
    
    def pin_asking(self):
        sess = s.request(api.pins()['method'], api.pins()['url'], headers.plex_identification())
        xbmc.log(f'headers {sess.content}', level=1)