from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Game


def home(request):

    # Todas las plataformas disponibles según los archivos JSON
    platforms = Game.platforms()

    # Todos los juegos
    games = Game.all()

    # Plataforma seleccionada
    platform = request.GET.get("platform")

    # Filtrar por el nombre del archivo JSON
    if platform and platform in platforms:
        games = [
            game
            for game in games
            if game.platform_file == platform
        ]

    # Paginación
    paginator = Paginator(games, 12)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {
            "page_obj": page_obj,
            "platforms": platforms,
        },
    )


def detail(request, game_id):

    game = Game.get(game_id)

    if game is None:
        return render(
            request,
            "games/404.html",
            status=404,
        )

    return render(
        request,
        "detail.html",
        {
            "game": game,
        },
    )
