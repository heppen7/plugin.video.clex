class PlexApi:
    def __init__(self) -> None:
        self.base = 'https://plex.tv'
    
    def pins(self):
        return {
            'url': '{}/api/v2/pins'.format(self.base),
            'method': 'post'
        }