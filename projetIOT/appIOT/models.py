import os
from django.db import models
class SensorReading(models.Model):
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        #return str(self.temperature)
        return f"{self.temperature}°C, {self.humidity}%"
