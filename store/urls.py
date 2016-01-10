from django.conf.urls import url
from store.views import *

urlpatterns = [
               url(r'^$', actions,  name="actions"),
               url(r'^categories/$', categories,  name="categories"),
               url(r'^brands/$', brands,  name="brands"),
               url(r'^categories/filter/(?P<category_id>\d+)$', category_filter,
                   name='category_filter'),
               url(r'^brands/filter/(?P<brand_id>\d+)$', brand_filter,
                   name='brand_filter'),
               url(r'^product/(?P<product_id>\d+)$', product,  name="product"),
               url(r'^docs/$', docs,  name="docs"),
               url(r'^about/$', about,  name="about"),
            ]
