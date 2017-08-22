from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from printing.views import DashboardView, HomeView, OrderOverviewView
from printing_2d import urls as urls_2d_printing

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='printing/general/login.html'), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name='printing/general/logout.html'),
        name='logout'),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    url(r'^order/(?P<order_hash>[\S0-9_.-\\s\- ]*)', OrderOverviewView.as_view(), name="overview"),
    url(r'^printing_2d/', include(urls_2d_printing.urlpatterns, namespace="printing_2d"), ),

]
