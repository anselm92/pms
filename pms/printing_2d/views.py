# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView

from printing.models import StaffCustomer, Order
from printing_2d.forms import ScriptOrderForm, CustomOrder2dForm
from printing_2d.models import ScriptOrder, CustomOrder2d


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ScriptOrderView(LoginRequiredMixin, CreateView):
    template_name = "order_script.html"
    form_class = ScriptOrderForm
    success_url = "."
    model = ScriptOrder

    def form_valid(self, form):
        order: ScriptOrder = form.save(commit=False)
        order.customer = StaffCustomer.objects.get(user=self.request.user)
        return super(ScriptOrderView, self).form_valid(form)


class CustomOrder2dView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "order_custom.html"
    form_class = CustomOrder2dForm
    success_url = 'overview'
    model = CustomOrder2d
    success_message = "Order '%(title)s' was sent successful"

    def get_success_url(self):
        return reverse('printing:printing_2d:overview', kwargs={'order_hash': self.object.order_hash})

    def form_valid(self, form):
        order: CustomOrder2d = form.save(commit=False)
        order.customer = StaffCustomer.objects.get(user=self.request.user)
        return super(CustomOrder2dView, self).form_valid(form)


class OrderView(DetailView):
    template_name = "order_overview.html"
    model = Order
    context_object_name = 'order'
    slug_url_kwarg = "order_hash"
    slug_field = "order_hash"
