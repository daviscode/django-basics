from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Currency, QRCode, Product

@receiver(post_save, sender=Product)
def capture_save(sender, instance, created, **kwargs):
    if created:
        print(f"Product {instance} created.")
        # Add your logic here to handle creation
    else:
        print(f"Product {instance} updated.")
        # Add your logic here to handle updates

@receiver(post_delete, sender=Product)
def capture_delete(sender, instance, **kwargs):
    print(f"Product {instance} deleted.")
    # Add your logic here to handle deletion
