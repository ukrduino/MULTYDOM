from django.shortcuts import render_to_response, redirect
from store.models import Product
from cart.models import Order
from django.http.response import HttpResponseRedirect
from cart.forms import OrderForm
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib import messages
from MULTYDOM.settings import DEFAULT_FROM_EMAIL, SITE_ADDR, DEFAULT_TO_EMAIL


#TODO всю корзину сделать на Ajax


def add_to_cart_main(request, product_id=1):

    if request.session.get('prods_in_cart'):
        prods_in_cart = request.session.get('prods_in_cart')
        prods_in_cart.append(product_id)
        request.session['prods_in_cart'] = prods_in_cart
        group_prods_in_cart(request, prods_in_cart)
    else:
        prods_in_cart = list()
        prods_in_cart.append(product_id)
        request.session['prods_in_cart'] = prods_in_cart
        group_prods_in_cart(request, prods_in_cart)

    request.session['cart_qwt_of_prods'] = len(prods_in_cart)

    if request.session.get('cart_cost'):
        add_cart_cost = request.session['cart_cost']
        prod_to_add = Product.objects.get(id=product_id)
        add_cart_cost += prod_to_add.productCurrentPrice
        request.session['cart_cost'] = add_cart_cost
    else:
        add_cart_cost = 0
        prod_to_add = Product.objects.get(id=product_id)
        add_cart_cost += prod_to_add.productCurrentPrice
        request.session['cart_cost'] = add_cart_cost

    # http://stackoverflow.com/a/12758859/3177550
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def group_prods_in_cart(request, prods_in_cart):
    # группировка товаров... товаров с таким-то id  - 2,
    # с таким-то - 4...  для выписывания счета (создания заказа для сохренения в Б/д)

    prods_in_cart = prods_in_cart
    # создаем словарь для группировки id
    grouped_prods_in_cart = {}
    # для каждого элемента (назовем его prod) в списке prods_in_cart....
    for prod in prods_in_cart:  # http://samag.ru/archive/article/1581
        # если запись с ключем равным такому id(преобразованному в int) уже есть в списке prod_cart_checkout....
        if prod in grouped_prods_in_cart:
            # то увеличиваем ее (записи с ключем равным id товара из списка cart) значение на 1
            grouped_prods_in_cart[prod] += 1
        else:
            # если записи с таким ключем нет то создаем ее...
            grouped_prods_in_cart[prod] = 1

    # и сохраняем отсортированный словарь prod_cart_checkout в session в запись с ключем cart_checkout_items
    request.session['grouped_prods_in_cart'] = grouped_prods_in_cart


def add_to_cart(request, product_id):
    prods_in_cart = request.session.get('prods_in_cart')
    prods_in_cart.append(product_id)
    request.session['prods_in_cart'] = prods_in_cart
    group_prods_in_cart(request, prods_in_cart)

    request.session['cart_qwt_of_prods'] = len(prods_in_cart)

    add_cart_cost = request.session['cart_cost']
    prod_to_add = Product.objects.get(id=product_id)
    add_cart_cost += prod_to_add.productCurrentPrice
    request.session['cart_cost'] = add_cart_cost

    # http://stackoverflow.com/a/12758859/3177550
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def rem_from_cart(request, product_id):
    if product_id in request.session.get('prods_in_cart'):
        rem_usercart = request.session.get('prods_in_cart')
        rem_usercart.remove(product_id)
        request.session['prods_in_cart'] = rem_usercart
        group_prods_in_cart(request, rem_usercart)

        request.session['cart_qwt_of_prods'] = len(rem_usercart)

        rem_cart_cost = request.session.get('cart_cost')
        prod_to_rem = Product.objects.get(id=product_id)
        rem_cart_cost -= prod_to_rem.productCurrentPrice
        request.session['cart_cost'] = rem_cart_cost

    # http://stackoverflow.com/a/12758859/3177550
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cart(request):

    args = dict()

    args['products'] = Product.objects.all()
    args['form'] = OrderForm

    # Пример заполнения полей формы из контекста при создании формы
    # cart_cost = request.session.get('cart_cost')
    # form = OrderForm(initial={'order_sum': cart_cost})
    # args['form'] = form

    return render_to_response('cart.html', args, context_instance=RequestContext(request))


