from django.conf.urls import url

from .views import *

app_name = 'printing_3d'

urlpatterns = [
    url(r'^order/3d/(?P<order_token>[\S0-9_.-\\s\- ]*)$', CreateCustomOrder3DView.as_view(), name="order_3d"),
    url(r'^preview/(?P<order_hash>[\S0-9_.-\\s\- ]*)$', Preview3dOrderView.as_view(), name="preview"),
    url(r'^order/(?P<order_hash>[\S0-9_.-\\s\- ]*)/update/$', Order3dDetailView.as_view(),
        name="order3d_update"),
    url(r'^order/(?P<order_hash>[\S0-9_.-\\s\- ]*)/$', ShowOrder3dOverviewView.as_view(), name="order3d_overview"),

]
