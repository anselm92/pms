from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse

from printing.views import DashboardView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name="home"),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='printing/login.html'), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name='printing/logout.html'), name='logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
]
