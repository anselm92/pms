from django.db import models
from printing.models import Order, Material


class Material3d(Material):
    pass


class Order3d(Order):
    material = models.ForeignKey(Material3d)
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()
