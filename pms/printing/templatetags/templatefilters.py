from django import template
from printing.models import ORDER_STATUS


register = template.Library()


def order_status(status_2_find):
    """Removes all values of arg from the given string"""
    for status, status_name in ORDER_STATUS:
        if status == status_2_find:
            return status_name
    return ''

register.filter('order_status', order_status)
