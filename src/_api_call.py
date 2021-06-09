import requests
from config import Config as conf
from utils import fprint
from rest_endpoint import RESTEndpoint


def __SimpleRequest(url, headers={}, payload={}, params={}, method="GET"):
    try:
        response = requests.request(
            method, url, headers=headers, data=payload, params=params
        )
        return response.json()
    except Exception:
        pass


def SearchSongByName(query: str):
    url = "https://{}{}".format(RESTEndpoint.BASE_URL, RESTEndpoint.SEARCH_ENDPOINT)
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
