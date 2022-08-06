from random import choices
from django import forms

from core.utils import END_CHOICES


class RefreshAppFilesForm(forms.Form):
    end = forms.CharField(required=True)
    token = forms.CharField(required=True)

    def __init__(self, end=None, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app:
            if end == 'FRONT':
                self.fields['token'].initial = app.fe_token
            else:
                self.fields['token'].initial = app.be_token
            print(end)
            self.fields['end'].initial = end
    