from django.urls import path

from .views import *

app_name = "core"

urlpatterns = [
    path('', get_apps, name='get_apps'),
    path('apps/', get_apps, name='get_apps'),
    path('apps/collaboration', get_collaboration_apps, name='get_collaboration_apps'),
    path('apps/<int:id>/', get_app, name='get_app'),
    path('apps/create/', create_app, name='create_app'),
    path('apps/<int:id>/update/', update_app, name='update_app'),
    path('apps/<int:id>/delete/', delete_app, name='delete_app'),

    path('apps/<int:app_id>/functionalities/create/', create_app_functionality, name='create_app_functionality'),
    path('apps/<int:app_id>/functionalities/<int:id>/', get_app_functionality, name='get_app_functionality'),
    path('apps/<int:app_id>/functionalities/<int:id>/update', update_app_functionality, name='update_app_functionality'),
    path('functionalities/<int:id>/delete/', delete_functionality, name='delete_functionality'),

    path('apps/<int:app_id>/files/refresh/', refresh_app_files, name='refresh_app_files'),

]