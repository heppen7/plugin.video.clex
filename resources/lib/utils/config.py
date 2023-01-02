import xbmcaddon
import xbmc
import json
import uuid
import platform

ID = 'plugin.video.clex'
ADDON = xbmcaddon.Addon(ID)

CONFIG = {
    'id': ID,
    'addon': ADDON,
    'name': ADDON.getAddonInfo('name'),
    'icon': ADDON.getAddonInfo('icon'),
    'version': ADDON.getAddonInfo('version'),
    'movies_path': ADDON.getAddonInfo('profile') + 'movies',
    'shows_path': ADDON.getAddonInfo('profile') + 'tvshows',
}

try:
    command = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Application.GetProperties",
        "params": {
            "properties": ["language"]
        }
    }

    rpc = json.loads(xbmc.executeJSONRPC(json.dumps(command)))
    CONFIG['language'] = rpc.get('result').get('language').split('_')[0]
except:
    CONFIG['language'] = 'en'

def lang(id):
    return ADDON.getLocalizedString(id)

def get_settings():
    return ADDON.getSettings()

def get_setting(key):
    return ADDON.getSetting(key)

def set_setting(key, value):
    ADDON.setSetting(key, value)
    return get_setting(key)

def get_device():
    device = None
    if xbmc.getCondVisibility('system.platform.windows'):
        device = 'Windows'
    if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.android'):
        device = 'Linux'
    if xbmc.getCondVisibility('system.platform.osx'):
        device = 'Darwin'
    if xbmc.getCondVisibility('system.platform.android'):
        device = 'Android'
        
    if device is None:
        device = platform.system()
        
    return device

def client_id():
    return str(uuid.uuid4())

def return_client_id():
    if get_setting('client_id') != '':
        return get_setting('client_id')
    else:
        return set_setting('client_id', client_id())

def get_platform():
    platform = 'Unknown'

    if xbmc.getCondVisibility('system.platform.osx'):
        platform = 'MacOSX'
    if xbmc.getCondVisibility('system.platform.atv2'):
        platform = 'AppleTV2'
    if xbmc.getCondVisibility('system.platform.tvos'):
        platform = 'tvOS'
    if xbmc.getCondVisibility('system.platform.ios'):
        platform = 'iOS'
    if xbmc.getCondVisibility('system.platform.windows'):
        platform = 'Windows'
    if xbmc.getCondVisibility('system.platform.raspberrypi'):
        platform = 'RaspberryPi'
    if xbmc.getCondVisibility('system.platform.linux'):
        platform = 'Linux'
    if xbmc.getCondVisibility('system.platform.android'):
        platform = 'Android'

    return platform

def plex_identification():
    return {
        'X-Plex-Device': get_device(),
        'X-Plex-Client-Platform': 'Kodi',
        'X-Plex-Device-Name': CONFIG['name'],
        'X-Plex-Language': CONFIG['language'],
        'X-Plex-Platform': get_platform(),
        'X-Plex-Product': CONFIG['name'],
        'X-Plex-Client-Identifier': return_client_id(),
        'X-Plex-Platform-Version': platform.uname()[2],
        'X-Plex-Version': CONFIG['version'],
        'X-Plex-Provides': 'player,controller'
    }
    
def plex_token():
    return {
        'X-Plex-Token': get_setting('auth_token')
    }
    
def container_size():
    return {
        'count': 40
    }