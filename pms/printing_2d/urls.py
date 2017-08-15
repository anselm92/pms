from django.conf.urls import url
from django.urls import reverse

from .views import *

app_name = 'printing_2d'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^order/script$', ScriptOrderView.as_view(), name="script"),
    url(r'^order/custom$', CustomOrder2dView.as_view(), name="custom"),
    url(r'^order/(?P<order_hash>[\S0-9_.-\\s\- ]*)', OrderView.as_view(), name="overview"),
]
