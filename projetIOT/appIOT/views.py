from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import SensorReading
from .serializers import TemperatureHumidityDataSerializer
from django.utils import timezone
from django.http import JsonResponse
import csv
from django.http import HttpResponse

def sensor_data(request):

    if request.method == "POST":
        # Récupération des données de la requête POST
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        # Création d'une instance du modèle SensorReading avec les données reçues
        sensor_reading = SensorReading.objects.create(temperature=temperature, humidity=humidity)
        # Sérialisation de l'instance créée pour envoyer la réponse
        serializer = TemperatureHumidityDataSerializer(sensor_reading)
        # Envoi de la réponse avec le code HTTP 201 CREATED
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        # Si la méthode HTTP n'est pas POST, on récupère toutes les données de la base de données et on les affiche
        queryset = SensorReading.objects.all()
        serializer_class = TemperatureHumidityDataSerializer
        readings = [{'temperature': reading.temperature, 'humidity': reading.humidity, 'created_at': reading.created_at} for reading in queryset]

def sensor(request):
    data=SensorReading.objects.all();
    return render(request, 'appIOT/sensor_data.html',{'data':data})

class TemperatureHumidityDataList(generics.ListAPIView):
    queryset = SensorReading.objects.all()
    serializer_class = TemperatureHumidityDataSerializer

from datetime import timedelta

def tableau(request):
    # Récupérer la dernière valeur de température et d'humidité
    last_reading = SensorReading.objects.last()
    last_temperature = last_reading.temperature if last_reading else None
    last_humidity = last_reading.humidity if last_reading else None

    # Calculer le temps écoulé depuis la dernière valeur stockée
    time_elapsed = None
    if last_reading:
        time_elapsed = timezone.now() - last_reading.created_at
        '''minutes_elapsed = int(round(time_elapsed.total_seconds() %60))
        heur_elepsed=int(round(time_elapsed.total_seconds() /3600))
        time_elapsed = f'il y a {minutes_elapsed} minute{"s" if minutes_elapsed > 1 else ""}' '''
    minutes_elapsed = int(round(time_elapsed.total_seconds() / 60))
    jours = minutes_elapsed // 1440
    heure = (minutes_elapsed % 1440) // 60
    minute = minutes_elapsed % 60

    if jours >= 1:
        time_elapsed = f"il y a {jours}J {heure}H {minute}min"
    elif heure >= 1:
        time_elapsed = f"il y a {heure}H {minute}min"
    else:
        time_elapsed = f"il y a {minute}min"



    context = {
        'last_temperature': last_temperature,
        'last_humidity': last_humidity,
        'time_elapsed': time_elapsed,
    }
    return render(request, 'appIOT/tableau.html', context)




def graphique(request):
    return render(request, 'appIOT/graphique.html')


def chart_data(request):
    dht = SensorReading.objects.all()


    data={
        'temps': [Dt.created_at for Dt in dht],
        'temperature': [Temp.temperature for Temp in dht],
        'humidity': [Hum.humidity for Hum in dht]
    }
    return JsonResponse(data)
def graphique(request):
    return render(request, 'appIOT/graphique.html')


def chart_data(request):
    dht = SensorReading.objects.all()


    data={
        'temps': [Dt.created_at for Dt in dht],
        'temperature': [Temp.temperature for Temp in dht],
        'humidity': [Hum.humidity for Hum in dht]
    }
    return JsonResponse(data)




def download_csv(request):
    model_values = SensorReading.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['temperature', 'humidity', 'created_at'])

    for reading in model_values:
        writer.writerow([reading.temperature, reading.humidity, reading.created_at])

    return response

