from ..plex.connections import Connections
from ..utils.dialogs import Dialogs
from ..utils.config import CONFIG
from ..routing import Router

import xbmcvfs
from xbmcgui import ListItem
from concurrent.futures import ThreadPoolExecutor

router = Router()
dialog = Dialogs()
addon_id = CONFIG['id']


class Library(Connections):
    def __init__(self, lib_type) -> None:
        super().__init__()
        self.library_type = lib_type

    def write_nfo(self, dir, file, id):
        buffer = None
        if self.library_type == 'movie':
            buffer = 'https://www.themoviedb.org/movie/' + id
        else:
            buffer = 'https://www.themoviedb.org/tv/' + id
        if not xbmcvfs.exists(dir):
            success = xbmcvfs.mkdir(dir)
            if success:
                if not xbmcvfs.exists(file):
                    with xbmcvfs.File(file, 'w') as f:
                        f.write(buffer)
                else:
                    return True
        else:
            with xbmcvfs.File(file, 'w') as f:
                f.write(buffer)

    def options(self):
        libs = [lib for lib in self.get_libraries()
                if lib['type'] == self.library_type]
        opts = []
        for lib in libs:
            li = ListItem(lib['title'], lib['type'])
            opts.append(li)
        d = dialog.libraries(opts)
        if d:
            return self.indexes(d)

    def indexes(self, idx):
        libs = [lib for lib in self.get_libraries()
                if lib['type'] == self.library_type]
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
        path = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))
        path = f'{path}/'
        if not xbmcvfs.exists(path):
            success = xbmcvfs.mkdir(path)
            if success:
                if self.library_type == 'movie':
                    self.movie_threading(content)
                else:
                    self.shows_threading(content)
        else:
            if self.library_type == 'movie':
                self.movie_threading(content)
            else:
                self.shows_threading(content)

    def create_movie_strm(self, content):
        plugin_path = router.url_path("play", url=content["path"],
                                      info=content, library=True)
        path = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))
        dir = f'{path}/{content["title"]} ({content["year"]})/'
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

    def create_shows_dirs(self, content):
        path = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))
        dir = f'{path}/{content["title"]} ({content["year"]})/'
        seasons = self.get_seasons(content['key'])
        for season in seasons:
            path = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))
            season = season["title"]
            s_dir = f'{path}/{content["title"]} ({content["year"]})/{season}/'
            if not xbmcvfs.exists(dir):
                success = xbmcvfs.mkdir(dir)
                if success:
                    if not xbmcvfs.exists(s_dir):
                        success = xbmcvfs.mkdir(s_dir)
                        if success:
                            self.create_shows_strm(s_dir, season['key'])
                    else:
                        return True
            else:
                self.create_shows_strm(s_dir, season['key'])

    def create_shows_strm(self, s_dir, key):
        episodes = self.get_episodes(key)
        for episode in episodes:
            plugin_path = router.url_path("play", url=episode["path"],
                                          info=episode, library=True)
            title = episode['grandparentTitle'].replace(' ', '.')
            s = f'{int(episode["parentIndex"]):02}'
            e = f'{int(episode["index"]):02}'
            file = f'{s_dir}{title}.S{s}E{e}.strm'
            if not xbmcvfs.exists(s_dir):
                success = xbmcvfs.mkdir(s_dir)
                if success:
                    if not xbmcvfs.exists(file):
                        with xbmcvfs.File(file, 'w') as f:
                            f.write(plugin_path)
                    else:
                        return True
            else:
                with xbmcvfs.File(file, 'w') as f:
                    f.write(plugin_path)

    def create_show_nfo(self, content):
        base = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))
        base_dir = f'{base}/{content["title"]} ({content["year"]})/'
        file = f'{base_dir}tvshow.nfo'

        self.write_nfo(base_dir, file,
                       str(self.get_tmdb_show_id(content['title'],
                                                 content['year'])))

    def create_movie_nfo(self, content):
        base = xbmcvfs.translatePath(CONFIG[self.library_type].rstrip("/"))
        base_dir = f'{base}/{content["title"]} ({content["year"]})/'
        title = content['title'].replace(' ', '.')
        file = f'{base_dir}{title}.{content["year"]}.nfo'

        self.write_nfo(base_dir, file,
                       str(self.get_tmdb_movie_id(
                           content['originalTitle'], content['year'])))

    def movie_threading(self, data):
        n_threads = len(data)
        processes = [self.create_movie_strm, self.create_movie_nfo]
        with ThreadPoolExecutor(n_threads) as executor:
            for p in processes:
                _ = executor.map(p, data)

    def shows_threading(self, data):
        n_threads = len(data)
        processes = [self.create_shows_dirs,
                     self.create_shows_strm,
                     self.create_show_nfo]
        with ThreadPoolExecutor(n_threads) as executor:
            for p in processes:
                _ = executor.map(p, data)
