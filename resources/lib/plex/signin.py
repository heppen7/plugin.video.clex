import xbmc
import xml.etree.ElementTree as xml

from ..utils.headers import Headers
from ..utils.request import Request
from ..utils.dialogs import Dialogs
from ..utils.settings import Settings
from .api import PlexApi

headers = Headers()
dialog = Dialogs()
settings = Settings()
s = Request() # session

class SignIn(object):
    def __init__(self) -> None:
        pass
    
    def pin_asking(self):
        data = s.request(PlexApi().pins()['method'], PlexApi().pins()['url'], headers=headers.plex_identification()).content
        for child in xml.fromstring(data):
            if child.attrib.get("status") == 400:
                xbmc.log(f'{data}', level=1) # TODO: log error 
            else:
                return {'id': xml.fromstring(data).attrib["id"], 'code': xml.fromstring(data).attrib["code"]}
    
    def token_asking(self, pin_id):
        data = s.request(PlexApi().token(pin_id)['method'], PlexApi().token(pin_id)['url'], headers=headers.plex_identification()).content
        for child in xml.fromstring(data):
            if child.attrib.get("status") == 400:
                xbmc.log(f'{data}', level=1) # TODO: log error 
            else:
                return xml.fromstring(data).attrib["authToken"]

    def signin(self):
        pin_code = self.pin_asking()
        if isinstance(pin_code, dict):
            if dialog.pin_code(pin_code['code']):
                token = self.token_asking(pin_code['id'])
                settings.set_setting('auth_token', token)