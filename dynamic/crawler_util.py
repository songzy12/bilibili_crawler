import requests
from . import constant


def fetch_dynamic_api(api_url, cookie):
    headers = constant.HEADERS_TEMPLATE.copy()
    headers["Cookie"] = cookie

    print(f"fetching {api_url}")
    return requests.get(api_url, headers=headers).json()


def fetch_picture(picture_url, cookie=None):
    print(f"crawling: {picture_url}")
    # Use minimal headers suitable for CDN image fetches.
    headers = {
        "User-Agent": constant.HEADERS_TEMPLATE.get("User-Agent", ""),
        "Referer": "https://www.bilibili.com/",
    }
    if cookie:
        headers["Cookie"] = cookie

    return requests.get(picture_url, headers=headers).content
