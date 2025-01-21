from django.shortcuts import render
import requests
import logging
import json
import os
import time
from urllib.parse import urljoin
from requests.exceptions import RequestException
from django.contrib.auth import logout
from bs4 import BeautifulSoup
import random
from accounts.models import Product,ShoppingCart


def home_view(request):
    featured_products = Product.objects.filter(product_tag=Product.FEATURED)
    bestsellers = Product.objects.filter(product_tag='Bestsellers')
    New_arrivals = Product.objects.filter(product_tag='New Arrivals')
    Popular = Product.objects.filter(product_tag='Popular Categories')
    return render(request,'home/index.html',
    {
    'featured_products': featured_products,
    'bestsellers': bestsellers,
    'New_arrivals':New_arrivals,
    'Popular':Popular,
    })

def product_detail(request):
    return render(request,'home/product_detail.html')

def checkout_view(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)
    # Calculate cart total and shipping fee
    cart_total = sum(item.total_price() for item in cart_items)
    shipping_fee = sum(item.shipping_fee for item in cart_items)  
    total_with_shipping = cart_total + shipping_fee
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_fee': shipping_fee,
        'total_with_shipping': total_with_shipping,
    }
    return render(request,'home/checkout.html',context)
