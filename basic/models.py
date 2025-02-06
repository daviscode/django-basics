from django.db import models
import uuid

class Currency(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.BigIntegerField(null=True, blank=True)
    deleted_by = models.BigIntegerField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)

    class Meta:
        db_table = 'st_currencies'
        constraints = [
            models.CheckConstraint(
                check=models.Q(code__regex='^[A-Z]{3}$'),
                name='code_format_check'
            ),
            models.CheckConstraint(
                check=models.Q(name__regex='^[A-Z][a-z]*( [A-Z][a-z]*)*$'),
                name='name_format_check'
            ),
        ]

    def __str__(self):
        return self.code
    

class QRCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.BigIntegerField(null=True, blank=True)
    deleted_by = models.BigIntegerField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    product_id = models.BigIntegerField()
    qr_code_data = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    dynamic = models.BooleanField(default=False)

    class Meta:
        db_table = 'qr_code'

    def __str__(self):
        return f"QR Code for Product ID: {self.product_id}"

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.BigIntegerField(null=True, blank=True)
    deleted_by = models.BigIntegerField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True, blank=True)
    eco_friendly = models.BooleanField(default=False)
    image = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'product'
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__regex=r'^[A-Z][a-z]*( [A-Z][a-z]*)*$'),
                name='product_name_format_check'
            ),
            models.CheckConstraint(
                check=models.Q(category__regex=r'^[A-Z][a-z]*$'),
                name='category_format_check'
            ),
        ]

    def __str__(self):
        return self.name