import requests


def get_from_api(url):
    return requests.get(url).json()


def get_all_trivia():
    url = "https://opentdb.com/api.php?amount=20"
    return get_from_api(url)["results"]
