from django.db import models
from printing.models import Order, Material


class Material3d(Material):
    pass


class Order3d(Order):
    material = models.ForeignKey(Material3d)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    chargeable_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    junk_weight = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)

    class Meta:
        permissions = (
            ('view_order3d', 'Can view'),
        )
