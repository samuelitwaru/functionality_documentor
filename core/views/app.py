from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from core.forms.app import CreateAppForm, UpdateAppForm
from core.forms.file import RefreshAppFilesForm
from core.forms.functionality import CreateFunctionalityForm
from core.tasks import run_task

from ..forms import AppForm
from ..models import App, AppUser


def get_apps(request):
    query = App.objects.filter(user=get_user(request))
    filter_apps_form = AppForm(data=request.GET)
    if filter_apps_form.is_valid():
        data = filter_apps_form.cleaned_data
        # get data

        # perform query

    page = int(request.GET.get('page', 1))
    paginator = Paginator(query.all(), settings.PAGINATION_COUNT)
    apps = paginator.get_page(page)
    context = {
        'apps': apps,
        'filter_apps_form': filter_apps_form,
    }
    return render(request, 'app/apps.html', context)


def get_collaboration_apps(request):
    user = user=get_user(request)
    query = user.apps
    filter_apps_form = AppForm(data=request.GET)
    if filter_apps_form.is_valid():
        data = filter_apps_form.cleaned_data
        # get data

        # perform query

    page = int(request.GET.get('page', 1))
    paginator = Paginator(query.all(), settings.PAGINATION_COUNT)
    apps = paginator.get_page(page)
    context = {
        'apps': apps,
        'filter_apps_form': filter_apps_form,
    }
    return render(request, 'app/collaboration-apps.html', context)


def get_app(request, id):
    app = App.objects.get(id=id)
    create_functionality_form = CreateFunctionalityForm(app=app)
    refresh_front_app_files_form = RefreshAppFilesForm(end='FRONT', app=app)
    refresh_back_app_files_form = RefreshAppFilesForm(end='BACK', app=app)
    context = {
        'app': app,
        'create_functionality_form': create_functionality_form,
        'refresh_front_app_files_form': refresh_front_app_files_form,
        'refresh_back_app_files_form': refresh_back_app_files_form
    }
    return render(request, 'app/app.html', context)


def create_app(request):
    create_app_form = CreateAppForm()
    if request.method == 'POST':
        create_app_form = CreateAppForm(request.POST)
        if create_app_form.is_valid():
            data = create_app_form.cleaned_data
            users = data.pop('users')
            app = App.objects.create(**data)
            AppUser.objects.bulk_create(
                [AppUser(name=name, app=app) for name in users])
            messages.success(request, 'app created')
            return redirect('core:get_apps')
    context = {
        'create_app_form': create_app_form,
    }
    return render(request, 'app/create-app.html', context)


def update_app(request, id):
    app = App.objects.get(id=id)
    app.users = [user.name for user in app.appuser_set.all()]
    update_app_form = UpdateAppForm(app=app, data={
        'name': app.name,
        'description': app.description,
        'users': app.users,
        'fe_repo': app.fe_repo,
        'fe_token': app.fe_token,
        'fe_ignore_files': app.fe_ignore_files,
        'fe_folders': app.fe_folders,
        'be_repo': app.be_repo,
        'be_token': app.be_token,
        'be_ignore_files': app.be_ignore_files,
        'be_folders': app.be_folders,
    })
    if request.method == 'POST':
        update_app_form = UpdateAppForm(app=app, data=request.POST)
        if update_app_form.is_valid():
            data = update_app_form.cleaned_data
            print(data)
            app.name = data['name']
            app.description = data['description']
            app.fe_repo = data['fe_repo']
            app.fe_token = data['fe_token']
            app.fe_ignore_files = data['fe_ignore_files']
            app.fe_folders = data['fe_folders']
            app.be_repo = data['be_repo']
            app.be_token = data['be_token']
            app.be_ignore_files = data['be_ignore_files']
            app.be_folders = data['be_folders']

            [user.delete() for user in app.appuser_set.all()
             if not user in data['users']]
            app.appuser_set.add(*data['users'])
            app.save()
            run_task('task 1')
            messages.success(request, 'app updated.')
            return redirect('core:get_app', id=id)
    context = {
        'update_app_form': update_app_form,
        'app': app,
    }
    return render(request, 'app/update-app.html', context)


def delete_app(request, id):
    app = App.objects.get(id=id)
    app.delete()
    messages.success(request, 'app deleted')
    return redirect('core:get_apps')
