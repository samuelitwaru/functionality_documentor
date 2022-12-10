from django.contrib import messages
from django.shortcuts import redirect, render
from github import Github

from core.forms.file import RefreshAppFilesForm
from core.utils import get_url_path, match_file

from ..forms import CreateFunctionalityForm, UpdateFunctionalityForm
from ..models import App, File


def refresh_app_files(request, app_id):
    app = App.objects.get(id=app_id)
    refresh_app_files_form = RefreshAppFilesForm(data=request.POST)
    if refresh_app_files_form.is_valid():
        data = refresh_app_files_form.cleaned_data
        end = data['end']
        # load files
        if end == 'FRONT':
            ignore_files = app.fe_ignore_files
            folders = app.fe_folders or [""]
            repo_url = app.fe_repo
        else:
            ignore_files = app.be_ignore_files
            folders = app.be_folders or [""]
            repo_url = app.be_repo


        g = Github(data['token'])
        repo = g.get_repo(get_url_path(repo_url))
        file_ids = []
        count = 0
        for folder in folders:
            contents = repo.get_contents(folder)
            while len(contents) > 1:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    if match_file(file_content.path, ignore_files):
                        continue
                    # store file path
                    file, created = File.objects.get_or_create(path=file_content.path, end=end, app=app)
                    file_ids.append(file.id)
                    if created:
                        count += 1
        # delete other files
        File.objects.filter(app=app, end=end).exclude(id__in=file_ids).delete() 
        # batch save files
        messages.success(request, f"Loaded {count} new files")
        return redirect(request.META.get('HTTP_REFERER'))

