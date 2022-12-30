import requests


class Request:
    def __init__(self) -> None:
        self.session = requests.Session()
        
    def _get(self, url, params=None, headers=None):
        return self.session.get(url, params=params, headers=headers)
    
    def _post(self, url, payload=None, headers=None):
        return self.session.post(url=url, data=payload, headers=headers)
    
    def request(self, method, url, headers=None, params=None, payload=None):
        if method == 'get':
            return self._get(url=url, params=params, headers=headers)
        elif method == 'post':
            return self._post(url=url, payload=payload, headers=headers)