# Generated by Django 4.0.4 on 2022-05-26 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='item_amout',
            new_name='item_amount',
        ),
    ]
