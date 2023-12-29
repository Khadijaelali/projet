from rest_framework import serializers
from .models import SensorReading

class TemperatureHumidityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'