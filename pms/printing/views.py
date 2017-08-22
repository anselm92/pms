from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, FormView

from printing.forms import ExternalCommentForm
from printing.models import Order, StaffCustomer, Comment, ExternalCustomer


class HomeView(TemplateView):
    template_name = "printing/general/home.html"


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "printing/general/dashboard.html"
    permission_required = "printing.dashboard_show"


class CreateOrderView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    success_message = "Order '%(title)s' was sent successful"

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.object.order_hash})

    def form_valid(self, form):
        order: Order = form.save(commit=False)
        order.customer = StaffCustomer.objects.get(user=self.request.user)
        return super(CreateOrderView, self).form_valid(form)


class OrderDetailView(DetailView):
    template_name = "printing/order/order_overview.html"
    model = Order
    context_object_name = 'order'
    slug_url_kwarg = "order_hash"
    slug_field = "order_hash"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(order=self.get_object())[:5]
        context['comment_form'] = ExternalCommentForm()
        return context


class ExternalCommentView(FormView):
    template_name = "printing/order/order_overview.html"
    form_class = ExternalCommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.order = Order.objects.get(order_hash=self.kwargs['order_hash'])
        comment.customer = ExternalCustomer.objects.get(id=1)
        comment.save()
        return super(ExternalCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.kwargs['order_hash']})


class OrderOverviewView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        view = OrderDetailView.as_view()
        return view(request, *args, **kwargs)

    @staticmethod
    def post(request, *args, **kwargs):
        view = ExternalCommentView.as_view()
        return view(request, *args, **kwargs)
