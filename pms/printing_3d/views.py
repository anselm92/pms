from printing.views import CreateOrderView
from .forms import Order3dForm
from .models import Order3d


class CreateCustomOrder3DView(CreateOrderView):
    template_name = "order/order_3d.html"
    form_class = Order3dForm
    model = Order3d
