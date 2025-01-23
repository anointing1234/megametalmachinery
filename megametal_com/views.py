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

def Excavators_view(request):
    # Query products with "Excavators" in their name
    excavator_products = Product.objects.filter(name__icontains="Excavator")
    # Render the products to a template
    excavator_count = excavator_products.count()
    return render(request, 'home/excavators.html',{    
    'excavator_products': excavator_products,
    'excavator_count': excavator_count,
    })

def Bulldozers_view(request):
    Bulldozar_products = Product.objects.filter(name__icontains="bulldozar")
    Bulldozar_count = Bulldozar_products.count()  # Fixed typo here
    return render(request, 'home/Bulldozers.html', {
        'Bulldozar_products': Bulldozar_products,
        'Bulldozar_count': Bulldozar_count,
    })

def Cranes_view(request):
    # Query products with "Crane" in their name
    Crane_products = Product.objects.filter(name__icontains="Crane")
    Crane_count = Crane_products.count()  # Fixed typo here
    return render(request, 'home/Cranes.html', {
        'Crane_products': Crane_products,
        'Crane_count': Crane_count,
    })

def Loaders_view(request):
    Loaders_products = Product.objects.filter(name__icontains="Loader")
    Loaders_count = Loaders_products.count()  # Fixed typo here
    return render(request, 'home/Loaders.html', {
        'Loaders_products': Loaders_products,
        'Loaders_count': Loaders_count,
    })





def SteelPlates_view(request):
    Steel_products = Product.objects.filter(name__icontains="Steel Plate")
    Steel_count = Steel_products.count()  # Fixed typo here
    return render(request, 'home/steel.html', {
        'Steel_products': Steel_products,
        'Steel_count': Steel_count,
    })
    

def AluminumSheets_view(request):
    Aluminum_products = Product.objects.filter(name__icontains="Aluminum Sheet")
    Aluminum_count = Aluminum_products.count()  # Fixed typo here
    return render(request, 'home/Aluminum.html', {
        'Aluminum_products': Aluminum_products,
        'Aluminum_count': Aluminum_count,
    })
    

def CopperWires_view(request):
    Copper_products = Product.objects.filter(name__icontains="Copper")
    Copper_count = Copper_products.count()  # Fixed typo here
    return render(request, 'home/Copper.html', {
        'Copper_products': Copper_products,
        'Copper_count': Copper_count,
    })
    

def MetalPipes_view(request):
    Metal_products = Product.objects.filter(name__icontains="Metal pipes")
    Metal_count = Metal_products.count()  # Fixed typo here
    return render(request, 'home/metal.html', {
        'Metal_products': Metal_products,
        'Metal_count': Metal_count,
    })



def CNCMachines_view(request):
    cnc_products = Product.objects.filter(name__icontains="CNC")
    cnc_count =  cnc_products.count()  # Fixed typo here
    return render(request, 'home/cnc.html', {
        'cnc_products': cnc_products,
        'cnc_count': cnc_count,
    })
   

def Lathes_view(request):
    Lathes_products = Product.objects.filter(name__icontains="Lathes")
    Lathes_count =  Lathes_products.count()  # Fixed typo here
    return render(request, 'home/Lathes.html', {
        'Lathes_products': Lathes_products,
        'Lathes_count': Lathes_count,
    })

def MillingMachines_view(request):
    Milling_products = Product.objects.filter(name__icontains="Milling Machine")
    Milling_count =   Milling_products.count()  # Fixed typo here
    return render(request, 'home/Milling.html', {
        'Milling_products': Milling_products,
        'Milling_count': Milling_count,
    })


def HydraulicPresses_view(request):
    Hydraulic_products = Product.objects.filter(name__icontains="Hydraulic Press")
    Hydraulic_count =    Hydraulic_products.count()  # Fixed typo here
    return render(request, 'home/Hydraulic.html', {
        'Hydraulic_products':  Hydraulic_products,
        'Hydraulic_count':  Hydraulic_count,
    })    



