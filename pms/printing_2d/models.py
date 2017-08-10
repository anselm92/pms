from django.db import models
from printing.models import Order, CostCenter, Material


class CoverSheetColor(models.Model):
    name = models.CharField(max_length=99)
    color_code = models.CharField(max_length=99)

    def __str__(self):
        return self.name


class ScriptOrder(Order):
    cover_sheet_color = models.ForeignKey(CoverSheetColor)


class PostProcessing2d(models.Model):
    name = models.CharField(max_length=99)

    def __str__(self):
        return self.name


class Material2d(Material):
    paper_weight = models.FloatField()  # Weight in grams
    paper_format = models.CharField(max_length=20)

    def __str__(self):
        return '%s, %d grams' % (self.paper_format, self.paper_weight)


SIDED_PRINTING_SIMPLEX = 1
SIDED_PRINTING_DUPLEX = 2
SIDED_PRINTING = ((SIDED_PRINTING_SIMPLEX, 'Simplex'),
                  (SIDED_PRINTING_DUPLEX, 'Duplex'),)


class CustomOrder2d(Order):
    sided_printing = models.SmallIntegerField(choices=SIDED_PRINTING, default=SIDED_PRINTING_SIMPLEX)
    chromatic_printing = models.BooleanField(default=False)
    cost_center = models.ForeignKey(CostCenter)
    post_processing = models.ManyToManyField(PostProcessing2d)
    material = models.ForeignKey(Material2d)
