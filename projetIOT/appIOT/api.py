from .models  import SensorReading
from .serializers import  TemperatureHumidityDataSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import  SensorReading
from .serializers import TemperatureHumidityDataSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import telepot
from django.conf import settings
import rest_framework



@api_view(["GET", "POST"])
def dhtser(request):
    if request.method == "GET":
        all_readings = SensorReading.objects.all()
        data_serializer = TemperatureHumidityDataSerializer(all_readings, many=True)
        return Response(data_serializer.data)
    elif request.method == "POST":
        serializer = TemperatureHumidityDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            latest_reading = SensorReading.objects.last()
            if latest_reading is not None:
                derniere_temperature = latest_reading.temperature


                if 2<= derniere_temperature <=8:

                    # Alert Email
                    subject = 'Alerte'
                    message = f"Alerte : La température actuelle est de {derniere_temperature} degrés Celsius, ce qui dépasse le seuil."
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['kaoutharelallam@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)
                    test_smtp_connection()  # Test de la connexion SMTP

                elif 8< derniere_temperature <=30 or  0<= derniere_temperature <2:
                    subject = 'Alerte'
                    message = "Alerte : Aucune lecture disponible."
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['kaoutharelallam@gmail.com','khadija.elali20@ump.ac.ma']
                    send_mail(subject, message, email_from, recipient_list)
                    test_smtp_connection()  # Test de la connexion SMTP

                elif derniere_temperature <0 or  derniere_temperature> 10:
                    subject = 'Alerte'
                    message = "Alerte : Aucune lecture disponible."
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['kaoutharelallam@gmail.com','khadija.elali20@ump.ac.ma','khadija1elle@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)
                    test_smtp_connection()  # Test de la connexion SMTP





            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import smtplib

def test_smtp_connection():
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp_server.quit()
        print("La connexion SMTP a réussi.")
    except Exception as e:
        print("Erreur lors de la connexion SMTP :", str(e))
# Alert whatsapp
#from twilio.rest import Client
#account_sid = '*'
#auth_token = '*'
#client = Client(account_sid, auth_token)

#message = client.messages.create(
#   from_= 'whatsapp:+14155238886',
#  body='Votre capteur de température a détecté un dépassement du seuil.',
# to='whatsapp:*',
#)