from django.shortcuts import render_to_response, render
from store.models import *
from django.template import RequestContext
from MULTYDOM.settings import SITE_ADDR


def product(request, product_id=1):
    args = dict()
    args['product'] = Product.objects.get(id=product_id)
    args['nodes'] = Category.objects.all()

    return render(request, 'product.html', args)


def actions(request):
    return render(request, 'actions.html')


def categories(request):
    args = dict()
    args['categories'] = Category.objects.filter(parent_id=None)
    args['nodes'] = Category.objects.all()
    return render(request, 'categories.html', args)


def category_filter(request, category_id):
    args = dict()
    args['SITE_ADDR'] = SITE_ADDR
    cats = Category.objects.filter(parent_id=category_id)
    args['nodes'] = Category.objects.all()

    if len(cats) > 0:
        args['categories'] = cats

    else:
        args['products'] = Product.objects.filter(productCategory_id=category_id)

        return render(request, 'products.html', args)

    return render(request, 'categories.html', args)


def brands(request):
    args = dict()
    args['brands'] = Manufacturer.objects.all()
    args['nodes'] = Category.objects.all()
    return render(request, 'brands.html', args)


def brand_filter(request, brand_id):
    args = dict()
    args['products'] = Product.objects.filter(manufacturer_id=brand_id)
    args['nodes'] = Category.objects.all()
    return render(request, 'products.html', args)


def docs(request):
    return render_to_response('docs.html', context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))