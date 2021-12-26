import requests


class YouTubeReader:
    def __init__(self, endpoint, key):
        self.key = key
        self.endpoint = endpoint

    def read_comments_by_id(self, video_id, comments_count):
        params = {'key': self.key, 'textFormat': 'plainText', 'part': 'snippet', 'video_id': video_id,
                  'maxResults': comments_count}
        r = requests.get(self.endpoint, params=params)
        data = r.json()
        result = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in data['items']]
        params["maxResults"] = int(params["maxResults"]) - int(data["pageInfo"]["resultsPerPage"])

        while "nextPageToken" in data and int(params["maxResults"]) > 0:
            params["pageToken"] = data["nextPageToken"]
            data = requests.get(self.endpoint, params=params).json()
            result += [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in data['items']]
            params["maxResults"] = int(params["maxResults"]) - int(data["pageInfo"]["resultsPerPage"])

        return result