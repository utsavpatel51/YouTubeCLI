import requests
from config import Config as conf
from rest_endpoint import RESTEndpoint


def _simple_request(url, headers={}, payload={}, params={}, method="GET"):
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
        "q": query.strip(),
    }
    result = _simple_request(url=url, params=params)
    videos = [
        (video["id"]["videoId"], video["snippet"]["title"]) for video in result["items"]
    ]
    return videos
