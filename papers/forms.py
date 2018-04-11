from django import forms

from .models import Papers


class PaperForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Papers
        fields = [
            'id',
            'name',
            'paper',
        ]
