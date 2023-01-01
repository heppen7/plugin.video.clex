from contextlib import contextmanager
from xbmcgui import ListItem
import xbmcplugin

from .config import ADDON
from ..routing import Router

handle = Router().handle
    
    
class AddItem:
    def __enter__(self):
        return self
        
    def __exit__(self, *args, **kwargs):
        xbmcplugin.endOfDirectory(handle)
            
    def add(self, title, url, playable=False, info=None, art=None, content=None, folder=True):
        list_item = ListItem(label=title)
        if playable:
            list_item.setProperty('IsPlayable', 'true')
            folder = False
        if art:
            list_item.setArt(art)
        else:
            art = {
                'icon': ADDON.getAddonInfo('icon'),
                'fanart': ADDON.getAddonInfo('fanart')
            }
            list_item.setArt(art)
        if info:
            list_item.setInfo('video', info)
        if content:
            xbmcplugin.setContent(handle, content)
        xbmcplugin.addDirectoryItem(handle, url, list_item, isFolder=folder)