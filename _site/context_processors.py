from django.conf import settings

def site_info(request):
    return {
        "site_name": settings.SITE_NAME,
    }

def navbar_items(request):
    return {
        "navbar_items": [
            {
                "name": "GAMES",
                "icon": "👾",
                "url": "games:home",
                "namespace": "games",
            },
            {
                "name": "MOVIES",
                "icon": "🎬",
                "url": "movies:home",
                "namespace": "movies",
            },
        ]
    }
