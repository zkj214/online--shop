# Generated by Django 5.2.2 on 2025-06-10 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sales',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stocks',
        ),
    ]
