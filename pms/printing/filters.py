from django_filters import FilterSet

from printing.models import Order


class OrdersFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'order_hash': ['contains'],
            'title': ['contains'],
            'status': ['exact'],
            'customer__first_name': ['contains'],
        }
