from django import forms

from .models import TempSettings


class TempSettingsForm(forms.ModelForm):
    class Meta:
        model = TempSettings
