from django import forms
from ..models import App, AppUser, Functionality
from .utils import StringListField


class CreateFunctionalityForm(forms.Form):
    app = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField()
    front_end_file = forms.CharField(required=False, empty_value=None)
    back_end_file = forms.CharField(required=False, empty_value=None)
    front_end_handler = forms.CharField(required=False, empty_value=None)
    back_end_handler = forms.CharField(required=False, empty_value=None)
    description = forms.CharField(widget=forms.Textarea)
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app:
            self.fields["app"].initial = app.id
            self.fields['users'].choices = [(user.id, user) for user in app.appuser_set.all()]
    
    def clean(self):
        cleaned_data = super().clean()
        app_id = cleaned_data["app"]
        self.cleaned_data['app'] = App.objects.get(id=app_id)
        self.cleaned_data['users'] = AppUser.objects.filter(id__in=cleaned_data['users'])


class UpdateFunctionalityForm(forms.Form):
    app = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField()
    front_end_file = forms.CharField(required=False, empty_value=None)
    back_end_file = forms.CharField(required=False, empty_value=None)
    front_end_handler = forms.CharField(required=False, empty_value=None)
    back_end_handler = forms.CharField(required=False, empty_value=None)
    description = forms.CharField(widget=forms.Textarea)
    helpers = StringListField(widget=forms.Textarea, required=False)
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, func=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if func:
            self.fields['users'].choices = [(user.id, user) for user in func.app.appuser_set.all()]

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['users'] = AppUser.objects.filter(id__in=cleaned_data['users'])
        

