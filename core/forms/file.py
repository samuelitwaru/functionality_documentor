from django import forms


class RefreshAppFilesForm(forms.Form):
    fe_token = forms.CharField(required=True)

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app:
            self.fields['fe_token'].initial = app.fe_token
    