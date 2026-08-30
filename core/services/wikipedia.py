from urllib.parse import quote

import requests


WIKIPEDIA_API = (
    "https://es.wikipedia.org/api/rest_v1/page/summary/{}"
)

HEADERS = {
    "User-Agent": "ZonaGeek/1.0"
}


def get_person_summary(name):
    url = WIKIPEDIA_API.format(
        quote(name)
    )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=5,
        )

        if response.status_code != 200:
            return None

        data = response.json()

    except (
        requests.RequestException,
        ValueError,
    ):
        return None

    thumbnail = data.get("thumbnail") or {}

    content_urls = data.get("content_urls") or {}

    desktop = content_urls.get("desktop") or {}

    return {
        "title": data.get("title"),
        "description": data.get("description"),
        "extract": data.get("extract"),
        "image": thumbnail.get("source"),
        "url": desktop.get("page"),
    }