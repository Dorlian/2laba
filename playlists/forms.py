from django import forms

from .data import TRACKS


def _track_choices():
    return [(t["id"], f'{t["artist"]} — {t["title"]}') for t in TRACKS]


class PlaylistForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "",
                "autocomplete": "off",
            }
        ),
    )
    description = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "input input--area",
                "rows": 3,
                "placeholder": "",
            }
        ),
    )
    track_ids = forms.MultipleChoiceField(
        choices=_track_choices,
        label="",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "track-pick"}),
    )
