from django.urls import reverse

from printing.views import CreateOrderView, PreviewOrderView, ShowOrderDetailView, ShowOrderOverviewView
from .forms import Order3dForm
from .models import Order3d


class CreateCustomOrder3DView(CreateOrderView):
    template_name = "order/order_3d.html"
    form_class = Order3dForm
    model = Order3d

    def get_success_url(self):
        return reverse('printing:printing_3d:preview', kwargs={'order_hash': self.object.order_hash})


class Preview3dOrderView(PreviewOrderView):
    model = Order3d
    fields = ['width', 'depth', 'height']
    context_object_name = 'order'


class Order3dDetailView(ShowOrderDetailView):
    model = Order3d
    fields = ShowOrderDetailView.fields + ['chargeable_weight','junk_weight']


class ShowOrder3dOverviewView(ShowOrderOverviewView):
    get_view = Order3dDetailView
