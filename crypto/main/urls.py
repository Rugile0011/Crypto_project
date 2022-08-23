from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [

    path('chart/', views.graph_view, name='chart'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
]
