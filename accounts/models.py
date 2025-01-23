import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime, timedelta
from PIL import Image
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.html import format_html
from decimal import Decimal
from django.contrib.auth import get_user_model
import uuid
from django.conf import settings
import json

import locale

# Set the locale to the user's locale (you can adjust this as needed, e.g., for US English)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')





class AccountManager(BaseUserManager):
    def create_user(self,email, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Set the password using Django's hashing method
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not username:
            username = f"admin_{email.split('@')[0]}"  # Generate a default username

        return self.create_user(email=email, username=username, password=password, **extra_fields)




class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(max_length=100)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Changed default to True for regular users
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    USERNAME_FIELD = 'email'
    
    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class Product(models.Model):
    # Product Categories
    CONSTRUCTION_EQUIPMENT = 'Construction Equipment'
    METAL_PRODUCTS = 'Metal Products'
    INDUSTRIAL_MACHINERY = 'Industrial Machinery'
    MINING_EQUIPMENT = 'Mining Equipment'
    AGRICULTURAL_MACHINERY = 'Agricultural Machinery'
    HEAVY_VEHICLES = 'Heavy Vehicles'

    PRODUCT_CATEGORY_CHOICES = [
        (CONSTRUCTION_EQUIPMENT, 'Construction Equipment'),
        (METAL_PRODUCTS, 'Metal Products'),
        (INDUSTRIAL_MACHINERY, 'Industrial Machinery'),
        (MINING_EQUIPMENT, 'Mining Equipment'),
        (AGRICULTURAL_MACHINERY, 'Agricultural Machinery'),
        (HEAVY_VEHICLES, 'Heavy Vehicles'),
    ]

    # Product Types
    MATERIALS = 'Materials'
    EQUIPMENT = 'Equipment'
    ACCESSORIES = 'Accessories'
    SPARE_PARTS = 'Spare Parts'
    TOOLS = 'Tools'
    SAFETY_GEAR = 'Safety Gear'

    PRODUCT_TYPE_CHOICES = [
        (MATERIALS, 'Materials'),
        (EQUIPMENT, 'Equipment'),
        (ACCESSORIES, 'Accessories'),
        (SPARE_PARTS, 'Spare Parts'),
        (TOOLS, 'Tools'),
        (SAFETY_GEAR, 'Safety Gear'),
    ]

    # Product Tags
    FEATURED = 'Featured Products'
    BESTSELLERS = 'Bestsellers'
    POPULAR = 'Popular Categories'
    NEW_ARRIVALS = 'New Arrivals'

    PRODUCT_TAG_CHOICES = [
        (FEATURED, 'Featured Products'),
        (BESTSELLERS, 'Bestsellers'),
        (POPULAR, 'Popular Categories'),
        (NEW_ARRIVALS, 'New Arrivals'),
    ]

    # Product Fields
    name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=50, choices=PRODUCT_CATEGORY_CHOICES)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)
    product_tag = models.CharField(max_length=50, choices=PRODUCT_TAG_CHOICES, blank=True, null=True)  # Optional tag field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reviews_in_stars = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # e.g., 4.5 stars
    material = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    specification_general = models.TextField(blank=True, null=True)
    dimensions = models.TextField(blank=True, null=True)

    # Product Image
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Shipping fee for the product
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Convert the image to WebP format before saving
        if self.image:
            img = Image.open(self.image)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Convert image to WebP format
            webp_image = BytesIO()
            img.save(webp_image, format="WebP", quality=90)  # Adjust quality as needed
            webp_image.seek(0)
            
            # Save as a WebP file
            self.image = InMemoryUploadedFile(webp_image, 'ImageField', f"{self.image.name.split('.')[0]}.webp", 'image/webp', webp_image.tell(), None)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class WrittenReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='written_reviews')
    name = models.CharField(max_length=100)  # Name of the reviewer
    stars = models.PositiveIntegerField(default=0)  # Star rating out of 5
    content = models.TextField()  # Review content
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)  # Optional reviewer image
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Convert the review image to WebP format before saving
        if self.image:
            img = Image.open(self.image)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Convert image to WebP format
            webp_image = BytesIO()
            img.save(webp_image, format="WebP", quality=90)  # Adjust quality as needed
            webp_image.seek(0)
            
            # Save as a WebP file
            self.image = InMemoryUploadedFile(webp_image, 'ImageField', f"{self.image.name.split('.')[0]}.webp", 'image/webp', webp_image.tell(), None)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.name} - {self.stars} stars"
    
    



class ShoppingCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Reference the custom user model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    # Shipping fee associated with the cart
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def total_price(self):
        """Calculate total price for the cart item (product price * quantity + shipping fee)."""
        return self.product.price * self.quantity + self.shipping_fee
    
    total_price.short_description = 'Total Price'

    def image_tag(self):
        """Return an HTML tag to display the product image in the admin interface."""
        if self.product.image:
            return format_html('<img src="{0}" style="max-width: 100px; max-height: 100px;" />', self.product.image.url)
        return 'No Image'

    image_tag.short_description = 'Image Preview'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.user.username}"
    

class BankDetails(models.Model):
    # Bank Account Information
    bank_name = models.CharField(max_length=255, default="Default Bank")
    branch_name = models.CharField(max_length=255, default="Default Branch")
    account_number = models.CharField(max_length=20, default="0000000000")
    account_holder = models.CharField(max_length=255, default="Default Account Holder")
    swift_code = models.CharField(max_length=11, default="SWIFT000")

    def __str__(self):
        return f"{self.bank_name} - {self.branch_name}"   
    
 



class Order(models.Model):
    ORDER_STATUSES = [
        ('under_review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Reference the custom user model
    order_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)  # Auto-generated order ID
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, default='under_review')
    product_details = models.TextField()  # JSON field to store product details
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Added shipping fee
    order_image = models.ImageField(upload_to='order_images/', null=True, blank=True, help_text="Upload an image for the order")
    bank_details = models.ForeignKey('BankDetails', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_date_start = models.DateField(null=True, blank=True)  # Start of delivery range
    delivery_date_end = models.DateField(null=True, blank=True)    # End of delivery range

    def calculate_total_price(self):
        """Calculate total price (sum of products and shipping fee)."""
        import json
        products = json.loads(self.product_details).get("products", [])
        products_total = sum(item["quantity"] * item["price"] for item in products)
        return products_total + self.shipping_fee

    def image_tag(self):
        """Display an HTML tag for the order image in the admin interface."""
        if self.order_image:
            return format_html('<img src="{0}" style="max-width: 100px; max-height: 100px;" />', self.order_image.url)
        return 'No Image'

    image_tag.short_description = 'Image Preview'

    def save(self, *args, **kwargs):
        # Generate a unique order ID if it does not exist
        if not self.order_id:
            self.order_id = str(uuid.uuid4())[:8].upper()  # Generate a short unique ID (8 characters)
        # Set delivery date range if not already set
        if not self.delivery_date_start or not self.delivery_date_end:
            today = datetime.now().date()
            self.delivery_date_start = today + timedelta(days=14)  # 2 weeks from today
            self.delivery_date_end = self.delivery_date_start + timedelta(days=7)  # Delivery range of 1 week
        super().save(*args, **kwargs)

    def formatted_delivery_date(self):
        """Generate a delivery date range and return it as a formatted string."""
        if self.created_at:
            from datetime import timedelta
            start_date = self.created_at + timedelta(days=14)  # Two weeks from creation date
            end_date = start_date + timedelta(days=7)  # A 7-day range
            return f"Between {start_date.strftime('%d %B')} and {end_date.strftime('%d %B')}"
        return "Delivery date unavailable"


    def format_product_details(self):
        """Format the product details into a readable string."""
        try:
            # Load the product details from JSON
            product_details = json.loads(self.product_details)

            # Initialize a list to store formatted details
            formatted_details = []
      
            # Check if the 'products' key exists and contains products
            if 'products' in product_details and isinstance(product_details['products'], list):
                for item in product_details['products']:
                    # Safely extract product details
                    name = item.get('name', 'N/A')
                    quantity = item.get('quantity', 'N/A')
                    price = item.get('price', 'N/A')
                    image_url = item.get('image', 'N/A')

                                    # Format the price with commas and two decimal places
                    formatted_price = locale.currency(float(price), grouping=True) if price != 'N/A' else 'N/A'

                    # Format the details in a user-friendly way
                    formatted_details.append(f"Product: {name}\n"
                                             f"Quantity: {quantity}\n"
                                             f"Price: {formatted_price}\n"
                                            )

            # Return the formatted details as a string, each product separated by two line breaks
            return "\n\n".join(formatted_details) if formatted_details else "No products found."

        except json.JSONDecodeError:
            # Handle JSON parsing error
            print("Error: Invalid JSON format in product_details.")
            return "Invalid product details format."

        except Exception as e:
            # Handle any other exceptions
            print(f"Error formatting product details: {e}")
            return "Unable to format product details"


    def __str__(self):
        return f"Order {self.order_id} - {self.email}"
    
    

class PartnerRegistration(models.Model):
    USER_TYPES = [
        ('manufacturer', 'Manufacturer'),
        ('supplier', 'Supplier'),
        ('service_provider', 'Service Provider'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_profile')
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    company_type = models.CharField(max_length=50, choices=USER_TYPES)
    address = models.TextField()
    services_provided = models.TextField()
    website = models.URLField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"    