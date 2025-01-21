from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from .form import RegisterForm,LoginForm,PartnerRegistrationForm
from django.http import JsonResponse
import requests 
from decimal import Decimal, InvalidOperation
import logging
import json
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal,InvalidOperation
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
import logging
from django.db import transaction
from django.db.models import F,Sum
from django.contrib.auth.decorators import login_required
from .models import Product,ShoppingCart,BankDetails,Order,PartnerRegistration
import logging

logger = logging.getLogger(__name__)


def Authenticate_view(request):
    register_form = RegisterForm()
    login_form = LoginForm()
    return render(request,'forms/Auth.html',{
        'login_form': login_form,
        'register_form': register_form,
        })


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            user = register_form.save()
            return JsonResponse({'success': True, 'message': 'Registration successful!', 'redirect_url': '/accounts/login_view'})  # Redirect URL
        else:
            # Collect all form errors
            error_messages = []
            if register_form.errors:
                for field, errors in register_form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field.capitalize()}: {error}")
            error_message = "\n".join(error_messages)

            return JsonResponse({'success': False, 'message': error_message})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})


 

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': '/'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid email  or password.'
            })
    else:
        login_form = LoginForm()
    return render(request, 'forms/Auth.html', {'login_form': login_form})

def logout_view(request):
    auth_logout(request)
    login_form = LoginForm()
    return render(request,'forms/Auth.html',
    { 
     'login':login_form                                         
    })

def cart_view(request):
    # Fetch cart items for the logged-in user
    cart_items = ShoppingCart.objects.filter(user=request.user)
    
    # Initialize total variables
    subtotal = 0
    total = 0
    shipping_total = 0
    
    # Loop through each item to calculate subtotal and shipping fee
    for item in cart_items:
        # Calculate the subtotal (product price * quantity)
        item_subtotal = item.product.price * item.quantity
        subtotal += item_subtotal
        
        # Calculate the shipping fee for the item (example logic)
        shipping_fee = item.product.shipping_fee * item.quantity  # You can adjust this logic based on the product
        
        # Add shipping fee to the total
        shipping_total += shipping_fee
        
        # Add the item total (subtotal + shipping) to the total
        total += item_subtotal + shipping_fee

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_total': shipping_total,
        'total': total,
    }
    return render(request, 'home/cart.html', context)



def product_description(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})



