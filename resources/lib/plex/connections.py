import requests
import xml.etree.ElementTree as xml

from ..utils.config import plex_identification, plex_token
from ..utils.config import container_size, set_setting
from .plex_api import PlexApi
from ..super_info import Super_Info

session = requests.Session()


class Connections(PlexApi, Super_Info):
    def __init__(self) -> None:
        super().__init__()
        self.api_key = 'cf77b617e02513674bcac64abcf24702'

    def _get(self, url, params=None, headers=None):
        return session.get(url, params=params, headers=headers)

    def _post(self, url, payload=None, headers=None):
        return session.post(url=url, data=payload, headers=headers)

    def request(self, method, url, headers=None, params=None, payload=None):
        if method == 'get':
            return self._get(url=url, params=params, headers=headers)
        elif method == 'post':
            return self._post(url=url, payload=payload, headers=headers)

    def merge_dict(self, dict1, dict2):
        dict2.update(dict1)
        return dict2

    def get_pms_res(self):
        heads = self.merge_dict(plex_identification(), plex_token())
        data = self.request(self.resources()['meth'],
                            self.resources()['url'], headers=heads)

        if data.status_code == 200:
            for resource in xml.fromstring(data.content):
                public_adress = resource.attrib.get('publicAddress')
                access_token = resource.attrib.get('accessToken')
                pms = [{'uri': c.attrib["uri"], 'token': access_token}
                       for con in resource for c in con
                       if c.attrib['address'] == public_adress]
                set_setting('pms_ip', pms[0]['uri'])
                set_setting('pms_token', pms[0]['token'])
                return pms

    def get_playlists(self):
        # TODO: implement this...
        pass

    def get_hubs(self):
        params = container_size()
        data = self.request(self.hubs()['meth'], self.hubs()['url'],
                            params=params)
        if data.status_code == 200:
            return self.extract_info(data.content, 'mixed')

    def get_hub(self, hub_id):
        data = self.request(self.hub(hub_id)['meth'], self.hub(hub_id)['url'])
        if data.status_code == 200:
            return self.extract_info(data.content, 'hub')

    def get_metadata(self, url):
        data = self.request(self.metadata(url)['meth'],
                            self.metadata(url)['url'])
        if data.status_code == 200:
            return self.extract_info(data.content, 'metadata')

    def get_genres(self):
        genres = []
        data = self.request(self.genres()['meth'], self.genres()['url'])
        if data.status_code == 200:
            for directory in xml.fromstring(data.content):
                if directory.get('type') == 'genre':
                    genres.append({
                        'name': directory.attrib.get('title'),
                        'key': directory.attrib.get('key'),
                        'fast_key': directory.attrib.get('fastKey')
                    })
            return genres

    def get_genre(self, id):
        data = self.request(self.genre()['meth'], self.genre()['url'],
                            params={'genre': id})
        if data.status_code == 200:
            return self.extract_info(data.content)

    def get_libraries(self):
        libraries = []
        data = self.request(self.libraries()['meth'], self.libraries()['url'])
        if data.status_code == 200:
            for directory in xml.fromstring(data.content):
                dirtype = directory.attrib.get('type')
                for location in directory:
                    libraries.append({
                        'title': directory.attrib.get('title'),
                        'id': location.attrib.get('id'),
                        'type': dirtype
                    })
            return libraries

    def get_library(self, lib_id):
        data = self.request(self.library(lib_id)['meth'],
                            self.library(lib_id)['url'])
        if data.status_code == 200:
            return self.extract_info(data.content)

    def get_seasons(self, url):
        data = self.request('get', url)
        if data.status_code == 200:
            return self.extract_info(data.content)

    def get_episodes(self, url):
        data = self.request('get', url)
        if data.status_code == 200:
            return self.extract_info(data.content)

    def get_tmdb_movie_id(self, title, year):
        from datetime import datetime
        data = self.request('get', 'https://api.themoviedb.org/3/search/movie',
                            None, {'api_key': self.api_key,
                                   'query': title}).json()
        if data:
            for result in data['results']:
                release_date = datetime.strptime(
                    result['release_date'], '%Y-%m-%d').strftime('%Y')
                org_title = result['original_title']
                if title in org_title and int(year) == int(release_date):
                    return result['id']

    def get_tmdb_show_id(self, title, year):
        from datetime import datetime
        data = self.request('get', 'https://api.themoviedb.org/3/search/tv',
                            None, {'api_key': self.api_key,
                                   'query': title}).json()
        if data:
            for result in data['results']:
                air_year = datetime.strptime(
                    result['first_air_date'], '%Y-%m-%d').strftime('%Y')
                if title in result['name'] and int(year) == int(air_year):
                    return result['id']
