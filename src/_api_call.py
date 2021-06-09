import requests
from config import Config as conf
from utils import fprint


def __SimpleRequest(url, headers={}, payload={}, params={}, method="GET"):
    try:
        response = requests.request(
            method, url, headers=headers, data=payload, params=params
        )
        return response.json()
    except Exception:
        pass


def SearchSongByName(query: str):
    url = "https://39b8f5ea-c383-416f-a7b6-03d8a88fd5a4.mock.pstmn.io/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": 25,
        "key": conf.API_KEY,
        "type": "video",
        "q": query,
    }
    result = __SimpleRequest(url=url, params=params)
    # result["items"][0]["id"]["videoId"]
    # result["items"][0]["snippet"]["title"]
    videos = []
    for video in result["items"]:
        videos.append((video["id"]["videoId"], video["snippet"]["title"]))
    return videos
