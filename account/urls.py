from django.urls import path

from .views import *

app_name = "account"

urlpatterns = [
    path('account/', index, name='index'),
    path('account/signin', signin, name='signin'),
    path('account/signup', signup, name='signup'),
    path('account/logout', logout_view, name='logout'),
]
