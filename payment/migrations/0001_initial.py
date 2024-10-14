# Generated by Django 4.2.16 on 2024-10-14 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_mode', models.CharField(choices=[('bank', 'Bank'), ('mpesa', 'Mpesa'), ('paypal', 'Paypal'), ('stripe', 'stripe')], default='mpesa', max_length=30)),
                ('description', models.CharField(max_length=255)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date_paid', models.DateTimeField(auto_now=True)),
                ('transaction_desc', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('status', models.CharField(choices=[('paid', 'paid'), ('refunded', 'refunded'), ('failed', 'failed'), ('unsettled', 'unsettled')], default='unsettled', max_length=50)),
                ('transaction_type', models.CharField(choices=[('payment', 'Payment'), ('refund', 'Refund'), ('authorization', 'Authorization'), ('chargeback', 'Chargeback'), ('adjustment', 'Adjustment'), ('payout', 'Payout')], default='', max_length=200)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='payment.payment')),
            ],
        ),
    ]
