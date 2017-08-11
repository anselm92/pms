from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class HomeView(TemplateView):
    template_name = "printing/home.html"


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "printing/dashboard.html"
    permission_required = "printing.dashboard_show"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        #context['latest_articles'] = Article.objects.all()[:5]
        return context