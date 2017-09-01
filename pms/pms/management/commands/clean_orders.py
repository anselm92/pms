from datetime import datetime, timedelta

from django.core.management import BaseCommand

from printing.models import Order


class Command(BaseCommand):
    help = 'Delete orders that have not been submitted'

    def handle(self, *args, **options):
        orders = Order.objects.filter(status=0, create_date__gte=datetime.now()-timedelta(hours=1))
        self.stdout.write('Deleting zombie orders...')
        for order in orders:
            self.stdout.write(f'Deleting {order.order_hash}')
        orders.delete()
        self.stdout.write('Done...')
