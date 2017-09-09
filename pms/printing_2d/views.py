# Create your views here.
from django.views.generic import TemplateView

from printing.mixins import PermissionPostGetRequiredMixin
from printing.views import CreateOrderView
from printing_2d.forms import ScriptOrderForm, CustomOrder2dForm
from printing_2d.models import ScriptOrder, CustomOrder2d


class HomeView(TemplateView):
    template_name = "general/index.html"


class CreateScriptOrderView(PermissionPostGetRequiredMixin, CreateOrderView):
    template_name = "order/order_script.html"
    form_class = ScriptOrderForm
    model = ScriptOrder
    permission_get_required = ["printing_2d.add_scriptorder"]
    permission_post_required = ["printing_2d.add_scriptorder"]


class CreateCustomOrder2DView(PermissionPostGetRequiredMixin, CreateOrderView):
    template_name = "order/order_custom.html"
    form_class = CustomOrder2dForm
    model = CustomOrder2d
    permission_get_required = ["printing_2d.add_customorder2d"]
    permission_post_required = ["printing_2d.add_customorder2d"]
