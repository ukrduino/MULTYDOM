from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', 'store.views.actions',  name="actions"),
                       url(r'^categories/$', 'store.views.categories',  name="categories"),
                       url(r'^brands/$', 'store.views.brands',  name="brands"),
                       url(r'^categories/filter/(?P<category_id>\d+)$', 'store.views.category_filter',
                           name='category_filter'),
                       url(r'^product/(?P<product_id>\d+)$', 'store.views.product',  name="product"),
                       url(r'^docs/$', 'store.views.docs',  name="docs"),
                       url(r'^about/$', 'store.views.about',  name="about"),
                       )