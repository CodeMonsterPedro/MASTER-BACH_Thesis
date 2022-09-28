from django.urls import path

from . import views

urlpatterns = [
    path('meteodata_list/', views.MeteodataView.as_view(), name="meteodata"),
    path('forecast_list/', views.ForecastView.as_view(), name="forecast"),
    path('anomaly_list/', views.AnomalyView.as_view(), name="anomaly"),
    path('neuralnet_list/', views.AnomalyView.as_view(), name="neuralnets"),
    path('test_list/', views.AnomalyView.as_view(), name="tests"),
    path('map/', views.AnomalyView.as_view(), name="map"),
    path('charts/', views.AnomalyView.as_view(), name="charts"),
]
