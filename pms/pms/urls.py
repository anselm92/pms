from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from printing.serializer import OrderViewSet, CustomerViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'users', UserViewSet)

# Non-translated URLs
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token)
]

# Translated URLs
translated_urls = ([
    url(r'^', include('printing.urls')),
])

urlpatterns += i18n_patterns(
    url(r'^', include(translated_urls, namespace='printing')),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
