from django.urls import path
from . import views
from .views import *
from .api.methods import *


urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('generator/', views.table_generator, name='generator'),
    path('generator/api/table_generator/', generate_tables),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('matches/', views.matches, name='matches-page'),
    path('matches/api/delete_match/', delete_match),
    path('matches/api/save_match/', save_match),
    path('counter/', views.counter)
    
]
