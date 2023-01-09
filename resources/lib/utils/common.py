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
            videoinfo = listitem.getVideoInfoTag()
            actors = [xbmc.Actor(a) for a in info['cast']]
            if info.get('mediatype'):
                videoinfo.setMediaType(info['mediatype'])
            videoinfo.setTitle(info['title'])
            videoinfo.setPlot(info['summary'])
            videoinfo.setPlotOutline(info['tagline'])
            if info.get('year'):
                videoinfo.setYear(info['year'])
            videoinfo.setStudios([info['studio']])
            videoinfo.setCountries(info['country'])
            videoinfo.setGenres(info['genre'])
            videoinfo.setDirectors(info['director'])
            videoinfo.setWriters(info['writer'])
            videoinfo.setCast(actors)
            videoinfo.setRating(info['rating'])
            videoinfo.setUserRating(info['userrating'])
            if info.get('duration'):
                videoinfo.setDuration(info['duration'])
            videoinfo.setPremiered(info['premiered'])
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
        
    def play(self, title, file, info, library=None):
        listitem = ListItem(label=title, path=file)
        listitem.setProperty('IsPlayable', 'true')
        if info:
            videoinfo = listitem.getVideoInfoTag()
            actors = [xbmc.Actor(a) for a in info['cast']]
            if info.get('mediatype'):
                videoinfo.setMediaType(info['mediatype'])
            videoinfo.setTitle(info['title'])
            videoinfo.setPlot(info['summary'])
            videoinfo.setPlotOutline(info['tagline'])
            if info.get('year'):
                videoinfo.setYear(info['year'])
            videoinfo.setStudios([info['studio']])
            videoinfo.setCountries(info['country'])
            videoinfo.setGenres(info['genre'])
            videoinfo.setDirectors(info['director'])
            videoinfo.setWriters(info['writer'])
            videoinfo.setCast(actors)
            videoinfo.setRating(info['rating'])
            videoinfo.setUserRating(info['userrating'])
            if info.get('duration'):
                videoinfo.setDuration(info['duration'])
            videoinfo.setPremiered(info['premiered'])
        if library is None:
            xbmc.Player().play(item=file, listitem=listitem)
        else:
            xbmcplugin.setResolvedUrl(handle, True, listitem)