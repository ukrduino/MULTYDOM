from django.shortcuts import render_to_response
from store.models import *
from django.template import RequestContext
from MULTYDOM.settings import SITE_ADDR


args = dict()
args['SITE_ADDR'] = SITE_ADDR



def product(request, product_id=1):
    args['product'] = Product.objects.get(id=product_id)

    return render_to_response('product.html', args, context_instance=RequestContext(request))


def actions(request):
    return render_to_response('actions.html', )


def categories(request):

    args['categories'] = Category.objects.filter(parentCategory=None)

    return render_to_response('categories.html', args, context_instance=RequestContext(request))

#TODO - сделать универсальный фильтр (категории,товары,бренды)


def category_filter(request, category_id):

    cats = Category.objects.filter(parentCategory_id=category_id)

    if len(cats) > 0:
        args['categories'] = cats

    else:
        args['products'] = Product.objects.filter(productCategory_id=category_id)
        return render_to_response('products.html', args, context_instance=RequestContext(request))

    return render_to_response('categories.html', args, context_instance=RequestContext(request))


def brands(request):
    args['brands'] = Manufacturer.objects.all()
    return render_to_response('brands.html', args, context_instance=RequestContext(request))


def brand_filter(request, brand_id):
    args['products'] = Product.objects.filter(productManufacturer_id=brand_id)

    return render_to_response('products.html', args, context_instance=RequestContext(request))


def docs(request):
    return render_to_response('docs.html',)


def about(request):
    return render_to_response('about.html',)
