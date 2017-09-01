from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from printing.views import HomeView, ShowOrderOverviewView, CreateExternalCustomerView, \
    UnsubscribeFromOrder, UnsubscribeFromOrderSuccessful, ShowAllOrdersView, ServeOrderFiles, PreviewOrderView, \
    ShowOrderDetailView, CancelOrderView
from printing_2d import urls as urls_2d_printing
from printing_3d import urls as urls_3d_printing

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='printing/general/login.html'), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name='printing/general/logout.html'),
        name='logout'),
    url(r'^register/$', CreateExternalCustomerView.as_view(), name="register_customer"),
    url(r'^media/(?P<order_hash>[\S0-9_.-\\s\- ]*)/(?P<file>[\S0-9_.-\\s\- ]*)$', ServeOrderFiles.as_view(),
        name="media"),
    url(r'^orders/$', ShowAllOrdersView.as_view(), name="all_orders"),
    url(r'^order/preview/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', PreviewOrderView.as_view(), name="preview"),
    url(r'^order/cancel/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', CancelOrderView.as_view(), name="cancel_order"),
    url(r'^order/update/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', ShowOrderDetailView.as_view(), name="update_order"),
    url(r'^order/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', ShowOrderOverviewView.as_view(), name="overview"),
    url(r'^unsubscribe/(?P<token>[\S0-9_.-\\s\- ]*)/$', UnsubscribeFromOrder.as_view(), name="unsubscribe"),
    url(r'^unsubscribe_successful/$', UnsubscribeFromOrderSuccessful.as_view(), name="unsubscribe_successful"),
    url(r'^printing_2d/', include(urls_2d_printing.urlpatterns, namespace="printing_2d")),
    url(r'^printing_3d/', include(urls_3d_printing.urlpatterns, namespace="printing_3d"))
]
