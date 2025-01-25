from django.contrib import admin
from .models import Account,Product, WrittenReview,ShoppingCart,BankDetails,Order,PartnerRegistration
from django.utils.html import format_html
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging
from django.templatetags.static import static
import base64
from django.core.files import File
from io import BytesIO
from PIL import Image
import os
from django.contrib.staticfiles.storage import staticfiles_storage
import json
from django.db.models import Count




class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff', 'is_superuser')




class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_category', 'product_type', 'price', 'reviews_in_stars', 'quantity', 'shipping_fee', 'image_tag')  # Added 'shipping_fee'
    search_fields = ('name', 'description')  # Add search functionality
    list_filter = ('product_category', 'product_type', 'product_tag')  # Add filters for categories, types, and tags
    ordering = ('-price',)  # Default ordering by price (descending)

    # Image preview in the admin panel for product image
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{0}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        return 'No Image'
    image_tag.short_description = 'Image Preview'  # Custom label for image column

    # Allow editing of images directly from the form
    fieldsets = (
        (None, {
            'fields': ('name', 'product_category', 'product_type', 'product_tag', 'price', 'reviews_in_stars', 'material', 'quantity', 'shipping_fee', 'description', 'specification_general', 'dimensions', 'image')
        }),
    )
    readonly_fields = ('image_tag',)

    # Make sure the image field is displayed properly
    def save_model(self, request, obj, form, change):
        obj.save()




# Customizing WrittenReview Model in the Admin Panel
class WrittenReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'stars', 'date', 'image_tag')  # Fields to display in list view
    search_fields = ('product__name', 'content', 'name')  # Allow searching for reviews by product name, reviewer name, or content
    list_filter = ('stars',)  # Add filter for star ratings
    ordering = ('-date',)  # Default ordering by date (descending)

    # Image preview in the admin panel for review image
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{0}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        return 'No Image'
    image_tag.short_description = 'Image Preview'  # Custom label for image column

    # Allow editing of images directly from the form
    fieldsets = (
        (None, {
            'fields': ('product', 'name', 'stars', 'content', 'image', 'date')
        }),
    )
    readonly_fields = ('image_tag',)

    def save_model(self, request, obj, form, change):
        obj.save()



class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'image_tag', 'total_price', 'added_at')
    readonly_fields = ('total_price', 'image_tag')
    list_filter = ('user',)  # Filter by user
    search_fields = ('user__username', 'product__name')  # Search by user and product name

    def save_model(self, request, obj, form, change):
        obj.save()
        



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'id',
        'order_id',
        'user',
        'status',
        'total_price',
        'formatted_delivery_date',
        'image_tag',
        'created_at',
        'format_product_details',  # Add formatted product details to the list display
    )

    # Fields to make read-only in the detail view
    readonly_fields = ('order_id', 'formatted_delivery_date', 'image_tag', 'created_at', 'updated_at', 'format_product_details',)

    # Filters and search fields
    list_filter = ('status', 'created_at',)
    search_fields = ('order_id', 'email', 'user__username', 'user__email', 'phone',)

    # Fieldsets for organizing the admin detail view
    fieldsets = (
        ('Order Information', {
            'fields': (
                'order_id',
                'user',
                'email',
                'phone',
                'status',
                'product_details',
                'total_price',
                'shipping_fee',
            ),
        }),
        ('Delivery Information', {
            'fields': ('formatted_delivery_date',),
        }),
        ('Address Information', {
            'fields': ('street_address', 'city', 'state', 'postcode',),
        }),
        ('Order Image', {
            'fields': ('order_image', 'image_tag',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at',),
        }),
    )

    # Custom actions for confirming and declining orders
    actions = ['confirm_order', 'decline_order']

    def confirm_order(self, request, queryset):
        """Mark selected orders as completed and send confirmation email."""
        updated_count = queryset.filter(status='under_review').update(status='completed')
        
        # Send emails for each confirmed order
        for order in queryset.filter(status='completed'):
            self.send_confirmation_email(order)

        self.message_user(request, f"{updated_count} order(s) marked as 'Completed' and emails sent.")

    confirm_order.short_description = "Confirm selected orders"

    def decline_order(self, request, queryset):
        """Mark selected orders as cancelled."""
        updated_count = queryset.filter(status='under_review').update(status='cancelled')
        self.message_user(request, f"{updated_count} order(s) marked as 'Cancelled'.")

    decline_order.short_description = "Decline selected orders"

    def send_confirmation_email(self, order):
        """Send an order confirmation email to the user."""
        subject = f"Order Confirmation - {order.order_id}"

        # Prepare the email content
        formatted_product_details = order.format_product_details()  # Get the formatted product details
        formatted_delivery_date = order.formatted_delivery_date()  # Get the formatted delivery date range

        html_content = render_to_string('order_confirmation_email.html', {
            'order': order,
            'formatted_product_details': formatted_product_details,
            'formatted_delivery_date': formatted_delivery_date  # Pass formatted delivery date range
        })

        # Create the email message
        email = EmailMessage(
            subject,
            html_content,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],  # Send to the order's user email
        )
        email.content_subtype = 'html'  # Mark the email as HTML

        # Send the email
        try:
            email.send(fail_silently=False)
            print(f"Confirmation email sent successfully to {order.email}")  # Print message in the console
        except Exception as e:
            print(f"Failed to send confirmation email to {order.email}: {e}")

    def format_product_details(self, obj):
        """Format the product details for display in the admin panel."""
        try:
            product_details = json.loads(obj.product_details)
            return format_html("<br>".join([f"{item['name']} (Qty: {item['quantity']})" for item in product_details['products']]))
        except (json.JSONDecodeError, KeyError):
            return "Invalid product details"

    format_product_details.short_description = "Product Details"




@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'branch_name', 'account_number', 'swift_code')
    search_fields = ('bank_name', 'branch_name')
 
 

@admin.register(PartnerRegistration)
class PartnerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone_number', 'registration_date')
    search_fields = ('company_name', 'contact_person', 'email')
    list_filter = ('company_type', 'registration_date')        
        

admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(WrittenReview, WrittenReviewAdmin)        
admin.site.register(Account, AccountAdmin)    
