from django import forms

from core.forms.utils import StringListField

from ..models import App, AppUser


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = "__all__"


class CreateAppForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    users = StringListField(widget=forms.Textarea)
    fe_repo = forms.CharField(label='Front End Repo', required=False)
    fe_ignore_files = StringListField(label='Ignore Files', widget=forms.Textarea, required=False)
    fe_folders = StringListField(label='Folders', widget=forms.Textarea, required=False)
    fe_token = forms.CharField(label='Access Token', required=False)

    be_repo = forms.CharField(label='Back End Repo', required=False)
    be_ignore_files = StringListField(label='Ignore Files', widget=forms.Textarea, required=False)
    be_folders = StringListField(label='Folders', widget=forms.Textarea, required=False)
    be_token = forms.CharField(label='Access Token', required=False)


class UpdateAppForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    users = StringListField(widget=forms.Textarea, required=False)
    
    fe_repo = forms.CharField(label='Front End Repo', required=False)
    fe_ignore_files = StringListField(label='Ignore Files', widget=forms.Textarea, required=False)
    fe_folders = StringListField(label='Folders', widget=forms.Textarea, required=False)
    fe_token = forms.CharField(label='Access Token', required=False)

    fe_repo = forms.CharField(label='Front End Repo', required=False)
    fe_ignore_files = StringListField(label='Ignore Files', widget=forms.Textarea, required=False)
    fe_folders = StringListField(label='Folders', widget=forms.Textarea, required=False)
    fe_token = forms.CharField(label='Access Token', required=False)

    be_repo = forms.CharField(label='Back End Repo', required=False)
    be_ignore_files = StringListField(label='Ignore Files', widget=forms.Textarea, required=False)
    be_folders = StringListField(label='Folders', widget=forms.Textarea, required=False)
    be_token = forms.CharField(label='Access Token', required=False)

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

    def clean(self):
        if self.app:
            cleaned_data = super().clean()
            users = cleaned_data["users"]
            self.cleaned_data['users'] = []
            for user in  users:
                user, created = AppUser.objects.get_or_create(app=self.app, name=user)
                self.cleaned_data['users'].append(user)