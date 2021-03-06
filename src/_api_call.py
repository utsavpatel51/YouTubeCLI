import requests
from config import Config as conf
from rest_endpoint import RESTEndpoint
from utils import fprint, Video

def _simple_request(url, headers={}, payload={}, params={}, method="GET"):
    response = requests.request(
        method, url, headers=headers, data=payload, params=params
    )
    return response.status_code, response.json()


def SearchSongByName(query: str):
    url = "https://{}{}".format(RESTEndpoint.BASE_URL, RESTEndpoint.SEARCH_ENDPOINT)
    params = {
        "part": "snippet",
        "maxResults": 25,
        "key": conf.API_KEY,
        "type": "video",
        "q": query.strip(),
    }
    status, result = _simple_request(url=url, params=params)
    if status == 200:
        videos = [
            Video(video["id"]["videoId"], video["snippet"]["title"])
            for video in result["items"]
        ]
        return videos
    else:
        fprint("<invalid>{}</invalid>".format(result["error"]["message"]))
        return []
