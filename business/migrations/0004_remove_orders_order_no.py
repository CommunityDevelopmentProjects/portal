# Generated by Django 4.1.3 on 2022-12-27 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_orders_order_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_no',
        ),
    ]
