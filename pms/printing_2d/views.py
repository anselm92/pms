# Create your views here.
from django.views.generic import TemplateView

from printing.views import OrderView
from printing_2d.forms import ScriptOrderForm, CustomOrder2dForm
from printing_2d.models import ScriptOrder, CustomOrder2d


class HomeView(TemplateView):
    template_name = "general/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ScriptOrderView(OrderView):
    template_name = "order/order_script.html"
    form_class = ScriptOrderForm
    model = ScriptOrder

    def form_valid(self, form):
        return super(ScriptOrderView, self).form_valid(form)


class CustomOrder2dView(OrderView):
    template_name = "order/order_custom.html"
    form_class = CustomOrder2dForm
    model = CustomOrder2d

    def form_valid(self, form):
        return super(CustomOrder2dView, self).form_valid(form)
