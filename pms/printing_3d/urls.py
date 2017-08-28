from django.conf.urls import url

from .views import *

app_name = 'printing_3d'

urlpatterns = [
    url(r'^order/3d/(?P<order_token>[\S0-9_.-\\s\- ]*)$', CreateCustomOrder3DView.as_view(), name="order_3d"),
]
