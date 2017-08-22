# Create your views here.
from django.views.generic import TemplateView

from printing.views import CreateOrderView
from printing_2d.forms import ScriptOrderForm, CustomOrder2dForm
from printing_2d.models import ScriptOrder, CustomOrder2d


class HomeView(TemplateView):
    template_name = "general/index.html"


class CreateScriptOrderView(CreateOrderView):
    template_name = "order/order_script.html"
    form_class = ScriptOrderForm
    model = ScriptOrder


class CreateCustomOrder2DView(CreateOrderView):
    template_name = "order/order_custom.html"
    form_class = CustomOrder2dForm
    model = CustomOrder2d
