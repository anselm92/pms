from django.conf.urls import url
from django.urls import reverse

from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
]
