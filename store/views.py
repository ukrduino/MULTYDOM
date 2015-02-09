from django.shortcuts import render_to_response, redirect, HttpResponse
from store.models import *  # импортируем модели
# #from django.core.exceptions import ObjectDoesNotExist  # ошибка - объект не существует
# #from django.http.response import Http404  # вывод страницы 404
# from store.forms import CommentForm
# from django.core.context_processors import csrf  # защита данных передаваемых из форм
# #from django.contrib import auth   # модуль авторизации
from django.template import RequestContext
# from django.contrib import messages
from MULTYDOM.localSettings import SITE_ADDR

args = dict()
args['categories'] = Category.objects.all()
args['SITE_ADDR'] = SITE_ADDR


def product(request, product_id=1):
    args['product'] = Product.objects.get(id=product_id)

    return render_to_response('product.html', args, context_instance=RequestContext(request))


def actions(request):
    return render_to_response('actions.html', )


def categories(request):
    return render_to_response('categories.html', args, context_instance=RequestContext(request))


def category_filter(request, category_id):
    args['products'] = Product.objects.filter(productCategory_id=category_id)

    return render_to_response('products.html', args, context_instance=RequestContext(request))


def paymentDelivery(request):

    return render_to_response('paymentDelivery.html',)


def docs(request):
    return render_to_response('docs.html',)


def about(request):
    return render_to_response('about.html',)


# def products(request):
#     return render_to_response('products.html',)
#
#
# def filter3(request, roast):
#
#     args = dict()
#     kwargs = dict()
#
#     kwargs['product_сoffe_roast'] = roast
#
#     args['manufacturers'] = Manufacturer.objects.all()
#     args['products'] = Coffe.objects.filter(**kwargs)
#     request.session['selection_type'] = "Обжарка " + roast
#
#     return render_to_response('actions.html', args, context_instance=RequestContext(request))
#
#
# from django.views.static import serve
#
#
# def text(request):
#
#   f = open("/Users/Sergey/PycharmProjects/SHOP/static/textfile.txt", 'r')
#
#   return HttpResponse(f)

# def add_comment(request, product_id=1):
#     if 'pause' in request.session:
#         messages.error(request, 'Комментарий не опубликован!!! Вы оставили предидущий комментарий менее '
#                                 '1 минуты назад.')
#
#     if request.POST and ('pause' not in request.session):
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.comment_product = Coffe.objects.get(id=product_id)
#             form.save()
#             messages.success(request, 'Спасибо за Ваш комментарий!')
#             request.session.set_expiry(60)  # создает объект сессии и настраивает срок ее действия -60 секунд
#             request.session['pause'] = True  # Внутри сессии создает переменную 'pause' равную TRUE.
#         else:
#             messages.error(request, 'Сообщение не опубликовано!!!    Вы неправильно ответили '
#                                     'на вопрос проверки или оставили сообщение менее '
#                                     '1 минуты назад.')
#     return redirect('/%s' % product_id)
#
#
# def filter1(request, man_id):
#
#     args = dict()
#     kwargs = dict()
#     kwargs['product_manuf_id'] = man_id
#     args['manufacturers'] = Manufacturer.objects.all()
#     args['products'] = Coffe.objects.filter(**kwargs)
#     manufacturer = Manufacturer.objects.get(id=man_id)
#     request.session['selection_type'] = "Производитель " + manufacturer.title
#
#     return render_to_response('actions.html', args, context_instance=RequestContext(request))
#
#

