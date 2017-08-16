from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from printing.models import Order, StaffCustomer


class HomeView(TemplateView):
    template_name = "printing/general/home.html"


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "printing/general/dashboard.html"
    permission_required = "printing.dashboard_show"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context


class OrderView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    success_message = "Order '%(title)s' was sent successful"

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.object.order_hash})

    def form_valid(self, form):
        order: Order = form.save(commit=False)
        order.customer = StaffCustomer.objects.get(user=self.request.user)
        return super(OrderView, self).form_valid(form)


class OrderOverviewView(DetailView):
    template_name = "printing/order/order_overview.html"
    model = Order
    context_object_name = 'order'
    slug_url_kwarg = "order_hash"
    slug_field = "order_hash"
