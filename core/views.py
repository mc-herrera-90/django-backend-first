from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

from .services.wikipedia import get_person_summary


def index(request):
    return render(
        request,
        "index.html",
    )


def wikipedia_person(request):
    name = request.GET.get("name", "").strip()

    if not name:
        return JsonResponse(
            {"error": "Nombre requerido"},
            status=400,
        )

    cache_key = f"wikipedia_person:{name.lower()}"

    person = cache.get(cache_key)

    if person is None:
        person = get_person_summary(name)

        if person is None:
            return JsonResponse(
                {"error": "Persona no encontrada"},
                status=404,
            )

        cache.set(
            cache_key,
            person,
            timeout=60 * 60 * 24,
        )

    return JsonResponse(person)