import xbmc
import xbmcgui
import xbmcplugin

from .routing import Plugin

routing = Plugin()

query = ['Konto', 'Odtwarzanie']
query_d = {
    'user': 'test',
    'pass': 'mleko'
}
query_s = 'jakiś string przekazany dalej...'

def run():
    routing.run()

@routing.route('/')
def index():
    li = xbmcgui.ListItem('Login')
    li2 = xbmcgui.ListItem('Ustawienia')
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(login), li, True)
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(settings, query=query), li2, True)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/login')
def login():
    li = xbmcgui.ListItem('Logout')
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/settings')
def settings(query):
    items = query
    for i in items:    
        li = xbmcgui.ListItem(i)
        xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index), li, True)
    xbmcplugin.endOfDirectory(routing.handle)