from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = "printing/home.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "printing/dashboard.html"

