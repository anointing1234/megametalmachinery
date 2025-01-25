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
from django.core.paginator import Paginator


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



def about_us_view(request):
    return render(request,'home/about-us.html',)     

  
    


def Excavators_view(request):
    excavator_products = Product.objects.filter(name__icontains="Excavator")
    paginator = Paginator(excavator_products, 2)  # Show 2 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/excavators.html', {
        'excavator_products': page_obj,
        'excavator_count': excavator_products.count(),
    })

def Bulldozers_view(request):
    bulldozer_products = Product.objects.filter(name__icontains="bulldozar")
    paginator = Paginator(bulldozer_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Bulldozers.html', {
        'Bulldozar_products': page_obj,
        'Bulldozar_count': bulldozer_products.count(),
    })

def Cranes_view(request):
    crane_products = Product.objects.filter(name__icontains="Crane")
    paginator = Paginator(crane_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Cranes.html', {
        'Crane_products': page_obj,
        'Crane_count': crane_products.count(),
    })

def Loaders_view(request):
    loaders_products = Product.objects.filter(name__icontains="Loader")
    paginator = Paginator(loaders_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Loaders.html', {
        'Loaders_products': page_obj,
        'Loaders_count': loaders_products.count(),
    })

def SteelPlates_view(request):
    steel_products = Product.objects.filter(name__icontains="Steel Plate")
    paginator = Paginator(steel_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/steel.html', {
        'Steel_products': page_obj,
        'Steel_count': steel_products.count(),
    })

def AluminumSheets_view(request):
    aluminum_products = Product.objects.filter(name__icontains="Aluminum Sheet")
    paginator = Paginator(aluminum_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Aluminum.html', {
        'Aluminum_products': page_obj,
        'Aluminum_count': aluminum_products.count(),
    })

def CopperWires_view(request):
    copper_products = Product.objects.filter(name__icontains="Copper")
    paginator = Paginator(copper_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Copper.html', {
        'Copper_products': page_obj,
        'Copper_count': copper_products.count(),
    })

def MetalPipes_view(request):
    metal_products = Product.objects.filter(name__icontains="Metal pipes")
    paginator = Paginator(metal_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/metal.html', {
        'Metal_products': page_obj,
        'Metal_count': metal_products.count(),
    })

def CNCMachines_view(request):
    cnc_products = Product.objects.filter(name__icontains="CNC")
    paginator = Paginator(cnc_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/cnc.html', {
        'cnc_products': page_obj,
        'cnc_count': cnc_products.count(),
    })

def Lathes_view(request):
    lathes_products = Product.objects.filter(name__icontains="Lathes")
    paginator = Paginator(lathes_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Lathes.html', {
        'Lathes_products': page_obj,
        'Lathes_count': lathes_products.count(),
    })

def MillingMachines_view(request):
    milling_products = Product.objects.filter(name__icontains="Milling Machine")
    paginator = Paginator(milling_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Milling.html', {
        'Milling_products': page_obj,
        'Milling_count': milling_products.count(),
    })

def HydraulicPresses_view(request):
    hydraulic_products = Product.objects.filter(name__icontains="Hydraulic Press")
    paginator = Paginator(hydraulic_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Hydraulic.html', {
        'Hydraulic_products': page_obj,
        'Hydraulic_count': hydraulic_products.count(),
    })

def RockDrill_view(request):
    rock_drill_products = Product.objects.filter(name__icontains="Rock Drills")
    paginator = Paginator(rock_drill_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/RockDrill.html', {
        'RockDrill_products': page_obj,
        'RockDrill_count': rock_drill_products.count(),
    })

def CrushingMachines_view(request):
    crushing_machines_products = Product.objects.filter(name__icontains="Crushing Machines")
    paginator = Paginator(crushing_machines_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/CrushingMachines.html', {
        'CrushingMachines_products': page_obj,
        'CrushingMachines_count': crushing_machines_products.count(),
    })

def MiningTrucks_view(request):
    mining_trucks_products = Product.objects.filter(name__icontains="Mining Trucks")
    paginator = Paginator(mining_trucks_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/MiningTrucks.html', {
        'MiningTrucks_products': page_obj,
        'MiningTrucks_count': mining_trucks_products.count(),
    })

def ConveyorBelts_view(request):
    conveyor_belts_products = Product.objects.filter(name__icontains="Conveyor Belt")
    paginator = Paginator(conveyor_belts_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/ConveyorBelts.html', {
        'ConveyorBelts_products': page_obj,
        'ConveyorBelts_count': conveyor_belts_products.count(),
    })

def Tractors_view(request):
    tractor_products = Product.objects.filter(name__icontains="tractor")
    paginator = Paginator(tractor_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/tractor.html', {
        'tractor_products': page_obj,
        'tractor_count': tractor_products.count(),
    })

def plows_view(request):
    plows_view_products = Product.objects.filter(name__icontains="Plow")
    paginator = Paginator(plows_view_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/plow.html', {
        'plows_view_products': page_obj,
        'plows_view_count': plows_view_products.count(),
    })

def Harvesters_view(request):
    harvesters_products = Product.objects.filter(name__icontains="harvesters")
    paginator = Paginator(harvesters_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/harvesters.html', {
        'harvesters_products': page_obj,
        'harvesters_count': harvesters_products.count(),
    })

def Tankers_view(request):
    tanker_products = Product.objects.filter(name__icontains="Tanker")
    paginator = Paginator(tanker_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Tanker.html', {
        'Tanker_products': page_obj,
        'Tanker_count': tanker_products.count(),
    })

def Dumptrucks_view(request):
    dump_truck_products = Product.objects.filter(name__icontains="Dump Truck")
    paginator = Paginator(dump_truck_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/DumpTruck.html', {
        'DumpTruck_products': page_obj,
        'DumpTruck_count': dump_truck_products.count(),
    })

def Forklifts_view(request):
    forklift_products = Product.objects.filter(name__icontains="Forklift")
    paginator = Paginator(forklift_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Forklift.html', {
        'Forklift_products': page_obj,
        'Forklift_count': forklift_products.count(),
    })

def Trailers_view(request):
    trailer_products = Product.objects.filter(name__icontains="Trailer")
    paginator = Paginator(trailer_products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/Trailer.html', {
        'Trailer_products': page_obj,
        'Trailer_count': trailer_products.count(),
    })




def product_search(request):
    query = request.GET.get('search', '')
    print(f"Search query: {query}")  # Debugging line
    if query:
        products = Product.objects.filter(name__icontains=query)
        print(f"Found products: {products}")  # Debugging line
    else:
        products = Product.objects.none()

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/search_results.html', {
        'RockDrill_products': page_obj,
        'RockDrill_count': products.count(),
        'search_query': query,
    })











