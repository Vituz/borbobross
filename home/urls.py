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
    path('modify_deck/<int:deck_id>/', views.modify_deck, name='modify-deck'),
    path("delete_deck/<int:deck_id>", views.delete_deck, name="delete-deck"),
    path('players/', views.players_view, name='player-view'),
    path('players/<int:player_id>/', views.player_decks_list, name='player-deck-list'),
    path('stats/', views.stats_page, name='stats-page'),
    path('generator/api/table_generator/', generate_tables),
    path('matches/', views.matches, name='matches-page'),
    path('matches/api/delete_match/', delete_match),
    path('matches/api/save_match/', save_match),
    path('counter/', views.counter)
    
]
