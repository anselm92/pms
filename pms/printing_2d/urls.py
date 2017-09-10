from django.conf.urls import url

from .views import *

app_name = 'printing_2d'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^order/script/(?P<order_token>[\S0-9_.-\\s\- ]*)$', CreateScriptOrderView.as_view(), name="script"),
    url(r'^order/custom/(?P<order_token>[\S0-9_.-\\s\- ]*)$', CreateCustomOrder2DView.as_view(), name="custom"),
    url(r'^custom/(?P<order_hash>[\S0-9_.-\\s\- ]*)/update/$', CustomOrder2dDetailView.as_view(),
        name="customorder2d_update"),
    url(r'^script/(?P<order_hash>[\S0-9_.-\\s\- ]*)/update/$', ScriptOrderDetailView.as_view(),
        name="scriptorder_update"),
    url(r'^custom/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', ShowCustomOrder2dOverviewView.as_view(),
        name="customorder2d_overview"),
    url(r'^script/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', ShowScriptOrderOverviewView.as_view(),
        name="scriptorder_overview"),

]
