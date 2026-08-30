import json
from pathlib import Path

def _load_data():
    file_path = (
        Path(__file__).parent
        / "static"
        / "data"
        / "movies.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

class Movie:

    def __init__(
        self,
        id,
        title,
        year,
        genre,
        director,
        duration,
        rating,
        country,
        language,
        studio,
        portrait,
        landscape,
        description,
        cast,
        trailer
    ):
        self.id = id
        self.title = title
        self.year = year
        self.genre = genre
        self.director = director
        self.duration = duration
        self.rating = rating
        self.country = country
        self.language = language
        self.studio = studio
        self.portrait = portrait
        self.landscape = landscape
        self.description = description
        self.cast = cast
        self.trailer = trailer

    @classmethod
    def all(cls):
        return [cls(**movie) for movie in _load_data()]

    @classmethod
    def get(cls, movie_id):
        return next(
            (movie for movie in cls.all() if movie.id == movie_id),
            None,
        )