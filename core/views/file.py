from django.contrib import messages
from django.shortcuts import render, redirect

from core.forms.file import RefreshAppFilesForm
from ..forms import CreateFunctionalityForm, UpdateFunctionalityForm
from ..models import App, File
from github import Github

def refresh_app_files(request, app_id):
    app = App.objects.get(id=app_id)
    refresh_app_files_form = RefreshAppFilesForm(data=request.POST)
    if refresh_app_files_form.is_valid():
        data = refresh_app_files_form.cleaned_data
        # load files
        g = Github(data['access_token'])
        repo = g.get_repo('samuelitwaru/wex-results')
        folders = app.folders or [""]
        count = 0
        for folder in folders:
            contents = repo.get_contents(folder)
            while len(contents) > 1:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    print(file_content.path)
                    # store file path
                    file, created = File.objects.get_or_create(path=file_content.path, app=app)
                    if created:
                        count += 1
                    print(file.dot_notation())
                    
        # batch save files
        messages.success(request, f"Loaded {count} new files")
        return redirect(request.META.get('HTTP_REFERER'))

