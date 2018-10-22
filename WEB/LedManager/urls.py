from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.home),
    path('article/<id_article>', views.view_article),
    path('turnon/', views.turnon),
]
