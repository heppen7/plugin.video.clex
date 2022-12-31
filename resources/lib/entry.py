import xbmc
from xbmcgui import ListItem
import xbmcplugin

from .routing import Router
from .utils.settings import Settings
from .plex.signin import SignIn
from .plex.connections import Connections

routing = Router()
settings = Settings()
conn = Connections()

query = ['Konto', 'Odtwarzanie']

def run():
    routing.run()

@routing.route('/')
def index():
    if isinstance(settings.get_setting('auth_token'), str) and settings.get_setting('auth_token') != '':
        libraries = conn.get_libraries()
        for lib in libraries:
            li = ListItem(lib['title'])
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(library, id=lib['id']), li, True)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(manage, query=query), ListItem('Zarządzanie'), True)
        xbmcplugin.endOfDirectory(routing.handle)
    else:
        SignIn().signin()
        
@routing.route('/library')
def library(id):
    videos = conn.get_library(id)
    for video in videos:
        info = {
            'title': video['title'],
            'plot': video['summary'],
            'plotoutline': video['tagline']
        }
        art = {
            'poster': video['poster'],
            'thumb': video['poster'],
            'fanart': video['fanart']
        }
        li = ListItem(video['title'])
        li.setInfo('video', info)
        li.setArt(art)
        if video.get('key'):
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(seasons, url=video['key'], info=info), li, True)
        else:
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(play, url=video['file'], info=info), li)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/seasons')
def seasons(url, info):
    season = conn.get_seasons(url[0])
    for s in season:
        info = {
            'title': s['title'],
            'plot': s['summary']
        }
        art = {
            'poster': s['poster'],
            'thumb': s['poster'],
            'fanart': s['fanart']
        }
        li = ListItem(s['title'])
        li.setInfo('video', info)
        li.setArt(art)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(episodes, url=s['key'], info=info), li, True)
    xbmcplugin.endOfDirectory(routing.handle)
    
    
@routing.route('/episodes')
def episodes(url, info):
    episode = conn.get_episodes(url[0])
    for e in episode:
        info = {
            'title': e['title'],
            'plot': e['summary']
        }
        art = {
            'poster': e['poster'],
            'thumb': e['poster'],
            'fanart': e['fanart']
        }
        li = ListItem(e['title'])
        li.setInfo('video', info)
        li.setArt(art)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(play, url=e['file'], info=info), li)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/play')
def play(url, info):
    li = ListItem(info['title']) 
    li.setInfo('video', info)
    xbmc.Player().play(item=url[0], listitem=li)


@routing.route('/settings')
def manage(query):
    items = query
    for i in items:    
        li = ListItem(i)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)