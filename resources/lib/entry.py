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
        li = ListItem(video['title'])
        li.setArt({
            'poster': video['poster'],
            'thumb': video['poster'],
            'fanart': video['fanart']
        })
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/settings')
def manage(query):
    items = query
    for i in items:    
        li = ListItem(i)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)