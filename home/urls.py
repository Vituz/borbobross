from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('generator/', views.table_generator, name='generator'),
    path('generator/api/table_generator/', generate_tables)
]
