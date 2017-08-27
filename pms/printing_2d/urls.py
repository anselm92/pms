from django.conf.urls import url

from .views import *

app_name = 'printing_2d'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^order/script/(?P<order_token>[\S0-9_.-\\s\- ]*)$', CreateScriptOrderView.as_view(), name="script"),
    url(r'^order/custom/(?P<order_token>[\S0-9_.-\\s\- ]*)$', CreateCustomOrder2DView.as_view(), name="custom"),
]
