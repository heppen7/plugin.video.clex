import xbmcaddon
import xbmc
import json
import uuid
import platform

ID = 'plugin.video.clex'
ADDON = xbmcaddon.Addon(ID)


def get_settings():
    return ADDON.getSettings()


def get_setting(key):
    return ADDON.getSetting(key)


def set_setting(key, value):
    ADDON.setSetting(key, value)
    return get_setting(key)


CONFIG = {
    'id': ID,
    'addon': ADDON,
    'name': ADDON.getAddonInfo('name'),
    'icon': ADDON.getAddonInfo('icon'),
    'version': ADDON.getAddonInfo('version'),
    'movie': get_setting('movies'),
    'show': get_setting('tvshows'),
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
except Exception:
    CONFIG['language'] = 'en'


def lang(id):
    return ADDON.getLocalizedString(id)


windows = xbmc.getCondVisibility('system.platform.windows')
linux = xbmc.getCondVisibility('system.platform.linux')
android = xbmc.getCondVisibility('system.platform.android')
osx = xbmc.getCondVisibility('system.platform.osx')
atv = xbmc.getCondVisibility('system.platform.atv2')
tvos = xbmc.getCondVisibility('system.platform.tvos')
ios = xbmc.getCondVisibility('system.platform.ios')
rpi = xbmc.getCondVisibility('system.platform.raspberrypi')


def get_device():
    device = None

    if windows:
        device = 'Windows'

    if linux and not android:
        device = 'Linux'

    if osx:
        device = 'Darwin'

    if android:
        device = 'Android'

    if device is None:
        device = platform.system()

    return device


def get_platform():
    platform = 'Unknown'

    if osx:
        platform = 'MacOSX'
    if atv:
        platform = 'AppleTV2'
    if tvos:
        platform = 'tvOS'
    if ios:
        platform = 'iOS'
    if windows:
        platform = 'Windows'
    if rpi:
        platform = 'RaspberryPi'
    if linux:
        platform = 'Linux'
    if android:
        platform = 'Android'

    return platform


def client_id():
    return str(uuid.uuid4())


def return_client_id():
    if get_setting('client_id') != '':
        return get_setting('client_id')
    else:
        return set_setting('client_id', client_id())


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
