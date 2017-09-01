from django.core.management import BaseCommand

from printing.models import Order


class Command(BaseCommand):
    help = 'Delete orders that have not been submitted'

    def handle(self, *args, **options):
        orders = Order.objects.filter(status=0)
        self.stdout.write('Deleting zombie orders...')
        for order in orders:
            self.stdout.write(f'Deleting {order.order_hash}')
        orders.delete()
        self.stdout.write('Done...')
