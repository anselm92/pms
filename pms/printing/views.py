import secrets

import os
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.template import RequestContext, loader
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, FormView, UpdateView, DeleteView, ListView

from pms import settings
from printing.filters import OrdersFilter
from printing.forms import ExternalCommentForm, ExternalCustomerForm, StaffCommentBaseForm, OrderBaseForm
from printing.handlers import CONTENT_TYPES, convert_pdf_to_png, convert_stl_to_png
from printing.models import Order, StaffCustomer, Comment, ExternalCustomer, Subscription, OrderHistoryEntry, \
    ORDER_STATUS_OPEN, ORDER_STATUS_PENDING
from printing.utils import CommentEmail


class HomeView(TemplateView):
    template_name = "printing/general/home.html"


class SubscriptionView:
    def subscribe(self, order, customer):
        subscription, created = Subscription.objects.get_or_create(order=order, customer=customer)
        subscription.save()

    def send_mail(self, order, customer):
        subscriptions = Subscription.objects.filter(order=order).exclude(customer=customer)
        for subscription in subscriptions:
            mail = CommentEmail(order, subscription)
            mail.send()


class ShowOrderDetailView(DetailView):
    template_name = "printing/order/order_overview.html"
    model = Order
    context_object_name = 'order'
    slug_url_kwarg = "order_hash"
    slug_field = "order_hash"

    def get_queryset(self):
        qs = super(ShowOrderDetailView, self).get_queryset()
        return qs.filter(status__gt=0)

    def get_context_data(self, **kwargs):
        context = super(ShowOrderDetailView, self).get_context_data(**kwargs)

        query_filter = {'order': self.get_object()}
        query_filter.update({'public': True} if not self.request.user.is_authenticated() else {})
        context['comments'] = Comment.objects.filter(**query_filter)

        query_filter = {'order': self.get_object()}
        context['history'] = OrderHistoryEntry.objects.filter(**query_filter)

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


class CreateOrderView(UserPassesTestMixin, SuccessMessageMixin, CreateView, SubscriptionView):
    login_url = reverse_lazy('printing:register_customer')

    def test_func(self):
        token = self.kwargs['order_token']
        customers = ExternalCustomer.objects.filter(order_token=token)
        return True if (len(token) > 0 and len(customers) > 0 or self.request.user.is_authenticated()) else False

    def get_success_url(self):
        return reverse('printing:preview', kwargs={'order_hash': self.object.order_hash})

    def form_valid(self, form):
        is_authenticated = self.request.user.is_authenticated()
        token = self.kwargs['order_token']
        order: Order = form.save(commit=False)
        order.file_name = form.cleaned_data['file']
        if is_authenticated:
            order.customer, _ = StaffCustomer.objects.get_or_create(first_name=self.request.user.first_name,
                                                                    last_name=self.request.user.last_name,
                                                                    mail_address=self.request.user.email,
                                                                    user=self.request.user)
        else:
            ExternalCustomer.objects.get(order_token=token)
        order.save()
        if self.is_pdf(order.file.path):
            convert_pdf_to_png(order.file.path)
        if self.is_stl(order.file.path):
            convert_stl_to_png(order.file.path)

        self.subscribe(order, order.customer)
        return super(CreateOrderView, self).form_valid(form)

    def is_pdf(self, path):
        return os.path.splitext(path)[1] == '.pdf'

    def is_stl(self, path):
        return os.path.splitext(path)[1] == '.stl'


class CreateExternalCustomerView(FormView):
    template_name = "printing/general/create_customer.html"
    form_class = ExternalCustomerForm
    object = None

    def get_success_url(self):
        token = self.object.order_token
        return self.request.GET.get('next') + token

    def form_valid(self, form):
        customer, exists = ExternalCustomer.objects.get_or_create(first_name=form.cleaned_data['first_name'],
                                                                  last_name=form.cleaned_data['last_name'],
                                                                  mail_address=form.cleaned_data['mail_address'])
        customer.order_token = secrets.token_urlsafe(20)
        customer.save()
        self.object = customer
        return HttpResponseRedirect(self.get_success_url())


class CreateExternalCommentView(FormView, SubscriptionView):
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
        self.subscribe(comment.order, comment.customer)
        self.send_mail(comment.order, comment.customer)
        return super(CreateExternalCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.kwargs['order_hash']})


class CreateStaffCommentView(FormView, SubscriptionView):
    template_name = "printing/order/order_overview.html"
    form_class = StaffCommentBaseForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.order = Order.objects.get(order_hash=self.kwargs['order_hash'])
        comment.user = self.request.user
        comment.save()
        staff_customer = StaffCustomer.objects.get(user=comment.user)
        self.subscribe(comment.order, staff_customer)
        self.send_mail(comment.order, staff_customer) if comment.public else None
        return super(CreateStaffCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.kwargs['order_hash']})


class UnsubscribeFromOrder(DeleteView):
    model = Subscription
    slug_url_kwarg = "token"
    slug_field = "token"
    context_object_name = 'subscription'
    template_name = 'printing/order/unsubscribe.html'
    success_url = reverse_lazy('printing:unsubscribe_successful')


class UnsubscribeFromOrderSuccessful(TemplateView):
    template_name = 'printing/order/unsubscribe_successful.html'


class ShowAllOrdersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'printing/order/all_orders.html'
    paginate_by = 20
    permission_required = "printing.dashboard_show"

    def _get_url_page(self, url_list, page):
        paginator = Paginator(url_list, self.paginate_by)
        try:
            url_list = paginator.page(page)
        except PageNotAnInteger:
            url_list = paginator.page(1)
        except EmptyPage:
            url_list = paginator.page(paginator.num_pages)
        return url_list

    def get_context_data(self, **kwargs):
        context = super(ShowAllOrdersView, self).get_context_data(**kwargs)
        url_list = Order.objects.order_by('-create_date').filter(status__gt=0)

        url_filter = OrdersFilter(self.request.GET, queryset=url_list)
        context['url_list'] = self._get_url_page(url_filter.qs,
                                                 self.request.GET.get('page'))
        context['url_filter'] = url_filter
        return context


class PreviewOrderView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'printing/order/order_preview.html'
    model = Order
    slug_url_kwarg = "order_hash"
    slug_field = "order_hash"
    success_message = "Order was sent successful"
    fields = []

    def test_func(self):
        token = self.kwargs['order_hash']
        customers = ExternalCustomer.objects.filter(order_token=token)
        return True if (((len(token) > 0 and len(
            customers) > 0 or self.request.user.is_authenticated()) and self.get_object().status == ORDER_STATUS_PENDING)) else False

    def form_valid(self, form):
        order: Order = form.save(commit=False)
        order.status = ORDER_STATUS_OPEN
        order.save()
        return super(PreviewOrderView, self).form_valid(form)

    def get_success_url(self):
        return reverse('printing:overview', kwargs={'order_hash': self.object.order_hash})

    def get_login_url(self):
        return reverse('printing:404')


class ServeOrderFiles(View):
    def get(self, request, order_hash, file):
        path = os.path.join(settings.FILES_ROOT, order_hash, file)
        if os.path.isfile(path):
            file_extension = os.path.splitext(path)[1].lower()
            image_data = open(path, "rb").read()
            content_type = CONTENT_TYPES.get(file_extension)
            if not content_type:
                content_type = 'application/' + file_extension[1:]
            return HttpResponse(image_data, content_type=content_type)
        return self.raise_404(request)

    def post(self, request):
        return HttpResponseNotAllowed('GET')

    def raise_404(self, request):
        t = loader.get_template('errors/404.html')
        return HttpResponseNotFound(t.render({}))
