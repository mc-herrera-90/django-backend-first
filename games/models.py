import json
from pathlib import Path


DATA_PATH = Path(__file__).parent / "static" / "data"


def _load_data(platform):
    file_path = DATA_PATH / f"{platform}.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


class Game:

    def __init__(
        self,
        id,
        title,
        year,
        genre,
        developer,
        platform,
        publisher,
        rating,
        portrait,
        marquee,
        video,
        description,
    ):
        self.id = id
        self.title = title
        self.year = year
        self.genre = genre
        self.developer = developer
        self.platform = platform
        self.platform_file = None
        self.publisher = publisher
        self.rating = rating
        self.portrait = portrait
        self.marquee = marquee
        self.video = video
        self.description = description
        
    @property
    def platform_icon(self):
        return f"img/platforms/{self.platform_file}.webp"


    def _get_image(self, filename):
        image_path = (
            Path(__file__).parent
            / "static"
            / self.portrait.rsplit("/", 1)[0]
            / filename
        )

        if image_path.exists():
            return self.portrait.rsplit("/", 1)[0] + f"/{filename}"

        return None


    @property
    def cartridge(self):
        return self._get_image("cartucho.webp")


    @property
    def poster(self):
        return self._get_image("poster.webp")

    @classmethod
    def platforms(cls):
        return [
            file.stem
            for file in DATA_PATH.glob("*.json")
        ]

    @classmethod
    def all(cls):
        games = []
        game_id = 1

        for platform in cls.platforms():

            for game in _load_data(platform):

                game_instance = cls(
                    id=game_id,
                    **game
                )

                game_instance.platform_file = platform

                games.append(game_instance)
                game_id += 1

        return games

    @classmethod
    def get(cls, game_id):
        return next(
            (
                game
                for game in cls.all()
                if game.id == game_id
            ),
            None,
        )