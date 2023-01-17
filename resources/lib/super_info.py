import xml.etree.ElementTree as xml


class Super_Info:

    def meta_info(self, info):
        return {
            'mediatype': info.get("mediatype"),
            'title': info.get("title"),
            'originalTitle': info.get('originalTitle'),
            'summary': info.get('summary'),
            'tagline': info.get('tagline'),
            'year': info.get('year'),
            'studio': info.get('studio'),
            'country': info.get('country'),
            'genre': info.get('genre'),
            'director': info.get('director'),
            'writer': info.get('writer'),
            'cast': info.get('cast'),
            'rating': info.get('rating'),
            'userrating': info.get('userrating'),
            'duration': info.get('duration'),
            'premiered': info.get('premiered'),
            'bitrate': info.get('bitrate'),
            'width': info.get('width'),
            'height': info.get('height'),
            'aspectRatio': info.get('aspectRatio'),
            'audioChannels': info.get('audioChannels'),
            'audioCodec': info.get('audioCodec'),
            'videoCodec': info.get('videoCodec'),
            'videoResolution': info.get('videoResolution'),
            'videoFrameRate': info.get('videoFrameRate'),
            'videoProfile': info.get('videoProfile'),
            'poster': self.media(info.get("thumb")),
            'fanart': self.media(info.get("art")),
            'added':  info.get('added'),
            'path': self.media(info.get('key'))
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
        return [{
            'mediatype': video.attrib.get("type"),
            'title': video.attrib.get("title"),
            'originalTitle': video.attrib.get('originalTitle'),
            'summary': video.attrib.get('summary'),
            'tagline': video.attrib.get('tagline'),
            'year': video.attrib.get('year'),
            'studio': video.attrib.get('studio'),
            'country': [e.attrib.get('tag')
                        for e in video.findall('.//Country')],
            'genre': [e.attrib.get('tag') for e in video.findall('.//Genre')],
            'director': [e.attrib.get('tag')
                         for e in video.findall('.//Director')],
            'writer': [e.attrib.get('tag')
                       for e in video.findall('.//Writer')],
            'cast': [e.attrib.get('tag') for e in video.findall('.//Role')],
            'rating': video.attrib.get('rating'),
            'userrating': video.attrib.get('audienceRating'),
            'duration': video.attrib.get('duration'),
            'premiered': video.attrib.get('originallyAvailableAt'),
            'bitrate': media.attrib.get('bitrate'),
            'width': media.attrib.get('width'),
            'height': media.attrib.get('height'),
            'aspectRatio': media.attrib.get('aspectRatio'),
            'audioChannels': media.attrib.get('audioChannels'),
            'audioCodec': media.attrib.get('audioCodec'),
            'videoCodec': media.attrib.get('videoCodec'),
            'videoResolution': media.attrib.get('videoResolution'),
            'videoFrameRate': media.attrib.get('videoFrameRate'),
            'videoProfile': media.attrib.get('videoProfile'),
            'poster': self.media(video.attrib.get("thumb")),
            'fanart': self.media(video.attrib.get("art")),
            'added': video.attrib.get('updatedAt'),
            'path': self.media(part.attrib.get('key')),
            } for video in videos for media in video for part in media]

    def show(self, shows):
        return [{
            'mediatype': directory.attrib.get("type"),
            'title': directory.attrib.get("title"),
            'originalTitle': directory.attrib.get('originalTitle'),
            'summary': directory.attrib.get('summary'),
            'tagline': directory.attrib.get('tagline'),
            'year': directory.attrib.get('year'),
            'studio': directory.attrib.get('studio'),
            'country': [e.attrib.get('tag')
                        for e in directory.findall('.//Country')],
            'genre': [e.attrib.get('tag')
                      for e in directory.findall('.//Genre')],
            'director': [e.attrib.get('tag')
                         for e in directory.findall('.//Director')],
            'writer': [e.attrib.get('tag')
                       for e in directory.findall('.//Writer')],
            'cast': [e.attrib.get('tag')
                     for e in directory.findall('.//Role')],
            'rating': directory.attrib.get('rating'),
            'userrating': directory.attrib.get('audienceRating'),
            'duration': directory.attrib.get('duration'),
            'premiered': directory.attrib.get('originallyAvailableAt'),
            'bitrate': directory.attrib.get('bitrate'),
            'width': directory.attrib.get('width'),
            'height': directory.attrib.get('height'),
            'aspectRatio': directory.attrib.get('aspectRatio'),
            'audioChannels': directory.attrib.get('audioChannels'),
            'audioCodec': directory.attrib.get('audioCodec'),
            'videoCodec': directory.attrib.get('videoCodec'),
            'videoResolution': directory.attrib.get('videoResolution'),
            'videoFrameRate': directory.attrib.get('videoFrameRate'),
            'videoProfile': directory.attrib.get('videoProfile'),
            'poster': self.media(directory.attrib.get("thumb")),
            'fanart': self.media(directory.attrib.get("art")),
            'added': directory.attrib.get('updatedAt'),
            'key': self.media(directory.attrib.get('key')),
            } for directory in shows]

    def season(self, season):
        return [{
            'mediatype': directory.attrib.get("type"),
            'title': directory.attrib.get("title"),
            'summary': directory.attrib.get('summary'),
            'tagline': directory.attrib.get('tagline'),
            'year': directory.attrib.get('year'),
            'studio': directory.attrib.get('studio'),
            'country': [e.attrib.get('tag')
                        for e in directory.findall('.//Country')],
            'genre': [e.attrib.get('tag')
                      for e in directory.findall('.//Genre')],
            'director': [e.attrib.get('tag')
                         for e in directory.findall('.//Director')],
            'writer': [e.attrib.get('tag')
                       for e in directory.findall('.//Writer')],
            'cast': [e.attrib.get('tag')
                     for e in directory.findall('.//Role')],
            'rating': directory.attrib.get('rating'),
            'userrating': directory.attrib.get('audienceRating'),
            'duration': directory.attrib.get('duration'),
            'premiered': directory.attrib.get('originallyAvailableAt'),
            'bitrate': directory.attrib.get('bitrate'),
            'width': directory.attrib.get('width'),
            'height': directory.attrib.get('height'),
            'aspectRatio': directory.attrib.get('aspectRatio'),
            'audioChannels': directory.attrib.get('audioChannels'),
            'audioCodec': directory.attrib.get('audioCodec'),
            'videoCodec': directory.attrib.get('videoCodec'),
            'videoResolution': directory.attrib.get('videoResolution'),
            'videoFrameRate': directory.attrib.get('videoFrameRate'),
            'videoProfile': directory.attrib.get('videoProfile'),
            'poster': self.media(directory.attrib.get("thumb")),
            'fanart': self.media(directory.attrib.get("art")),
            'added': directory.attrib.get('updatedAt'),
            'key': self.media(directory.attrib.get('key')),
        } for directory in season]

    def episode(self, episode):
        return [{
            'mediatype': video.attrib.get("type"),
            'title': video.attrib.get("title"),
            'parentTitle': video.attrib.get('parentTitle'),
            'grandparentTitle': video.attrib.get('grandparentTitle'),
            'index': video.attrib.get('index'),
            'parentIndex': video.attrib.get('parentIndex'),
            'summary': video.attrib.get('summary'),
            'tagline': video.attrib.get('tagline'),
            'year': video.attrib.get('year'),
            'studio': video.attrib.get('studio'),
            'country': [e.attrib.get('tag')
                        for e in video.findall('.//Country')],
            'genre': [e.attrib.get('tag') for e in video.findall('.//Genre')],
            'director': [e.attrib.get('tag')
                         for e in video.findall('.//Director')],
            'writer': [e.attrib.get('tag')
                       for e in video.findall('.//Writer')],
            'cast': [e.attrib.get('tag') for e in video.findall('.//Role')],
            'rating': video.attrib.get('rating'),
            'userrating': video.attrib.get('audienceRating'),
            'duration': video.attrib.get('duration'),
            'premiered': video.attrib.get('originallyAvailableAt'),
            'bitrate': media.attrib.get('bitrate'),
            'width': media.attrib.get('width'),
            'height': media.attrib.get('height'),
            'aspectRatio': media.attrib.get('aspectRatio'),
            'audioChannels': media.attrib.get('audioChannels'),
            'audioCodec': media.attrib.get('audioCodec'),
            'videoCodec': media.attrib.get('videoCodec'),
            'videoResolution': media.attrib.get('videoResolution'),
            'videoFrameRate': media.attrib.get('videoFrameRate'),
            'videoProfile': media.attrib.get('videoProfile'),
            'poster': self.media(video.attrib.get("thumb")),
            'fanart': self.media(video.attrib.get("art")),
            'added': video.attrib.get('updatedAt'),
            'path': self.media(part.attrib.get('key')),
        } for video in episode for media in video for part in media]
