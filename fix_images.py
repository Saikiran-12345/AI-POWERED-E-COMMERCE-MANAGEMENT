import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

products = Product.objects.all()

fallback_image_urls = [
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?q=80&w=800&auto=format&fit=crop",
]

for p in products:
    if not p.main_image or not p.main_image.name:
        url = fallback_image_urls[p.id % len(fallback_image_urls)]
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                p.main_image.save(f"fallback_{p.id}.jpg", ContentFile(resp.content), save=True)
                print(f"Saved fallback image for {p.name}")
        except Exception as e:
            print(f"Failed fallback image for {p.name}: {e}")

print("Fixed all missing images!")
