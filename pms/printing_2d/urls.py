from django.conf.urls import url

from .views import *

app_name = 'printing_2d'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^order/script$', ScriptOrderView.as_view(), name="script"),
    url(r'^order/custom$', CustomOrder2dView.as_view(), name="custom"),
]
