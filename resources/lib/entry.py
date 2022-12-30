import xbmc
import xbmcgui
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
        xbmc.log(f'{conn.get_playlists()}', level=1)
        # 
        li = xbmcgui.ListItem('Ustawienia')
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(manage, query=query), li, True)
        xbmcplugin.endOfDirectory(routing.handle)
    else:
        SignIn().signin()
    
@routing.route('/settings')
def manage(query):
    items = query
    for i in items:    
        li = xbmcgui.ListItem(i)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)