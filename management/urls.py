from django.conf.urls import url, patterns
from django.views.generic import TemplateView


urlpatterns = patterns('management.views',

                       url(r'newDollar', 'newDollar', name='newDollar'),
                       url(r'newPriceIndex', 'newPriceIndex', name='newPriceIndex'),
                       url(r'login', 'user_login', name='user_login'),
                       # переход на менеджерскую страницу с других страниц
                       url(r'$', 'management', name='management'),

                       )


                       # # добавление товара в корзину
                       # url(r'add_product/(?P<product_id>\d+)$', 'add_to_cart_main', name='add_main'),
                       # # товар в корзине ++
                       # url(r'cart_add_product/(?P<product_id>\d+)$', 'add_to_cart', name='add'),
                       # # товар  в корзине --
                       # url(r'cart_rem_product/(?P<product_id>\d+)$', 'rem_from_cart', name='rem'),
                       # # оформить заказ
                       # # заказ создан
                       # url(r'order_created/$', TemplateView.as_view(template_name='order_created.html'),
                       #     name="order_created"),
                       # # подтвердить заказ
                       # url(r'confirm_order/(?P<order_code>\d+)$', 'confirm_order', name='confirm_order'),
                       # # заказ подтвержден
                       # url(r'order_confirmed/$', TemplateView.as_view(template_name='order_confirmed.html'),
                       #     name="order_confirmed"),



