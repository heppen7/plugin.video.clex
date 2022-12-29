import xbmc
import xbmcgui
import xbmcplugin

from .routing import Plugin

routing = Plugin()

query = {
    'user': 'test',
    'pass': 'mleko'
}

query_s = 'jakiś string przekazany dalej...'

def run():
    routing.run()

@routing.route('/')
def index():
    li = xbmcgui.ListItem('Login')
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(login, '/login', query=query, query_s=query_s), li, True)
    xbmcplugin.endOfDirectory(routing.handle)
    
@routing.route('/login')
def login(query, query_s):
    xbmc.log(f'{query, query_s}', level=1)
    li = xbmcgui.ListItem('Logout')
    xbmcplugin.addDirectoryItem(routing.handle, routing.url_for(index, '/'), li, True)
    xbmcplugin.endOfDirectory(routing.handle)