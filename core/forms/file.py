from django import forms


class RefreshAppFilesForm(forms.Form):
    access_token = forms.CharField(required=True)

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app:
            self.fields['access_token'].initial = app.access_token
    