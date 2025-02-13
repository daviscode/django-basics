from django.db import models
import uuid
from django.core.cache import cache

class Currency(models.Model):
    # Primary key field that auto-increments
    id = models.BigAutoField(primary_key=True)

    # Boolean field indicating whether the currency is active
    active = models.BooleanField(default=True)

    # DateTime field that automatically sets the current date and time when the record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Big integer field to store the ID of the user who created the record
    created_by = models.BigIntegerField(null=True, blank=True)

    # UUID field that generates a unique identifier for each record
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # DateTime field to store when the currency was deactivated
    deactivated_at = models.DateTimeField(null=True, blank=True)

    # Big integer field to store the ID of the user who deactivated the record
    deactivated_by = models.BigIntegerField(null=True, blank=True)

    # Big integer field to store the ID of the user who deleted the record
    deleted_by = models.BigIntegerField(null=True, blank=True)

    # Boolean field indicating whether the currency is deleted
    deleted = models.BooleanField(default=False)

    # DateTime field to store when the currency was deleted
    deleted_at = models.DateTimeField(null=True, blank=True)

    # DateTime field that automatically updates to the current date and time whenever the record is saved
    updated_at = models.DateTimeField(auto_now=True)

    # Big integer field to store the ID of the user who last updated the record
    updated_by = models.BigIntegerField(null=True, blank=True)

    # Character field to store the currency code (e.g., USD, EUR), which must be unique
    code = models.CharField(max_length=3, unique=True)

    # Character field to store the name of the currency
    name = models.CharField(max_length=50)

    # Character field to store the symbol of the currency (e.g., $, €)
    symbol = models.CharField(max_length=10)

    class Meta:
        # Specifies the name of the database table to use for the model
        db_table = 'st_currencies'

        # Defines database constraints
        constraints = [
            # Ensures that the `code` field is a three-letter uppercase string
            models.CheckConstraint(
                check=models.Q(code__regex='^[A-Z]{3}$'),
                name='code_format_check'
            ),
            # Ensures that the `name` field starts with a capital letter and contains only letters and spaces
            models.CheckConstraint(
                check=models.Q(name__regex='^[A-Z][a-z]*( [A-Z][a-z]*)*$'),
                name='name_format_check'
            ),
        ]

    def __str__(self):
        # Returns the currency code when the object is printed
        return self.code

    def save(self, *args, **kwargs):
        # Save the instance first
        super().save(*args, **kwargs)
        # Cache the name and symbol fields
        self.cache_name_and_symbol()

    def cache_name_and_symbol(self):
        # Caches the `name` and `symbol` fields for one hour using Django's caching framework
        cache_key = f"currency_{self.code}_name_symbol"
        cache.set(cache_key, {'name': self.name, 'symbol': self.symbol}, timeout=60*60)

    @classmethod
    def get_cached_name_and_symbol(cls, code):
        # Retrieves the cached `name` and `symbol` for a given currency code
        cache_key = f"currency_{code}_name_symbol"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        else:
            try:
                # If data is not in cache, fetch it from the database and cache it
                currency = cls.objects.get(code=code)
                currency.cache_name_and_symbol()
                return {'name': currency.name, 'symbol': currency.symbol}
            except cls.DoesNotExist:
                return None

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
    