from .utils.common import AddItem
from .routing import Router
from .plex.account import Account
from .plex.connections import Connections
from .utils.library import Library
from .utils.config import lang

routing = Router()
conn = Connections()
account = Account()


def run():
    if not account.data():
        if account.signin():
            routing.redirect('/')
    else:
        routing.run()


@routing.route('/')
def index():
    with AddItem() as item:
        item.add('Hub', routing.url_for(hubs))
        item.add('Gatunki', routing.url_for(genres))
        item.add('Biblioteka', routing.url_for(libraries))
        item.add('Zarządzaj Plex Media Server', routing.url_for(manage))


@routing.route('/hubs')
def hubs():
    hubs = conn.get_hubs()
    with AddItem() as item:
        for h in hubs:
            if int(h['hub_size']) > 0:
                item.add(h['hub_name'], routing.url_for(hub, key=h['key']))


@routing.route('/hub')
def hub(key):
    videos = conn.get_hub(key[0])
    with AddItem() as item:
        for video in videos[0]:
            info = conn.meta_info(video)
            art = conn.meta_art(video)
            if video.get('key'):
                if 'children' in video['key']:
                    url = routing.url_for(metadata, url=video['key'],
                                          info=info)
                    item.add(video['title'], url, info=info, art=art)
                else:
                    url = routing.url_for(metadata, url=video['key'],
                                          info=info)
                    item.add(video['title'], url, info=info, art=art,
                             folder=False)
            else:
                url = routing.url_for(play, url=video['path'], info=info)
                item.add(video['title'], url, info=info, art=art,
                         content='movies', folder=False)


@routing.route('/genres')
def genres():
    genres = conn.get_genres()
    with AddItem() as item:
        for g in genres:
            item.add(g['name'], routing.url_for(genre, key=g['key']))


@routing.route('/genre')
def genre(key):
    titles = conn.get_genre(key)
    with AddItem() as item:
        for video in titles:
            info = conn.meta_info(video)
            art = conn.meta_art(video)
            url = routing.url_for(play, url=video['path'], info=info)
            item.add(video['title'], url, info=info, art=art, content='movies',
                     folder=False)


@routing.route('/libraries')
def libraries():
    libraries = conn.get_libraries()
    with AddItem() as item:
        for lib in libraries:
            item.add(lib['title'], routing.url_for(library, id=lib['id']))


@routing.route('/library')
def library(id):
    videos = conn.get_library(id)
    with AddItem() as item:
        for video in videos:
            info = conn.meta_info(video)
            art = conn.meta_art(video)
            if video.get('key'):
                url = routing.url_for(seasons, url=video['key'], info=info)
                item.add(video['title'], url, info=info, art=art)
            else:
                url = routing.url_for(play, url=video['path'], info=info)
                item.add(video['title'], url, info=info, art=art,
                         content='movies', folder=False)


@routing.route('/seasons')
def seasons(url, info):
    season = None
    if isinstance(url, list):
        season = conn.get_episodes(url[0])
    else:
        season = conn.get_episodes(url)
    with AddItem() as item:
        for s in season:
            info = conn.meta_info(s)
            art = conn.meta_art(s)
            if s.get('key'):
                url = routing.url_for(episodes, url=s['key'], info=info)
                item.add(s['title'], url, info=info, art=art)
            else:
                url = routing.url_for(play, url=s['path'], info=info)
                item.add(s['title'], url, info=info, art=art, content='movies',
                         folder=False)


@routing.route('/episodes')
def episodes(url, info):
    episode = None
    if isinstance(url, list):
        episode = conn.get_episodes(url[0])
    else:
        episode = conn.get_episodes(url)
    with AddItem() as item:
        for e in episode:
            info = conn.meta_info(e)
            art = conn.meta_art(e)
            url = routing.url_for(play, url=e['path'], info=info)
            item.add(e['title'], url, info=info, art=art, content='movies',
                     folder=False)


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
            play(m[0]['path'], info)


@routing.route('/play')
def play(url, info, library=None):
    file = None
    if isinstance(url, list):
        file = url[0]
    else:
        file = url
    with AddItem() as item:
        if library is None:
            item.play(info['title'], file=file, info=info)
        else:
            item.play(info['title'], file=file, info=info, library=True)


@routing.route('/settings')
def manage():
    with AddItem() as item:
        item.add('Zaimportuj bibliotekę', routing.url_for(select_libs))


@routing.route('/select_libs')
def select_libs():
    with AddItem() as item:
        item.add(lang(32008), routing.url_for(import_movies), folder=False)
        item.add(lang(32009), routing.url_for(import_tvshows), folder=False)


@routing.route('/movies_importing')
def import_movies():
    Library('movie').options()


@routing.route('/tvshows_importing')
def import_tvshows():
    Library('show').options()
