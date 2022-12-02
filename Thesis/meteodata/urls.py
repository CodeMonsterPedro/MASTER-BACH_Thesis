from django.urls import path

from . import views

urlpatterns = [
    path('meteodata_list', views.MeteodataView.as_view(), name="meteodata"),
    path('meteodata_update', views.update_meteodata, name="meteodata_update"),
    path('forecast_list', views.ForecastView.as_view(), name="forecast"),
    path('forecast_update', views.update_forecast, name="forecast_update"),
    path('neuralnet_list', views.NeuralnetView.as_view(), name="neuralnets"),
    path('test_list', views.TestsView.as_view(), name="tests")
]
