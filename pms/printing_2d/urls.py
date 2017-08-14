from django.conf.urls import url
from django.urls import reverse

from .views import *

app_name = 'printing_2d'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^order/script$', ScriptOrderView.as_view(), name="order/script"),
    url(r'^order/custom$', CustomOrder2dView.as_view(), name="order/custom"),
    url(r'^order/success/(?P<order_id>[\S0-9_.-\\s\- ]*)', SuccessView.as_view(), name="success"),
]
