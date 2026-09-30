import requests

from django.conf import settings


BASE_URL = "https://api.screenscraper.fr/api2"


def _get_params():
    return {
        "devid": settings.SCREENSCRAPER_DEVID,
        "devpassword": settings.SCREENSCRAPER_DEVPASSWORD,
        "softname": settings.SCREENSCRAPER_SOFTNAME,
        "ssid": settings.SCREENSCRAPER_USER,
        "sspassword": settings.SCREENSCRAPER_PASSWORD,
        "output": "json",
    }

def search_games(query, system_id=None):
    params = _get_params()
    params["recherche"] = query

    if system_id:
        params["systemeid"] = system_id

    response = requests.get(
        f"{BASE_URL}/jeuRecherche.php",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def get_game(game_id, system_id=None):
    params = _get_params()
    params["gameid"] = game_id

    if system_id:
        params["systemeid"] = system_id

    response = requests.get(
        f"{BASE_URL}/jeuInfos.php",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()