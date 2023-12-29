from . import views
from django.urls import path
from . import api
from .views import download_csv

urlpatterns = [
    path('api/temperature-humidity/',views.TemperatureHumidityDataList.as_view(), name='TemperatureHumidityDataList'),
    # path('sensor-data/a', views.sensor_data, name='sensor_data'),
    path('sensor-data/', views.sensor, name='sensor_data'),
    path('api/temperaturehumidity',api.dhtser),
    path('', views.tableau, name='tableau'),
    path('graphique/', views.graphique, name='graphique'),
    path('chart-data/', views.chart_data, name='chart-data'),
    path('download-csv/', download_csv, name='download_csv'),

]