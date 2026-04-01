
# Create your models here.
from django.db import models
from django.contrib.gis.db import models as gis_models
import django.utils.timezone as djangoTimezone

# Create your models here.
class Predio(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    geom = gis_models.PolygonField(srid=25830,blank=True, null=True) 
    data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

    def save(self, *args, **kwargs):
            # Calculate values from the geometry before saving
            if self.geom:
                self.area = self.geom.area
                self.perimeter = self.geom.length
            
            super().save(*args, **kwargs)


class Calles(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    perimeter = models.FloatField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    geom = gis_models.LineStringField(srid=25830,blank=True, null=True) 
    data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())
    
    def save(self, *args, **kwargs):
            # Calculate values from the geometry before saving
            if self.geom:
                self.perimeter = self.geom.length
            
            super().save(*args, **kwargs)

class Iglesias(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    geom = gis_models.PointField(srid=25830,blank=True, null=True) 
    data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

