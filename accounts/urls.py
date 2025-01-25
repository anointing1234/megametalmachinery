from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 
from django.conf.urls import handler404, handler500



urlpatterns = [
    path('Authenticate_view/', views.Authenticate_view, name='Authenticate_view'),
    path('login_view/',views.login_view,name='login_view'),
    path('register/',views.register,name='register'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('product/<int:product_id>/', views.product_description, name='product_detail'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'), 
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path("get_bank_details/", views.get_bank_details, name="get_bank_details"),
    path("create_order/", views.create_order, name="create_order"),
    path("order_success/", views.order_success, name="order_success"),
    path("myorders/",views.myorders,name="myorders"),
    path('orders/<str:order_id>/', views.order_details, name='order_details'),
    path('register_partner/',views.register_partners,name='register_partner'),
    path('logout_view/',views.logout_view,name='logout_view'),
    path('products/',views.products_view,name='products'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('send-reset-code/',views.send_reset_code_view, name='sendmail_view'),
    path('reset-password/',views.ResetPasswordView, name='reset_password_page'),
    path('reset_password/',views.reset_password_view, name='reset_password'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = views.custom_404_view
handler500 = views.custom_500_view
 
 

