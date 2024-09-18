import requests


def get_from_api(url):
    return requests.get(url).json()


def get_users():
    url = "https://randomuser.me/api?results=4"
    return get_from_api(url)["results"]
