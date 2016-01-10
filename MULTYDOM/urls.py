from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
import sys


urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^cart/', include('cart.urls')),
               url(r'^management/', include('management.urls')),
               url(r'^', include('store.urls')),
               url(r'^ckeditor/', include('ckeditor.urls')),
               url(r'^captcha/', include('captcha.urls'))
               ]

if not sys.platform.startswith('linux'):
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
