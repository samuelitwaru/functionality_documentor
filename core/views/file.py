from django.contrib import messages
from django.shortcuts import render, redirect

from core.forms.file import RefreshAppFilesForm
from core.utils import match_file
from ..forms import CreateFunctionalityForm, UpdateFunctionalityForm
from ..models import App, File
from github import Github

def refresh_app_files(request, app_id):
    app = App.objects.get(id=app_id)
    refresh_app_files_form = RefreshAppFilesForm(data=request.POST)
    if refresh_app_files_form.is_valid():
        data = refresh_app_files_form.cleaned_data
        # load files
        g = Github(data['fe_token'])
        repo = g.get_repo(app.repo_name)
        fe_ignore_files = app.fe_ignore_files
        fe_folders = app.fe_folders or [""]
        file_ids = []
        count = 0
        for folder in fe_folders:
            contents = repo.get_contents(folder)
            while len(contents) > 1:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    if match_file(file_content.path, fe_ignore_files):
                        continue
                    # store file path
                    file, created = File.objects.get_or_create(path=file_content.path, app=app)
                    file_ids.append(file.id)
                    if created:
                        count += 1
        # delete other files
        File.objects.exclude(id__in=file_ids).delete() 
        # batch save files
        messages.success(request, f"Loaded {count} new files")
        return redirect(request.META.get('HTTP_REFERER'))

