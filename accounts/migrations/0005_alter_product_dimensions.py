# Generated by Django 5.0.7 on 2025-01-17 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_shoppingcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dimensions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
