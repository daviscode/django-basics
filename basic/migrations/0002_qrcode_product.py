# Generated by Django 5.1.6 on 2025-02-06 07:44

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('deactivated_at', models.DateTimeField(blank=True, null=True)),
                ('deactivated_by', models.BigIntegerField(blank=True, null=True)),
                ('deleted_by', models.BigIntegerField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('product_id', models.BigIntegerField()),
                ('qr_code_data', models.TextField()),
                ('generated_date', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('dynamic', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'qr_code',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('deactivated_at', models.DateTimeField(blank=True, null=True)),
                ('deactivated_by', models.BigIntegerField(blank=True, null=True)),
                ('deleted_by', models.BigIntegerField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(max_length=50)),
                ('eco_friendly', models.BooleanField(default=False)),
                ('image', models.TextField(blank=True, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.currency')),
                ('qr_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basic.qrcode')),
            ],
            options={
                'db_table': 'product',
                'constraints': [models.CheckConstraint(condition=models.Q(('name__regex', '^[A-Z][a-z]*( [A-Z][a-z]*)*$')), name='product_name_format_check'), models.CheckConstraint(condition=models.Q(('category__regex', '^[A-Z][a-z]*$')), name='category_format_check')],
            },
        ),
    ]
