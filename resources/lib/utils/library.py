from ..plex.connections import Connections
from ..utils.dialogs import Dialogs
from ..utils.config import CONFIG
from ..routing import Router

import xbmc
import xbmcvfs
from xbmcgui import ListItem
from concurrent.futures import ThreadPoolExecutor

import xml.etree.ElementTree as xml

router = Router()
dialog = Dialogs()
addon_id = CONFIG['id']


class Library(Connections):
    def __init__(self) -> None:
        super().__init__()

    def options(self, type):
        libs = [l for l in self.get_libraries() if l['type'] == type]
        opts = []
        for l in libs:
            li = ListItem(l['title'], l['type'])
            opts.append(li)
        d = dialog.libraries(opts)
        if d:
            return self.indexes(d, type)
    
    def indexes(self, idx, type):
        libs = [l for l in self.get_libraries() if l['type'] == type]
        opts = []
        for i in idx:
            opts.append(libs[i])
        return self.concurrent(opts)
    
    def concurrent(self, opts):
        titles = []
        id_map = []
        
        for o in opts:
            id_map.append(o['id'])
            
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.get_library, id_map)
            for result in results:
                titles.append(result)

        return self.construct_urls(titles)
    
    def construct_urls(self, data):
        urls = []
        for d in data:
            for n in d:
                urls.append(n)
 
        return self.create_strm_dir(urls)
    
    def construct_strm(self, content):
        for c in content:
            plugin_path = router.url_path("play", url=c["file"], info={'title': c['title']}, library=True)
            self.create_strm(c['title'], c['year'], plugin_path)
    
    def create_strm_dir(self, urls):
        path = xbmcvfs.translatePath(CONFIG["movies"]) + '/'
        if not xbmcvfs.exists(path):
            success = xbmcvfs.mkdir(path)
            if success:
                self.construct_strm(urls)
        else:
            self.construct_strm(urls)
            
    def create_strm(self, title, year, content):
        dir = f'{xbmcvfs.translatePath(CONFIG["movies"].rstrip("/"))}/{title} {year}/'
        title = title.replace(' ', '.')
        file = f'{dir}{title}.{year}.strm'
        if not xbmcvfs.exists(dir):
            success = xbmcvfs.mkdir(dir)
            if success:
                if not xbmcvfs.exists(file):
                    with xbmcvfs.File(file, 'w') as f:
                        f.write(content)
                else:
                    return True
        else:
            with xbmcvfs.File(file, 'w') as f:
                f.write(content)
        