import xbmc
from xbmcgui import ListItem
import xbmcplugin

from .routing import Router
from .plex.account import Account
from .plex.connections import Connections

routing = Router()
conn = Connections()
account = Account()

query = ['Konto', 'Odtwarzanie']

def run():
    if not account.data():
        if account.signin():
            routing.redirect('/')
    else:
        routing.run()
        
@routing.route('/')
def index():
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(hubs), ListItem('Hub'), True)
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(genres), ListItem('Gatunki'), True)
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(libraries), ListItem('Biblioteka'), True)
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(manage, query=query), ListItem('Zarządzanie'), True)
    xbmcplugin.endOfDirectory(routing.handle)

@routing.route('/hubs')
def hubs():
    hubs = conn.get_hubs()
    for h in hubs:
        li = ListItem(h['hub_name'])
        if int(h['hub_size']) > 0:
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(hub, key=h['key']), li, True)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/hub')
def hub(key):
    videos = conn.get_hub(key[0])
    for video in videos[0]:
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
            if 'children' in video['key']:
                xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(metadata, url=video['key'], info=info), li, True)
            else:
                xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(metadata, url=video['key'], info=info), li)
        else:
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(play, url=video['file'], info=info), li)
    xbmcplugin.endOfDirectory(routing.handle)

@routing.route('/genres')
def genres():
    genres = conn.get_genres()
    for g in genres:
        li = ListItem(g['name'])
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(genre, key=g['key']), li, True)
    xbmcplugin.endOfDirectory(routing.handle)
       
@routing.route('/genre') 
def genre(key):
    titles = conn.get_genre(key)
    for video in titles:
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
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(play, url=video['file'], info=info), li)
    xbmcplugin.endOfDirectory(routing.handle)

@routing.route('/libraries')
def libraries():
    libraries = conn.get_libraries()
    for lib in libraries:
        li = ListItem(lib['title'])
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(library, id=lib['id']), li, True)
    xbmcplugin.endOfDirectory(routing.handle)
        
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
    season = None
    if isinstance(url, list):
        season = conn.get_episodes(url[0])
    else:
        season = conn.get_episodes(url)
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
        if s.get('key'):
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(episodes, url=s['key'], info=info), li, True)
        else:
            xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(play, url=s['file'], info=info), li)
    xbmcplugin.endOfDirectory(routing.handle)
    
    
@routing.route('/episodes')
def episodes(url, info):
    episode = None
    if isinstance(url, list):
        episode = conn.get_episodes(url[0])
    else:
        episode = conn.get_episodes(url)
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
    
@routing.route('/video')
def metadata(url, info):
    meta = conn.get_metadata(url[0])
    for m in meta:
        if 'children' in url[0]:
            if m[0].get('key'):
                if 'allLeaves' in m[0]['key']:
                    episodes(m[0]["key"], info)
            else:
               seasons(url[0], info)
        else:
            play(m[0]['file'], info)
    
@routing.route('/play')
def play(url, info):
    file = None
    if isinstance(url, list):
        file = url[0]
    else:
        file = url
    li = ListItem(info['title']) 
    li.setInfo('video', info)
    xbmc.Player().play(item=file, listitem=li)


@routing.route('/settings')
def manage(query):
    items = query
    for i in items:    
        li = ListItem(i)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)