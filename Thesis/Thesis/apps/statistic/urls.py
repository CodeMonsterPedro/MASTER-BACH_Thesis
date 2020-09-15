from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('current/', views.test, name='current'),
    path('forecast/', views.test, name='forecast'),
    path('test/', views.test, name='test'),

]
