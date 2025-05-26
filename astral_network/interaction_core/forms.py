from django import forms

from interaction_core.models import Music


class AddMusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = (
            'author', 'title', 'music',
        )