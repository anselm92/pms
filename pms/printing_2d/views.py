# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView, CreateView

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


class CustomOrder2dView(LoginRequiredMixin, CreateView):
    template_name = "order_custom.html"
    form_class = CustomOrder2dForm
    success_url = 'success'
    model = CustomOrder2d

    def get_success_url(self):
        return reverse('printing:printing_2d:success', kwargs={'order_id': self.object.id})

    def form_valid(self, form):
        order: CustomOrder2d = form.save(commit=False)
        order.customer = StaffCustomer.objects.get(user=self.request.user)
        return super(CustomOrder2dView, self).form_valid(form)


class SuccessView(TemplateView):
    template_name = "order_success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        order = Order.objects.get(id=kwargs['order_id'])
        context['order'] = order
        return context
