from django.conf.urls import url

from printing.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
]