@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)  # Fetch the product
            user = request.user  # Get the logged-in user
            
            # Check if the product is already in the cart
            cart_item, created = ShoppingCart.objects.get_or_create(
                user=user, product=product,shipping_fee=product.shipping_fee,
                defaults={'quantity': 1}
            )
            if not created:
                # If the item exists, increase the quantity
                cart_item.quantity += 1
                cart_item.save()
            
            return JsonResponse({"message": "Product added to cart successfully!"}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = ShoppingCart.objects.filter(user=request.user).count()  # Get the number of items in the cart
        return JsonResponse({"cart_count": cart_count})
    else:
        return JsonResponse({"cart_count": 0})
    
    # Helper function to calculate the cart total
def get_cart_total(user):
    cart_items = ShoppingCart.objects.filter(user=user)
    total = sum(item.total_price() for item in cart_items)
    return total

# Helper function to calculate shipping fee (example logic, adjust as needed)
def calculate_shipping_fee(cart_total):
    # Example: Flat $10 shipping if cart total is below $100, free otherwise
    return  cart_total 

# Function to increase item quantity
def increase_quantity(request, item_id):
    cart_item = ShoppingCart.objects.get(id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    # Calculate updated totals
    cart_total = get_cart_total(request.user)
    shipping_fee = calculate_shipping_fee(cart_total)
    total_amount = cart_total + shipping_fee

    return JsonResponse({
        'new_quantity': cart_item.quantity,
        'new_total': cart_item.total_price(),
        'new_cart_total': cart_total,
        'new_shipping_total': shipping_fee,
        'new_total_amount': total_amount,
    })

# Function to decrease item quantity
def decrease_quantity(request, item_id):
    cart_item = ShoppingCart.objects.get(id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    # Calculate updated totals
    cart_total = get_cart_total(request.user)
    shipping_fee = calculate_shipping_fee(cart_total)
    total_amount = cart_total + shipping_fee

    return JsonResponse({
        'new_quantity': cart_item.quantity,
        'new_total': cart_item.total_price(),
        'new_cart_total': cart_total,
        'new_shipping_total': shipping_fee,
        'new_total_amount': total_amount,
    })

# Function to remove item from cart
def remove_from_cart(request, item_id):
    cart_item = ShoppingCart.objects.get(id=item_id, user=request.user)
    cart_item.delete()

    # Calculate updated totals
    cart_total = get_cart_total(request.user)
    shipping_fee = calculate_shipping_fee(cart_total)
    total_amount = cart_total + shipping_fee

    return JsonResponse({
        'message': 'Item removed successfully',
        'new_cart_total': cart_total,
        'new_shipping_total': shipping_fee,
        'new_total_amount': total_amount,
    })
    
    
def get_bank_details(request):
    try:
        bank_details = BankDetails.objects.first()  # Fetch the first bank details record
        if not bank_details:
            return JsonResponse({"error": "Bank details not found"}, status=404)

        return JsonResponse({
            "bank_name": bank_details.bank_name,
            "branch_name": bank_details.branch_name,
            "account_number": bank_details.account_number,
            "account_holder": bank_details.account_holder,
            "swift_code": bank_details.swift_code,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  
    

def create_order(request):
    if request.method == "POST":
        try:
            # Parse the request body
            data = json.loads(request.body)

            billing_details = data.get("billingDetails")
            cart_details = data.get("cartDetails")

            # Validate data
            if not billing_details or not cart_details:
                return JsonResponse({"success": False, "error": "Invalid request data."}, status=400)

            # Calculate total price
            total_price = sum(
                float(product["quantity"]) * float(product["price"])
                for product in cart_details["products"]
            )

            # Create a new order instance
            order = Order(
                user=request.user,
                street_address=billing_details["street_address"],
                city=billing_details["city"],
                state=billing_details["state"],
                postcode=billing_details["postcode"],
                email=billing_details["email"],
                phone=billing_details["phone"],
                product_details=json.dumps(cart_details),
                total_price=total_price,
                shipping_fee=cart_details.get("shipping_fee", 0.0),
            )

            # Assign an image to the order from the first product in cart_details
            first_product = cart_details["products"][0] if cart_details["products"] else None
            if first_product:
                product_id = first_product["id"]
                try:
                    product = Product.objects.get(id=product_id)
                    if product.image:
                        order.order_image = product.image  # Assign product's image to order_image
                except Product.DoesNotExist:
                    pass

            # Save the order instance
            order.save()

            # Clear the shopping cart for the user
            ShoppingCart.objects.filter(user=request.user).delete()

            return JsonResponse({"success": True, "order_id": order.id})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


def order_success(request):
    return render(request, 'home/order.html')


def myorders(request):
    """
    Fetch and display all orders for the currently logged-in user.
    """
    # Fetch orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Parse product details for each order
    for order in orders:
        try:
            order.product_details_parsed = json.loads(order.product_details).get('products', [])
        except json.JSONDecodeError:
            order.product_details_parsed = []  # Default to empty list if JSON is invalid

    return render(request, 'home/my_orders.html', {
        'orders': orders,
    })

def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'home/order_details.html', {'order': order})    

def register_partner(request):
    form = PartnerRegistrationForm()
    return render(request,'forms/register_partner',{'form':form})


def register_partners(request):
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST)
        if form.is_valid():
            # Check if the user already has a PartnerRegistration
            if PartnerRegistration.objects.filter(user=request.user).exists():
                messages.error(request, "You are already registered as a partner.")
                return redirect('register_partner')  # Redirect to avoid re-submitting the form

            # If no duplicate, save the form
            partner = form.save(commit=False)
            partner.user = request.user
            partner.registration_date = timezone.now()  # Set registration date
            partner.save()

            # Prepare the email content
            subject = "New Partner Registration"
            message = f"""
            A new partner has registered with the following details:

            Company Name: {partner.company_name}
            Contact Person: {partner.contact_person}
            Email: {partner.email}
            Phone Number: {partner.phone_number}
            Company Type: {partner.company_type}
            Address: {partner.address}
            Services/Products Provided: {partner.services_provided}
            Website: {partner.website or 'Not Provided'}
            Registration Date: {partner.registration_date.strftime('%Y-%m-%d %H:%M:%S')}
            """

            # Send the email
            company_email = settings.COMPANY_EMAIL  # Ensure this is set in your settings
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [company_email],
                fail_silently=False,
            )

            # Show success message
            messages.success(request, "Thank you for registering as a partner! We will get back to you shortly.")
            return redirect('some_success_page')  # Replace with the name of the success page/view

    else:
        form = PartnerRegistrationForm()

    return render(request, 'forms/register_partner.html', {'form': form})






def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)

def custom_500_view(request):
    return render(request, 'home/500.html', status=500)