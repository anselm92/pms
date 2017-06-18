from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

# Non-translated URLs
urlpatterns = [
    url(r'^admin/', admin.site.urls),
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
