from django.db import models

# Create your models here.

class View_data(models.Model):
        device_id = models.CharField(max_length=10, null=True, blank=True)
        date = models.DateField(null=True, blank=True)
        kwh = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
        power = models.DecimalField(max_digits=15,decimal_places=6, null=True, blank=True)
