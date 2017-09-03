from django import template
from printing_2d.models import SIDED_PRINTING


register = template.Library()


def sided_printing(sided_printing_2_find):
    for sided_printing, sided_printing_name in SIDED_PRINTING:
        if sided_printing == sided_printing_2_find:
            return sided_printing_name
    return ''

register.filter('sided_printing', sided_printing)
