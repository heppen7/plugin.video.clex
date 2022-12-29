import requests


class Request:
    def __init__(self) -> None:
        self.session = requests.Session()
        
    def _get(self, url):
        return self.session.get(url)
    
    def _post(self, url, headers=None):
        return self.session.post(url, headers)
    
    def request(self, method, url, headers=None, params=None, payload=None):
        if method == 'get':
            return self._get(url)
        elif method == 'post':
            return self._post(url, headers)