def RockDrill_view(request):
    RockDrill_products = Product.objects.filter(name__icontains="Rock Drills")
    RockDrill_count =   RockDrill_products.count()  # Fixed typo here
    return render(request, 'home/RockDrill.html', {
        'RockDrill_products':  RockDrill_products,
        'RockDrill_count':  RockDrill_count,
    })  



def CrushingMachines_view(request):
    CrushingMachines_products = Product.objects.filter(name__icontains="Crushing Machines")
    CrushingMachines_count =   CrushingMachines_products.count()  # Fixed typo here
    return render(request, 'home/CrushingMachines.html', {
        'CrushingMachines_products':  CrushingMachines_products,
        'CrushingMachines_count':  CrushingMachines_count,
    }) 



def MiningTrucks_view(request):
    MiningTrucks_products = Product.objects.filter(name__icontains="Mining Trucks")
    MiningTrucks_count =    MiningTrucks_products.count()  # Fixed typo here
    return render(request, 'home/MiningTrucks.html', {
        'MiningTrucks_products':  MiningTrucks_products,
        'MiningTrucks_count':  MiningTrucks_count,
    }) 



def ConveyorBelts_view(request):
    ConveyorBelts_products = Product.objects.filter(name__icontains="Conveyor Belt")
    ConveyorBelts_count =    ConveyorBelts_products.count()  # Fixed typo here
    return render(request, 'home/ConveyorBelts.html', {
        'ConveyorBelts_products': ConveyorBelts_products,
        'ConveyorBelts_count':  ConveyorBelts_count,
    }) 




def Tractors_view(request):
    tractor_products = Product.objects.filter(name__icontains="tractor")
    tractor_count =    tractor_products.count()  # Fixed typo here
    return render(request, 'home/tractor.html', {
        'tractor_products': tractor_products,
        'tractor_count':  tractor_count,
    }) 


def plows_view(request):
    plows_view_products = Product.objects.filter(name__icontains="Plow")
    plows_view_count = plows_view_products.count()  # Fixed typo here
    return render(request,'home/plow.html', {
        'plows_view_products': plows_view_products,
        'plows_view_count': plows_view_count,
    })






def Harvesters_view(request):
    harvesters_products = Product.objects.filter(name__icontains="harvesters")
    harvesters_count =    harvesters_products.count()  # Fixed typo here
    return render(request, 'home/harvesters.html', {
        'harvesters_products': harvesters_products,
        'harvesters_count':  harvesters_count,
    }) 


def Tankers_view(request):
    Tanker_products = Product.objects.filter(name__icontains="Tanker")
    Tanker_count =   Tanker_products.count()  # Fixed typo here
    return render(request, 'home/Tanker.html', {
        'Tanker_products': Tanker_products,
        'Tanker_count': Tanker_count,
    }) 

def Dumptrucks_view(request):
    DumpTruck_products = Product.objects.filter(name__icontains="Dump Truck")
    DumpTruck_count =  DumpTruck_products.count()  # Fixed typo here
    return render(request, 'home/DumpTruck.html', {
        'DumpTruck_products': DumpTruck_products,
        'DumpTruck_count': DumpTruck_count,
    }) 
  
    

def Forklifts_view(request):
    Forklift_products = Product.objects.filter(name__icontains="Forklift")
    Forklift_count =  Forklift_products.count()  # Fixed typo here
    return render(request, 'home/Forklift.html', {
        'Forklift_products': Forklift_products,
        'Forklift_count': Forklift_count,
    }) 

def Trailers_view(request):
    Trailer_products = Product.objects.filter(name__icontains="Trailer")
    Trailer_count =  Trailer_products.count()  # Fixed typo here
    return render(request, 'home/Trailer.html', {
        'Trailer_products': Trailer_products,
        'Trailer_count': Trailer_count,
    }) 

  
    













