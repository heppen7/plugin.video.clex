import sys
import xbmcaddon

from ast import literal_eval
from urllib.parse import urlsplit, urlencode, parse_qs


def make_path(*args):
    if args:
        url_args = args[0]
        return urlencode(url_args)

def parse_args(args):
    result = {}
    for k, v in args.items():
        try:
            result[k] = literal_eval(v[0])
        except:
            result[k] = v
    return result


class Router:
    def __init__(self, base=f'plugin://{xbmcaddon.Addon().getAddonInfo("id")}/') -> None:
        self._rules = {}
        self.args = {}
        if sys.argv:
            self.path = urlsplit(sys.argv[0] + sys.argv[2])
        if len(sys.argv) > 1 and sys.argv[1].isdigit():
            self.handle = int(sys.argv[1])
        else:
            self.handle = -1
        self.base_url = base
    
    def run(self):
        if len(sys.argv) > 2:
            self.args = parse_args(parse_qs(sys.argv[2].lstrip('?')))
        self.dispatch(self.args)
    
    def route(self, path, *args, **kwargs):
        def decorator(func):
            self.add_route(func, path, args, kwargs)
            return func
        return decorator
    
    def add_route(self, func, path, *args, **kwargs):
        self._rules.setdefault(path, []).append(func)
            
    def url_for(self, func, **kwargs):
        for path, funcs in self._rules.items():
            if func in funcs:
                return self.url_path(path, **kwargs)
    
    def url_path(self, path, *args, **kwargs):
        query = make_path(kwargs)
        return f"{self.base_url}{path}?{query}"
    
    def dispatch(self, *args):
        args = args[0]
        try:
            [func(**args) for func in self._rules[self.path.path]]
        except TypeError:
            [func() for func in self._rules[self.path.path]]
