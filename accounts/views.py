from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from .form import RegisterForm,LoginForm,PartnerRegistrationForm,SendresetcodeForm,PasswordResetForm,ReviewForm 
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
from django.core.mail import EmailMessage
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
from .models import Product,ShoppingCart,BankDetails,Order,PartnerRegistration,PasswordResetCode,WrittenReview 
import logging
from django.core.mail import send_mail


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
    register_form = RegisterForm()
    login_form = LoginForm()
    return render(request, 'forms/Auth.html', {
        'login_form': login_form,
        'register_form': register_form,
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



def product_description(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(product_category=product.product_category).exclude(id=product.id)[:5]
    reviews = WrittenReview.objects.filter(product=product)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)  # Include FILES for image upload
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product  # Associate the review with the product
            review.save()

            # Update the product's star rating
            update_product_rating(product)

            return redirect('product_detail', product_id=product.id)  # Redirect to the same product page
    else:
        form = ReviewForm()

    return render(request, 'home/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'form': form,  # Pass the form to the template
    })

def update_product_rating(product):
    reviews = WrittenReview.objects.filter(product=product)
    if reviews.exists():
        average_rating = sum(review.stars for review in reviews) / reviews.count()
        product.reviews_in_stars = round(average_rating, 1)  # Update the product's star rating
        product.save()
        


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

            # Create a list to hold order IDs for the response
            order_ids = []

            # Iterate over each product in the cart
            for product in cart_details["products"]:
                # Calculate total price for the individual product order
                total_price = float(product["quantity"]) * float(product["price"])

                # Calculate shipping fee (this is a placeholder; adjust as needed)
                shipping_fee = cart_details.get("shipping_fee", 0.0)  # Ensure this is set correctly

                # Create a new order instance for each product
                order = Order(
                    user=request.user,
                    street_address=billing_details["street_address"],
                    city=billing_details["city"],
                    state=billing_details["state"],
                    postcode=billing_details["postcode"],
                    email=billing_details["email"],
                    phone=billing_details["phone"],
                    product_details=json.dumps({"products": [product]}),  # Store only the current product
                    total_price=total_price,
                    shipping_fee=shipping_fee,
                )

                # Assign an image to the order from the product
                product_id = product["id"]
                try:
                    product_instance = Product.objects.get(id=product_id)
                    if product_instance.image:
                        order.order_image = product_instance.image  # Assign product's image to order_image
                except Product.DoesNotExist:
                    pass  # Handle the case where the product does not exist

                # Save the order instance
                order.save()
                order_ids.append(order.id)  # Store the order ID for the response

            # Clear the shopping cart for the user
            ShoppingCart.objects.filter(user=request.user).delete()

            return JsonResponse({"success": True, "order_ids": order_ids})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format."}, status=400)
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

            # Prepare the email content with HTML formatting
            subject = "New Partner Registration"
            message = f"""
            <html>
                <body>
                    <h2>New Partner Registration</h2>
                    <p>A new partner has registered with the following details:</p>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <th style="text-align: left; border: 1px solid #dddddd; padding: 8px;">Field</th>
                            <th style="text-align: left; border: 1px solid #dddddd; padding: 8px;">Details</th>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Company Name</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.company_name}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Contact Person</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.contact_person}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Email</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.email}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Phone Number</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.phone_number}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Company Type</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.company_type}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Address</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.address}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Services/Products Provided</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.services_provided}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Website</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.website or 'Not Provided'}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dddddd; padding: 8px;">Registration Date</td>
                            <td style="border: 1px solid #dddddd; padding: 8px;">{partner.registration_date.strftime('%Y-%m-%d %H:%M:%S')}</td>
                        </tr>
                    </table>
                </body>
            </html>
            """

            # Send the email
            company_email = settings.COMPANY_EMAIL  # Ensure this is set in your settings
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [company_email]
            )
            email.content_subtype = "html"  # Set content type to HTML
            email.charset = 'utf-8'  # Ensure UTF-8 encoding
            email.send(fail_silently=False)

            # Show success message
            messages.success(request, "Thank you for registering as a partner! We will get back to you shortly.")
            return render(request, 'home/partnersuccess.html')  # Replace with the name of the success page/view

    else:
        form = PartnerRegistrationForm()

    return render(request, 'forms/register_partner.html', {'form': form})



def products_view(request):
    return render(request,'home/products.html')


def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)

def custom_500_view(request):
    return render(request, 'home/500.html', status=500)

def forgot_password(request):
    sendmailreset = SendresetcodeForm()
    return render(request,'forms/send_password.html',{'sendmailreset': sendmailreset})

def send_reset_code_view(request):
    if request.method == 'POST':
        form = SendresetcodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if the email is registered
            User = get_user_model()  # Get the custom user model
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'This email address is not registered.'})

            # Generate a reset code
            reset_code = get_random_string(length=7)  # Generate a random string as the reset code
            
            # Store the reset code in the database
            PasswordResetCode.objects.update_or_create(
                email=email,
                defaults={'reset_code': reset_code}
            )
            
            # Send the email
            send_mail(
                'Password Reset Code',
                f'Your password reset code is: {reset_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True, 'message': 'A password reset code has been sent to your email.'})
        else:
            return JsonResponse({'success': False, 'message': form.errors['email'][0]})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def ResetPasswordView(request):
    return render(request,'forms/reset_password.html')   







def reset_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)  # Use a different variable name
        if form.is_valid():
            email = form.cleaned_data['email']
            reset_code = form.cleaned_data['reset_code']
            new_password = form.cleaned_data['new_password']

            # Check if the reset code is valid for the given email
            try:
                reset_entry = PasswordResetCode.objects.get(email=email, reset_code=reset_code)
            except PasswordResetCode.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid reset code or email.'})

            # Update the user's password
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)  # Set the new password
                user.save()

                # Optionally, delete the reset code after use
                reset_entry.delete()

                messages.success(request, "Your password has been reset successfully.")
                return JsonResponse({'success': True, 'message': 'Your password has been reset successfully.'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User  not found.'})

    else:
        form = PasswordResetForm()  # This is now correctly instantiated

    return render(request, 'reset_password.html', {'form': form})