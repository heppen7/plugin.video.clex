import xbmc
import xbmcgui
import xbmcplugin

from .routing import Router
from .plex.signin import SignIn

routing = Router()

query = ['Konto', 'Odtwarzanie']

def run():
    routing.run()

@routing.route('/')
def index():
    li = xbmcgui.ListItem('Login')
    li2 = xbmcgui.ListItem('Ustawienia')
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(login), li, False)
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(settings, query=query), li2, True)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/login')
def login():
    SignIn().pin_asking()
    
@routing.route('/settings')
def settings(query):
    items = query
    for i in items:    
        li = xbmcgui.ListItem(i)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)