from django import forms
from ..models import App, AppUser

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = "__all__"

class CreateAppForm(forms.Form):
    name = forms.CharField()
    repository = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    users = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        users = cleaned_data["users"]
        if users:
            self.cleaned_data['users'] = users.split(',')
        else:
            self.cleaned_data['users'] = []


class UpdateAppForm(forms.Form):
    name = forms.CharField()
    repository = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    users = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

    def clean(self):
        if self.app:
            cleaned_data = super().clean()
            print(cleaned_data)
            users = cleaned_data["users"]
            self.cleaned_data['users'] = []
            print('>>>>>>>>>>>>>', users)
            print('hello')
            if users:
                users = users.split(',')
                for user in  users:
                    user, created = AppUser.objects.get_or_create(app=self.app, name=user)
                    self.cleaned_data['users'].append(user)