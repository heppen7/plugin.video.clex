import xbmc
import xml.etree.ElementTree as xml

from ..utils.config import plex_identification
from ..utils.dialogs import Dialogs
from ..plex.connections import Connections
from ..utils.config import set_setting, get_setting

dialog = Dialogs()

class Account(Connections):
    def __init__(self) -> None:
        super().__init__()
    
    def pin_asking(self):
        data = self.request(self.pins()['method'], self.pins()['url'], headers=plex_identification()).content
        for child in xml.fromstring(data):
            if child.attrib.get("status") == 400:
                xbmc.log(f'{data}', level=1) # TODO: log error 
            else:
                return {'id': xml.fromstring(data).attrib["id"], 'code': xml.fromstring(data).attrib["code"]}
    
    def token_asking(self, pin_id):
        data = self.request(self.token(pin_id)['method'], self.token(pin_id)['url'], headers=plex_identification()).content
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
                set_setting('auth_token', token)
                return True

    def pms_data(self):
        ip = get_setting('pms_ip')
        token = get_setting('pms_token')
        
        if ip != '' and token != '':
            return True
        else:
            return False
        
    def data(self):
        client_id = get_setting('client_id')
        auth_token = get_setting('auth_token')
        
        if not self.pms_data():
            self.get_pms_res()
        else:
            if client_id != '' and auth_token != '':
                return True
            else:
                return False
            