from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests

from .forms import GameForm, GameRatingForm
from .models import Game, GameRating, Platform
from .services.screenscraper import search_games


def home(request):

    platforms = Platform.objects.all().order_by("name")

    games = Game.objects.select_related(
        "platform",
        "user",
    ).annotate(
        average_rating=Avg("ratings__rating"),
    )

    platform = request.GET.get("platform")

    if platform and platforms.filter(identifier=platform).exists():
        games = games.filter(
            platform__identifier=platform,
        )

    paginator = Paginator(
        games,
        12,
    )

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

    game = get_object_or_404(
        Game,
        id=game_id,
    )

    average_rating = game.ratings.aggregate(
        average=Avg("rating"),
    )["average"]

    ratings = game.ratings.select_related(
        "user",
    ).order_by(
        "-created_at",
    )

    user_rating = None

    if request.user.is_authenticated:

        user_rating = GameRating.objects.filter(
            game=game,
            user=request.user,
        ).first()

    return render(
        request,
        "detail.html",
        {
            "game": game,
            "average_rating": average_rating,
            "user_rating": user_rating,
            "ratings": ratings,
        },
    )


@login_required
def admin(request):

    games = Game.objects.filter(
        user=request.user,
    )

    return render(
        request,
        "games/admin/home.html",
        {
            "games": games,
        },
    )


@login_required
def create(request):

    if request.method == "POST":

        form = GameForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            game = form.save(
                commit=False,
            )

            game.user = request.user

            game.save()

            return redirect(
                "games:admin",
            )

    else:

        form = GameForm()

    return render(
        request,
        "games/admin/form.html",
        {
            "form": form,
        },
    )


@login_required
def edit(request, game_id):

    game = get_object_or_404(
        Game,
        id=game_id,
        user=request.user,
    )

    if request.method == "POST":

        form = GameForm(
            request.POST,
            request.FILES,
            instance=game,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "games:admin",
            )

    else:

        form = GameForm(
            instance=game,
        )

    return render(
        request,
        "games/admin/form.html",
        {
            "form": form,
            "game": game,
        },
    )


@login_required
def rate(request, game_id):

    game = get_object_or_404(
        Game,
        id=game_id,
    )

    rating = GameRating.objects.filter(
        game=game,
        user=request.user,
    ).first()

    if request.method == "POST":

        form = GameRatingForm(
            request.POST,
            instance=rating,
        )

        if form.is_valid():

            game_rating = form.save(
                commit=False,
            )

            game_rating.game = game
            game_rating.user = request.user

            game_rating.save()

            return redirect(
                "games:detail",
                game_id=game.id,
            )

    else:

        form = GameRatingForm(
            instance=rating,
        )

    return render(
        request,
        "detail.html",
        {
            "game": game,
            "form": form,
            "average_rating": game.ratings.aggregate(
                average=Avg("rating"),
            )["average"],
            "user_rating": rating,
            "ratings": game.ratings.select_related(
                "user",
            ).order_by(
                "-created_at",
            ),
        },
    )


@login_required
def delete(request, game_id):

    game = get_object_or_404(
        Game,
        id=game_id,
        user=request.user,
    )

    if request.method == "POST":

        game.delete()

        return redirect(
            "games:admin",
        )

    return redirect(
        "games:admin",
    )


@login_required
def screenscraper_search(request):

    query = request.GET.get(
        "q",
        "",
    ).strip()

    system_id = request.GET.get(
        "system_id",
    )

    if not query:

        return JsonResponse(
            {
                "results": [],
            }
        )

    try:

        data = search_games(
            query,
            system_id=system_id,
        )

    except requests.RequestException:

        return JsonResponse(
            {
                "error": "No fue posible conectarse con ScreenScraper.",
            },
            status=502,
        )

    games = data.get(
        "response",
        {},
    ).get(
        "jeux",
        [],
    )

    results = []

    for game in games:

        results.append(
            {
                "id": game.get("id"),
                "name": game.get("noms", {}).get(
                    "nom",
                    "",
                ),
            }
        )

    return JsonResponse(
        {
            "results": results,
        }
    )