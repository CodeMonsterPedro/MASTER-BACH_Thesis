from django.urls import path

from . import views

urlpatterns = [
    path('', views.MeteodataView.as_view(), name="meteodata-main"),
    path('meteodata-filter/', views.MeteodataChangePage.as_view(), name="meteodata-filter"),
    path('clear-meteodata-filter/', views.ClearMeteodataChangePage.as_view(), name="clear-meteodata-filter"),
    path('meteodata-sort/', views.MeteodataSortPage.as_view(), name="meteodata-sort"),
    path('clear-meteodata-sort/', views.ClearMeteodataSortPage.as_view(), name="clear-meteodata-sort"),
    path('meteodata-update/', views.MeteodataUpdateDataPage.as_view(), name="meteodata-update"),

    path('forecast/', views.ForecastView.as_view(), name="forecast-main"),
    path('forecast-filter/', views.ForecastChangePage.as_view(), name="forecast-filter"),
    path('clear-forecast-filter/', views.ClearForecastChangePage.as_view(), name="clear-forecast-filter"),
    path('forecast-sort/', views.ForecastSortPage.as_view(), name="forecast-sort"),
    path('clear-forecast-sort/', views.ClearForecastSortPage.as_view(), name="clear-forecast-sort"),
    path('forecast-update/', views.ForecastUpdateDataPage.as_view(), name="forecast-update"),
    path('forecast-update-test-result/', views.ForecastUpdateTestResultPage.as_view(), name="forecast-update-test-result"),

    path('anomaly/', views.AnomalyView.as_view(), name="anomaly-main"),
    path('anomaly-filter/', views.AnomalyChangePage.as_view(), name="anomaly-filter"),
    path('anomaly-update/', views.AnomalyUpdateDataPage.as_view(), name="anomaly-update"),
    path('anomaly-sort/', views.AnomalySortPage.as_view(), name="anomaly-sort")
]
