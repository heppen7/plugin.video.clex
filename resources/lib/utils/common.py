from xbmcgui import ListItem
import xbmcplugin
import xbmc
from datetime import datetime

from .config import ADDON
from ..routing import Router

handle = Router().handle
    
    
class AddItem:
    def __enter__(self):
        return self
        
    def __exit__(self, *args, **kwargs):
        xbmcplugin.endOfDirectory(handle)
        
    def _setinfo(self, listitem, info):
        videoinfo = listitem.getVideoInfoTag()
        if info.get('cast'):
            actors = [xbmc.Actor(a) for a in info['cast']]
            videoinfo.setCast(actors)
        if info.get('mediatype'):
            videoinfo.setMediaType(info['mediatype'])
        if info.get('title'):
            videoinfo.setTitle(info['title'])
        if info.get('summary'):
            videoinfo.setPlot(info['summary'])
        if info.get('tagline'):
            videoinfo.setPlotOutline(info['tagline'])
        if info.get('year'):
            videoinfo.setYear(int(info['year']))
        if info.get('studio'):
            videoinfo.setStudios([info['studio']])
        if info.get('country'):
            videoinfo.setCountries(info['country'])
        if info.get('genre'):
            videoinfo.setGenres(info['genre'])
        if info.get('director'):
            videoinfo.setDirectors(info['director'])
        if info.get('writer'):
            videoinfo.setWriters(info['writer'])
        if info.get('rating'):
            rating = float(info.get('rating')) if info.get('rating') else 0
            videoinfo.setRating(rating)
        if info.get('userrating'):
            userrating = int(float(info.get('userrating'))) if info.get('userrating') else 0
            videoinfo.setUserRating(userrating)
        if info.get('duration'):
            duration = int(int(info.get('duration'))/1000) if info.get('duration') else None
            videoinfo.setDuration(duration)
        if info.get('premiered'):
            videoinfo.setPremiered(info['premiered'])
        if info.get('added'):
            dateadded = int(info['added'])
            dateadded = datetime.fromtimestamp(dateadded).strftime('%Y-%m-%d') if isinstance(dateadded, int) else ''
            videoinfo.setDateAdded(dateadded)
        return listitem
            
    def add(self, title, url, info=None, art=None, content=None, folder=True):
        listitem = ListItem(label=title)
        if info:
            listitem = self._setinfo(listitem, info)
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
            listitem = self._setinfo(listitem, info)
        if library is None:
            xbmc.Player().play(item=file, listitem=listitem)
        else:
            xbmcplugin.setResolvedUrl(handle, True, listitem)