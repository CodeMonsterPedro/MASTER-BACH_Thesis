from django.urls import path

from . import views

urlpatterns = [
    path('', views.MeteodataView.as_view(), name="meteodata-main"),
    path('meteodata-filter/', views.MeteodataChangePage.as_view(), name="meteodata-filter"),
    path('meteodata-update/', views.MeteodataUpdateDataPage.as_view(), name="meteodata-update"),
    path('forecast/', views.ForecastView.as_view(), name="forecast-main"),
    path('forecast-filter/', views.ForecastChangePage.as_view(), name="forecast-filter"),
    path('forecast-update/', views.ForecastUpdateDataPage.as_view(), name="forecast-update"),
    path('anomaly/', views.AnomalyView.as_view(), name="anomaly-main"),
    path('anomaly-filter/', views.AnomalyChangePage.as_view(), name="anomaly-filter"),
    path('anomaly-update/', views.AnomalyUpdateDataPage.as_view(), name="anomaly-update")
]
