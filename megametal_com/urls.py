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
    path('Excavators/',views.Excavators_view,name='Excavators'),
    path('Bulldozers/',views.Bulldozers_view,name='Bulldozers'),
    path('Cranes/',views.Cranes_view,name='Cranes'),
    path('Loaders/',views.Loaders_view,name='Loaders'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

