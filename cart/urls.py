from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('cart.views',

                       # добавление товара в корзину
                       url(r'add_product/(?P<product_id>\d+)$', 'add_to_cart_main', name='add_main'),
                       # товар в корзине ++
                       url(r'cart_add_product/(?P<product_id>\d+)$', 'add_to_cart', name='add'),
                       # товар  в корзине --
                       url(r'cart_rem_product/(?P<product_id>\d+)$', 'rem_from_cart', name='rem'),
                       # оформить заказ
                       url(r'make_order$', 'make_order', name='make_order'),
                       # заказ создан
                       url(r'order_created/$', TemplateView.as_view(template_name='order_created.html'),
                           name="order_created"),
                       # подтвердить заказ
                       url(r'confirm_order/(?P<order_code>\d+)$', 'confirm_order', name='confirm_order'),
                       # заказ подтвержден
                       url(r'order_confirmed/$', TemplateView.as_view(template_name='order_confirmed.html'),
                           name="order_confirmed"),
                       # переход в карзину с других страниц
                       url(r'$', 'cart', name='my_cart'),
                       )
