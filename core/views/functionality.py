from django.contrib import messages
from django.shortcuts import render, redirect

from core.utils import create_gist, delete_gist
from ..forms import CreateFunctionalityForm, UpdateFunctionalityForm
from ..models import App, Functionality


def get_app_functionality(request, app_id, id):
    app = App.objects.get(id=app_id)
    functionality = Functionality.objects.get(id=id)
    context = {
        'app': app,
        'func': functionality,
    }
    return render(request, 'functionality/functionality.html', context)


def create_app_functionality(request, app_id):
    if request.method == 'POST':
        app = App.objects.get(id=app_id)
        create_functionality_form = CreateFunctionalityForm(
            app=app, data=request.POST)
        if create_functionality_form.is_valid():
            data = create_functionality_form.cleaned_data
            users = data.pop('users')
            func = Functionality.objects.create(**data)
            func.users.set(users)
            messages.success(request, 'functionality created')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            context = {
                'create_functionality_form': create_functionality_form,
                'app': app
            }
            return render(request, 'app/app.html', context)


def update_app_functionality(request, app_id, id):
    func = Functionality.objects.get(id=id)
    update_functionality_form = UpdateFunctionalityForm(func=func, data={
        'app': func.app.id,
        'name': func.name,
        'front_end_file': func.front_end_file,
        'back_end_file': func.back_end_file,
        'front_end_handler': func.front_end_handler,
        'back_end_handler': func.back_end_handler,
        'description': func.description,
        'users': [user.id for user in func.users.all()],
        'helpers': func.helpers
    })
    if request.method == 'POST':
        update_functionality_form = UpdateFunctionalityForm(
            func=func, data=request.POST)
        if update_functionality_form.is_valid():
            data = update_functionality_form.cleaned_data
            func.name = data['name']
            func.description = data['description']
            func.front_end_handler = data['front_end_handler']
            func.back_end_handler = data['back_end_handler']
            func.helpers = data['helpers']
            app = func.app

            if data['front_end_file']:
                if func.front_end_gist:
                    delete_gist(app.fe_token, func.front_end_gist)
                gist = create_gist(
                    app.fe_token, app.fe_repo_name,  data['front_end_file'])
                func.front_end_gist = gist.id
                func.front_end_file = data['front_end_file']

            if data['back_end_file']:
                if func.back_end_gist:
                    delete_gist(app.fe_token, func.back_end_gist)
                gist = create_gist(
                    app.be_token, app.be_repo_name,  data['back_end_file'])
                func.back_end_file = data['back_end_file']
                func.back_end_gist = gist.id

            func.save()

            func.users.set(data['users'])
            messages.success(request, 'functionality updated.')
            return redirect('core:get_app_functionality', app_id=app_id, id=id)
    context = {
        'update_functionality_form': update_functionality_form,
        'func': func,
    }
    return render(request, 'functionality/update-functionality.html', context)


def delete_functionality(request, id):
    functionality = Functionality.objects.get(id=id)
    app = functionality.app
    functionality.delete()
    messages.success(request, 'functionality deleted')
    return redirect('core:get_app', id=app.id)
