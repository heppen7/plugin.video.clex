from ..plex.connections import Connections
from ..utils.dialogs import Dialogs
from ..utils.config import CONFIG
from ..routing import Router

import xbmc
import xbmcvfs
from xbmcgui import ListItem
from concurrent.futures import ThreadPoolExecutor

import xml.etree.ElementTree as xml
from datetime import datetime

router = Router()
dialog = Dialogs()
addon_id = CONFIG['id']


def _nfo(data):
    if data.get('rating'):
        rating = float(data.get('rating'))
    else:
        rating = 0
    if data.get('duration'):
        duration = int(int(data.get('duration'))/1000)
    else:
        duration = ''
    if data.get('added'):
        dateadded = int(data['added'])
        if isinstance(dateadded, int):
            dateadded = datetime.fromtimestamp(dateadded).strftime('%Y-%m-%d')
        else:
            dateadded = ''
    return {
        'child': [
            {'tag': 'title', 'value': data['title']},
            {'tag': 'plot', 'value': data['summary']},
            {'tag': 'outline', 'value': data['tagline']},
            {'tag': 'year', 'value': data['year']},
            {'tag': 'studio', 'value': data['studio']},
            {'tag': 'country', 'value': data['country'][0]},
            {'tag': 'genre', 'value': " / ".join(data['genre'])},
            {'tag': 'director', 'value': data['director'][0]},
            {'tag': 'userrating', 'value': rating},
            {'tag': 'duration', 'value': duration},
            {'tag': 'premiered', 'value': data['premiered']},
            {'tag': 'dateadded', 'value': dateadded}
        ],
        'video': [
            {'tag': 'codec', 'value': data['videoCodec']},
            {'tag': 'aspect', 'value': data['aspectRatio']},
            {'tag': 'width', 'value': data['width']},
            {'tag': 'height', 'value': data['height']},
            {'tag': 'durationinseconds', 'value': duration}
        ],
        'audio': [
            {'tag': 'codec', 'value': data['audioCodec']},
            {'tag': 'channels', 'value': data['audioChannels']}
        ],
        'thumbs':[
            {'aspect': 'poster', 'value': data['poster']},
            {'aspect': 'landscape', 'value': data['fanart']},
            {'aspect': 'fanart', 'value': data['fanart']}
        ]
    }


class Library(Connections):
    def __init__(self, lib_type) -> None:
        super().__init__()
        self.library_type = lib_type

    def options(self):
        libs = [l for l in self.get_libraries() if l['type'] == self.library_type]
        opts = []
        for l in libs:
            li = ListItem(l['title'], l['type'])
            opts.append(li)
        d = dialog.libraries(opts)
        if d:
            return self.indexes(d)
    
    def indexes(self, idx):
        libs = [l for l in self.get_libraries() if l['type'] == self.library_type]
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
        content = []
        for d in data:
            for n in d:
                content.append(n)
        return self.create_dir(content)
    
    def create_dir(self, content):
        path = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/")) + '/'
        if not xbmcvfs.exists(path):
            success = xbmcvfs.mkdir(path)
            if success:
                self.threading(content)
        else:
            self.threading(content)
            
    def create_strm(self, content):
        plugin_path = router.url_path("play", url=content["path"], info=content, library=True)
        dir = f'{xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))}/{content["title"]} {content["year"]}/'
        title = content['title'].replace(' ', '.')
        file = f'{dir}{title}.{content["year"]}.strm'
        if not xbmcvfs.exists(dir):
            success = xbmcvfs.mkdir(dir)
            if success:
                if not xbmcvfs.exists(file):
                    with xbmcvfs.File(file, 'w') as f:
                        f.write(plugin_path)
                else:
                    return True
        else:
            with xbmcvfs.File(file, 'w') as f:
                f.write(plugin_path)
                
    def create_nfo(self, content):
        dir = f'{xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))}/{content["title"]} {content["year"]}/'
        title = content['title'].replace(' ', '.')
        file = f'{dir}{title}.{content["year"]}.nfo'
        # root  
        root = xml.Element('movie')
        # child tags
        for child in _nfo(content)['child']:
            tag = xml.Element(child['tag'])
            tag.text = str(child['value'])
            root.append(tag)
        for child in _nfo(content)['thumbs']:
            tag = xml.Element('thumb')
            tag.attrib['aspect'] = child['aspect']
            tag.text = str(child['value'])
            root.append(tag)
        
        # video/audio tree
        fileinfo = xml.Element('fileinfo')
        root.append(fileinfo)
        streamdetails = xml.Element('streamdetails')
        fileinfo.append(streamdetails)
        video = xml.Element('video')
        streamdetails.append(video)
        audio = xml.Element('audio')
        streamdetails.append(audio)
        # video tag
        for v in _nfo(content)['video']:
            tag = xml.Element(v['tag'])
            tag.text = str(v['value'])
            video.append(tag)
        # audio tag
        for a in _nfo(content)['audio']:
            tag = xml.Element(a['tag'])
            tag.text = str(a['value'])
            audio.append(tag)
        
        
        tree = xml.ElementTree(root)
        xml.indent(tree, space="    ", level=0)
        
        if not xbmcvfs.exists(dir):
            success = xbmcvfs.mkdir(dir)
            if success:
                if not xbmcvfs.exists(file):
                    with xbmcvfs.File(file, 'w') as f:
                        tree.write(f, encoding='utf-8')
                else:
                    return True
        else:
            with xbmcvfs.File(file, 'w') as f:
                tree.write(f, encoding='utf-8')
                
    def threading(self, data):
        n_threads = len(data)
        processes = [self.create_strm, self.create_nfo]
        with ThreadPoolExecutor(n_threads) as executor:
            for p in processes:
                _ = executor.map(p, data)

