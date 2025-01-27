from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 


urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('home/', views.home_view, name='home'),
    path('product_detail/',views.product_detail,name='product_detail'),
    path('checkout_view/',views.checkout_view,name='checkout_view'),
    path('about_us/',views.about_us_view,name='about_us'),
    
    
    path('Excavators/',views.Excavators_view,name='Excavators'),
    path('Bulldozers/',views.Bulldozers_view,name='Bulldozers'),
    path('Cranes/',views.Cranes_view,name='Cranes'),
    path('Loaders/',views.Loaders_view,name='Loaders'),

    path('SteelPlates/',views.SteelPlates_view,name='SteelPlates'),
    path('AluminumSheets/',views.AluminumSheets_view,name='AluminumSheets'),
    path('CopperWires/',views.CopperWires_view,name='CopperWires'),
    path('MetalPipes/',views.MetalPipes_view,name='MetalPipes'),
    
    path('Lathes/',views.Lathes_view,name='Lathes'),
    path('CNCMachines/',views.CNCMachines_view,name='CNCMachines'),
    path('MillingMachines/',views.MillingMachines_view,name='MillingMachines'),
    path('HydraulicPresses/',views.HydraulicPresses_view,name='HydraulicPresses'),
   
    
    path('RockDrill/',views.RockDrill_view,name='RockDrill'),
    path('CrushingMachines/',views.CrushingMachines_view,name='CrushingMachines'),
    path('MiningTrucks/',views.MiningTrucks_view,name='MiningTrucks'),
    path('ConveyorBelts/',views.ConveyorBelts_view,name='ConveyorBelts'),
   

    path('Tractors/',views.Tractors_view,name='Tractors'),
    path('Harvesters/',views.Harvesters_view,name='Harvesters'),
    path('Plows/',views.plows_view,name='Plows'),
   
    path('Tankers/',views.Tankers_view,name='Tankers'),
    path('Dumptrucks/',views.Dumptrucks_view,name='Dumptrucks'),
    path('Forklifts/',views.Forklifts_view,name='Forklifts'),
    path('Trailers/',views.Trailers_view,name='Trailers'),
    
    path('search/',views.product_search, name='product_search'),   
                                   
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

