# Generated by Django 4.2.16 on 2024-10-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_client_tenant_remove_payment_transaction_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='name',
            new_name='agent',
        ),
        migrations.RenameField(
            model_name='owner',
            old_name='name',
            new_name='owner',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