def make_order(request):

    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.order_products = ordered_products_titles(request.session.get('grouped_prods_in_cart'))
            add.order_sum = request.session.get('cart_cost')
            add.save()

            shop_email_subject = "Новый заказ !!!"
            shop_email_body = "Поступил новый заказ №%s!\n" \
                              "Покупатель - %s.\n" \
                              "Сумма заказа - %s грн.\n" \
                              "Товары:\n" \
                              "%s" \
                              % (add.order_code, add.order_person, add.order_sum, add.order_products)

            send_mail(shop_email_subject,
                      shop_email_body,
                      # отправитель магазин
                      DEFAULT_FROM_EMAIL,
                      # получатель хозяин магазина
                      [DEFAULT_TO_EMAIL],
                      fail_silently=False)

            conf_link = "%s/cart/confirm_order/%s" % (SITE_ADDR, add.order_code)
            buyer_email_subject = "Ваш заказ в магазине MultyDOM"
            buyer_email_body = "Добрый день уважаемый %s!!!\n" \
                               "Спасибо за Ваш заказ.\n"\
                               "Товары:\n" \
                               "%s" \
                               "Сумма заказа - %s грн.\n\n" \
                               "Для подтверждения заказа необходимо перейти по ссылке укзанной ниже\n" \
                               "%s" % (add.order_person, add.order_products, add.order_sum, conf_link)

            send_mail(buyer_email_subject,
                      buyer_email_body,
                      DEFAULT_FROM_EMAIL,
                      [add.order_person_email],
                      fail_silently=False)

            del request.session['cart_qwt_of_prods']
            del request.session['cart_cost']
            del request.session['grouped_prods_in_cart']
            del request.session['prods_in_cart']

            return render_to_response('order_created.html', {'email': add.order_person_email})

        else:
            messages.error(request, 'Ваш заказ НЕ ОФОРМЛЕН!!! Проверьте правильность введения '
                                    'данных и повторите заказ. ВСЕ поля НЕОБХОДИМО заполнить, '
                                    'а последнее поле - посчитать и вписать ответ!!!')

            return redirect('my_cart')


def confirm_order(request, order_code):

    order = Order.objects.get(order_code=order_code)
    order.order_confirmed = True
    order.save()
    shop_email_subject = "Заказ №%s - подтвержден!!!" % order_code
    shop_email_body = "Заказ №%s!\n" \
                      "Покупатель - %s.\n" \
                      "Телефон клиента - %s.\n" \
                      "Товары - %s.\n" \
                      "Сумма заказа - %s.\n " \
                      "Форма оплаты - %s.\n" \
                      "Адрес доставки - %s.\n" \
                      "Способ доставки - %s" \
                      % (order.order_code,
                         order.order_person,
                         order.order_person_phone,
                         order.order_products,
                         order.order_sum,
                         order.order_pay_option,
                         order.order_person_address,
                         order.order_delivery_option)

    send_mail(shop_email_subject, shop_email_body, DEFAULT_FROM_EMAIL, [DEFAULT_TO_EMAIL],
              fail_silently=False)

    return redirect('order_confirmed')


# http://stackoverflow.com/a/4406521
# http://stackoverflow.com/a/4406558
def ordered_products_titles(grouped_prods_in_cart):
    dict1 = grouped_prods_in_cart
    dict2 = {}
    for key in dict1.keys():
        product = Product.objects.get(id=int(key))
        dict2[product.productTitle] = dict1[key]

    order_products_formated_str = ""

    for keys, values in dict2.items():
        order_products_formated_str += "%s - %s шт; \n" % (keys, values)

    return order_products_formated_str