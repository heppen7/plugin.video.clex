import xml.etree.ElementTree as xml

class Super_Info:
    
    def meta_info(self, info):
        return {
            'title': info.get('title'),
            'plot': info.get('summary'),
            'plotoutline': info.get('tagline')
        }
    
    def meta_art(self, art):
        return {
            'poster': art.get('poster'),
            'thumb': art.get('poster'),
            'fanart': art.get('fanart')
        }
    
    def extract_info(self, data, view_group=None):
        group = xml.fromstring(data)
        if view_group == 'mixed':
            return self._hubs(xml.fromstring(data))
        if view_group == 'hub' or view_group == 'metadata':
            return self._metadata(xml.fromstring(data))
        if group.attrib.get('viewGroup') == 'movie':
            return self.movie(xml.fromstring(data))
        elif group.attrib.get('viewGroup') == 'show':
            return self.show(xml.fromstring(data))
        elif group.attrib.get('viewGroup') == 'season':
            return self.season(xml.fromstring(data))
        elif group.attrib.get('viewGroup') == 'episode':
            return self.episode(xml.fromstring(data))
            
    def _hubs(self, data):
        hubs = []
        for hub in data:
            hubs.append({
                'hub_name': hub.attrib.get('title'),
                'key': hub.attrib.get('hubKey'),
                'hub_size': hub.attrib.get('size')
            })
        return hubs
            
    def _metadata(self, videos):
        info = []
        for video in videos:
            if video.attrib.get('type') == 'movie':
                info.append(self.movie(videos))
            elif video.attrib.get('type') == 'show':
                info.append(self.show(videos))
            elif video.attrib.get('type') == 'season':
                info.append(self.season(videos))
            elif video.attrib.get('type') == 'episode':
                info.append(self.episode(videos))
        return info
    
    def movie(self, videos):
        info = []
        file = None
        for video in videos:
            for media in video:
                for part in media:
                    file = part.attrib.get('key')
            info.append({
                'title': video.attrib.get("title"),
                'summary': video.attrib.get('summary'),
                'tagline': video.attrib.get('tagline'),
                'poster': self.media(video.attrib.get("thumb")),
                'fanart': self.media(video.attrib.get("art")),
                'file': self.media(file)
            })
        return info
    
    def show(self, shows):
        info = []
        for directory in shows:
            info.append({
                'title': directory.attrib.get("title"),
                'summary': directory.attrib.get('summary'),
                'tagline': directory.attrib.get('tagline'),
                'poster': self.media(directory.attrib.get("thumb")),
                'fanart': self.media(directory.attrib.get("art")),
                'key': self.media(directory.attrib.get("key"))
            })
        return info

    def season(self, season):
        info = []
        for directory in season:
            info.append({
                'title': directory.attrib.get("title"),
                'summary': directory.attrib.get('summary'),
                'poster': self.media(directory.attrib.get("thumb")),
                'fanart': self.media(directory.attrib.get("art")),
                'key': self.media(directory.attrib.get("key"))
            })
        return info

    def episode(self, episode):
        info = []
        file = None
        for video in episode:
            for media in video:
                for part in media:
                    file = part.attrib.get('key')
            info.append({
                'title': video.attrib.get("title"),
                'summary': video.attrib.get('summary'),
                'tagline': video.attrib.get('tagline'),
                'poster': self.media(video.attrib.get("thumb")),
                'fanart': self.media(video.attrib.get("art")),
                'file': self.media(file)
            })
        return info