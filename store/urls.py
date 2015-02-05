from django.conf.urls import patterns, url
# from store.models import Coffe
# from django.views.generic import TemplateView, ListView


urlpatterns = patterns('',
                       # url(r'^(?P<product_id>\d+)$', 'store.views.coffe_detail', name='coffe_detail'),
                       # # url(r'^filter/(?P<man_id>\d+)$', 'store.views.manufecturer_filter', name='man_filter'),
                       # # url(r'^filter/(?P<sort>)', 'store.views.sort_filter', name='sort_filter'),
                       # url(r'^add_comment/(?P<product_id>\d+)$', 'store.views.add_comment', name='comment'),
                       # # url(r'^$', ListView.as_view(model = Coffe, template_name = "actions.html"), name='home'),
                       url(r'^$', 'store.views.actions',  name="actions"),
                       url(r'^store/$', 'store.views.store',  name="store"),
                       url(r'^paymentDelivery/$', 'store.views.paymentDelivery',  name="paymentDelivery"),
                       url(r'^docs/$', 'store.views.docs',  name="docs"),
                       url(r'^about/$', 'store.views.about',  name="about"),

                       # url(r'^filter3/(?P<roast>\w+)$', 'store.views.filter3',  name="filter3"),
                       # url(r'^filter2/(?P<sort_id>\d+)$', 'store.views.filter2',  name="filter2"),
                       # url(r'^filter1/(?P<man_id>\d+)$', 'store.views.filter1',  name="filter1"),
                       # url(r'^text/$', 'store.views.text',  name="text"),
                       )