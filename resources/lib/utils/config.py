import xbmcaddon
import xbmc
import json

ID = 'plugin.video.clex'
ADDON = xbmcaddon.Addon(ID)

CONFIG = {
    'id': ID,
    'addon': ADDON,
    'name': ADDON.getAddonInfo('name'),
    'icon': ADDON.getAddonInfo('icon'),
    'version': ADDON.getAddonInfo('version')
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