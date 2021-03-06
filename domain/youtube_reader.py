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
        params["maxResults"] = int(params["maxResults"]) - int(data["pageInfo"]["totalResults"])

        while "nextPageToken" in data and len(result) < int(comments_count) and int(params["maxResults"])>0:
            params["pageToken"] = data["nextPageToken"]
            data = requests.get(self.endpoint, params=params).json()
            result += [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in data['items']]
            params["maxResults"] = max(0,int(params["maxResults"]) - int(data["pageInfo"]["totalResults"]))

        return result