from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

from core.forms.app import CreateAppForm, UpdateAppForm
from core.forms.functionality import CreateFunctionalityForm
from ..models import App, AppUser
from ..forms import AppForm



def get_apps(request):
    query = App.objects
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


def get_app(request, id):
    app = App.objects.get(id=id)
    create_functionality_form = CreateFunctionalityForm(app=app)
    context = {
        'app': app,
        'create_functionality_form': create_functionality_form,
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
            AppUser.objects.bulk_create([AppUser(name=name, app=app) for name in users])
            messages.success(request, 'app created')
            return redirect('core:get_apps')
    context = {
        'create_app_form': create_app_form,
    }
    return render(request, 'app/create-app.html', context)


def update_app(request, id):
    app = App.objects.get(id=id)
    app.users = [user.name for user in app.appuser_set.all()]
    print(app.appuser_set.all())
    print(app.users)
    update_app_form = UpdateAppForm(app=app, data={
        'name':app.name,
        'repository':app.repository,
        'description':app.description,
        'users':','.join(app.users),
    })
    if request.method == 'POST':
        update_app_form = UpdateAppForm(app=app, data=request.POST)
        if update_app_form.is_valid():
            data = update_app_form.cleaned_data
            app.name = data['name']
            app.repository = data['repository']
            app.description = data['description']
            [user.delete() for user in app.appuser_set.all() if not user in data['users']]
            app.appuser_set.add(*data['users'])
            app.save()
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