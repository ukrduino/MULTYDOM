from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^cart/', include('cart.urls')),
                       url(r'^management/', include('management.urls')),
                       url(r'^', include('store.urls')),
                       )

urlpatterns += patterns('', url(r'^captcha/', include('captcha.urls')),)

# comment on pythonanywhere
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )