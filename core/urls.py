from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('results', views.results, name='results'),
]