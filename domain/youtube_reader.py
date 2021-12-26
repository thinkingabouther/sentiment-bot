import requests


class YouTubeReader:
    def __init__(self, endpoint, key):
        self.key = key
        self.endpoint = endpoint

    def read_comments_by_id(self, video_id, max_comments):
        params = {'key': self.key, 'textFormat': 'plainText', 'part': 'snippet', 'video_id': video_id, 'maxResults': str(max_comments)}
        r = requests.get(self.endpoint, params=params)
        data = r.json()
        return [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in data['items']]