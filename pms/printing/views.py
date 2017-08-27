import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, FormView, UpdateView

from printing.forms import ExternalCommentForm, ExternalCustomerForm, StaffCommentBaseForm
from printing.models import Order, StaffCustomer, Comment, ExternalCustomer


class HomeView(TemplateView):
    template_name = "printing/general/home.html"


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "printing/general/dashboard.html"
    permission_required = "printing.dashboard_show"


class ShowOrderDetailView(DetailView):
    template_name = "printing/order/order_overview.html"
    model = Order
    context_object_name = 'order'
    slug_url_kwarg = "order_hash"
    slug_field = "order_hash"

    def get_context_data(self, **kwargs):
        context = super(ShowOrderDetailView, self).get_context_data(**kwargs)
        query_filter = {'order': self.get_object()}
        query_filter.update({'public': True} if not self.request.user.is_authenticated() else {})
        context['comments'] = Comment.objects.filter(**query_filter)
        context['form'] = ExternalCommentForm() if not self.request.user.is_authenticated() else StaffCommentBaseForm()
        return context


class ShowOrderOverviewView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        view = ShowOrderDetailView.as_view()
        return view(request, *args, **kwargs)

    @staticmethod
    def post(request, *args, **kwargs):
        view = CreateStaffCommentView.as_view() if request.user.is_authenticated() else CreateExternalCommentView.as_view()
        return view(request, *args, **kwargs)


class CreateOrderView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    success_message = "Order '%(title)s' was sent successful"
    login_url = reverse_lazy('printing:register_customer')

    def test_func(self):
        token = self.kwargs['order_token']
        customers = ExternalCustomer.objects.filter(order_token=token)
        return True if (len(token) > 0 and len(customers) > 0 or self.request.user.is_authenticated()) else False

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.object.order_hash})

    def form_valid(self, form):
        is_authenticated = self.request.user.is_authenticated()
        token = self.kwargs['order_token']
        order: Order = form.save(commit=False)
        order.customer = StaffCustomer.objects.get(
            user=self.request.user) if is_authenticated else ExternalCustomer.objects.get(order_token=token)
        return super(CreateOrderView, self).form_valid(form)


class CreateExternalCustomerView(FormView):
    template_name = "printing/general/create_customer.html"
    form_class = ExternalCustomerForm
    object = None

    def get_success_url(self):
        token = self.object.order_token
        return self.request.GET.get('next') + token

    def form_invalid(self, form):
        return super(CreateExternalCustomerView, self).form_invalid(form)

    def form_valid(self, form):
        customer, exists = ExternalCustomer.objects.get_or_create(first_name=form.cleaned_data['first_name'],
                                                                  last_name=form.cleaned_data['last_name'],
                                                                  mail_address=form.cleaned_data['mail_address'])
        customer.order_token = secrets.token_urlsafe(20)
        customer.save()
        self.object = customer
        return HttpResponseRedirect(self.get_success_url())


class CreateExternalCommentView(FormView):
    template_name = "printing/order/order_overview.html"
    form_class = ExternalCommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.public = True
        comment.order = Order.objects.get(order_hash=self.kwargs['order_hash'])
        comment.customer = ExternalCustomer.objects.get_or_create(first_name=form.cleaned_data['first_name'],
                                                                  last_name=form.cleaned_data['last_name'],
                                                                  mail_address=form.cleaned_data['mail_address'])[0]
        comment.save()
        return super(CreateExternalCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.kwargs['order_hash']})


class CreateStaffCommentView(FormView):
    template_name = "printing/order/order_overview.html"
    form_class = StaffCommentBaseForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.order = Order.objects.get(order_hash=self.kwargs['order_hash'])
        comment.user = self.request.user
        comment.save()
        return super(CreateStaffCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.kwargs['order_hash']})
