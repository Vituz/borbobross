from django.urls import path
from . import views
from .views import *
from .api.methods import *


urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('generator/', views.table_generator, name='generator'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new_deck/', views.add_new_deck, name='new-deck'),
    path('players/', views.players_view, name='player-view'),
    path('generator/api/table_generator/', generate_tables),
    path('matches/', views.matches, name='matches-page'),
    path('matches/api/delete_match/', delete_match),
    path('matches/api/save_match/', save_match),
    path('counter/', views.counter)
    
]
