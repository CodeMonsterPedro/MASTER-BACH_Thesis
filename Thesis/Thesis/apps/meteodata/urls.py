from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.test, name='search'),
    path('data_providers/', views.test, name='data_providers'),
    path('test/', views.test, name='test'),
]
