from django.shortcuts import render_to_response
from store.models import *
from django.template import RequestContext
from MULTYDOM.settings import SITE_ADDR


def product(request, product_id=1):
    args = dict()
    args['SITE_ADDR'] = SITE_ADDR
    args['product'] = Product.objects.get(id=product_id)
    args['nodes'] = Category.objects.all()

    return render_to_response('product.html', args, context_instance=RequestContext(request))


def actions(request):
    return render_to_response('actions.html', )


def categories(request):
    args = dict()
    args['SITE_ADDR'] = SITE_ADDR
    args['categories'] = Category.objects.filter(parent_id=None)
    args['nodes'] = Category.objects.all()
    return render_to_response('categories.html', args, context_instance=RequestContext(request))

#TODO - сделать универсальный фильтр (категории,товары,бренды)
#TODO - не выводить категории без товаров
#TODO - изменение цены товара из админки


def category_filter(request, category_id):
    args = dict()
    args['SITE_ADDR'] = SITE_ADDR
    cats = Category.objects.filter(parent_id=category_id)

    if len(cats) > 0:
        args['categories'] = cats
        args['nodes'] = Category.objects.all()

    else:
        args['products'] = Product.objects.filter(productCategory_id=category_id)
        args['nodes'] = Category.objects.all()

        return render_to_response('products.html', args, context_instance=RequestContext(request))

    return render_to_response('categories.html', args, context_instance=RequestContext(request))


def brands(request):
    args = dict()
    args['SITE_ADDR'] = SITE_ADDR
    args['brands'] = Manufacturer.objects.all()
    args['nodes'] = Category.objects.all()
    return render_to_response('brands.html', args, context_instance=RequestContext(request))


def brand_filter(request, brand_id):
    args = dict()
    args['SITE_ADDR'] = SITE_ADDR
    args['products'] = Product.objects.filter(productManufacturer_id=brand_id)

    return render_to_response('products.html', args, context_instance=RequestContext(request))


def docs(request):
    return render_to_response('docs.html',)


def about(request):
    return render_to_response('about.html',)


# def category_page(request, category_id):
#     #getting detail information about current object
#     current_category = Category.objects.get(id=category_id)
#     root_category_id = current_category.get_root().id
#     #render
#     return render_to_response("category_page.html",
#                           {
#                               'nodes':Category.objects.all(),
#                               'current_category':current_category,
#                               'root_category_id':root_category_id
#                           },
#                           context_instance=RequestContext(request))