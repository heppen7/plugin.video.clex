from xbmcgui import ListItem
import xbmcplugin
import xbmc

from .config import ADDON
from ..routing import Router

handle = Router().handle
    
    
class AddItem:
    def __enter__(self):
        return self
        
    def __exit__(self, *args, **kwargs):
        xbmcplugin.endOfDirectory(handle)
            
    def add(self, title, url, info=None, art=None, content=None, folder=True):
        listitem = ListItem(label=title)
        if info:
            listitem.setInfo('video', info)
        if art:
            listitem.setArt(art)
        else:
            art = {
                'icon': ADDON.getAddonInfo('icon'),
                'fanart': ADDON.getAddonInfo('fanart')
            }
            listitem.setArt(art)
        if content:
            xbmcplugin.setContent(handle, content)
        xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder=folder)
        
    def play(self, title, file, info):
        listitem = ListItem(label=title)
        listitem.setProperty('IsPlayable', 'true')
        if info:
            listitem.setInfo('video', info)
        xbmc.Player().play(item=file, listitem=listitem)