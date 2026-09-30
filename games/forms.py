from django import forms

from .models import Game, GameRating


class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["platform"].empty_label = "Selecciona una opción"

    class Meta:
        model = Game
        fields = (
            "title",
            "year",
            "genre",
            "developer",
            "platform",
            "publisher",
            "portrait",
            "marquee",
            "video",
            "technical_sheet",
            "cartridge",
            "description",
        )

        widgets = {
            "portrait": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                },
            ),
            "marquee": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                },
            ),
            "cartridge": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                },
            ),
            "video": forms.ClearableFileInput(
                attrs={
                    "accept": "video/mp4,video/webm,video/quicktime",
                },
            ),
            "technical_sheet": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf",
                },
            ),
        }


class GameRatingForm(forms.ModelForm):

    class Meta:
        model = GameRating
        fields = (
            "rating",
            "comment",
        )

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "La valoración debe estar entre 1 y 5."
            )

        return rating

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()

        if len(comment) > 500:
            raise forms.ValidationError(
                "El comentario no puede superar los 500 caracteres."
            )

        return comment