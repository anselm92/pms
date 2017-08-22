from django.conf.urls import url

from .views import *

app_name = 'printing_2d'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^order/script$', CreateScriptOrderView.as_view(), name="script"),
    url(r'^order/custom$', CreateCustomOrder2DView.as_view(), name="custom"),
]
