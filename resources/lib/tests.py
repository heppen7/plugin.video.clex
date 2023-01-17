import sys
from resources.lib.plex.connections import Connections
import cProfile


sys.path.insert(0, '')


conn = Connections()


def profiler(func):
    def wrapper(iterations):
        with cProfile.Profile() as pr:
            func(iterations)

            print(pr.print_stats())
    return wrapper


@profiler
def library(id):
    videos = conn.get_library(id)
    for video in videos:
        info = conn.meta_info(video)
        art = conn.meta_art(video)
        if video.get('key'):
            print(f'ListItem(title={info["title"]})')
        else:
            print(f'ListItem(title={info["title"]})')


library(1)
