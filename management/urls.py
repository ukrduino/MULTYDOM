from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from management.views import *

urlpatterns = [
               url(r'newDollar', newDollar, name='newDollar'),
               url(r'newPriceIndex', newPriceIndex, name='newPriceIndex'),
               url(r'login', user_login, name='user_login'),
               # переход на менеджерскую страницу с других страниц
               url(r'$', management, name='management'),
               ]


