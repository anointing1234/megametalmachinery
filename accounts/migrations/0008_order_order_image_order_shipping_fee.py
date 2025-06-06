# Generated by Django 5.0.7 on 2025-01-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_image',
            field=models.ImageField(blank=True, help_text='Upload an image for the order', null=True, upload_to='order_images/'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
