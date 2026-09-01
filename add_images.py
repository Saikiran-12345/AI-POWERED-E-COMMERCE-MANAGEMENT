import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

products = Product.objects.all()

image_urls = [
    "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=800&auto=format&fit=crop", # phone
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800&auto=format&fit=crop", # headphones
    "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?q=80&w=800&auto=format&fit=crop", # laptop
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12?q=80&w=800&auto=format&fit=crop", # smartwatch
    "https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=800&auto=format&fit=crop", # leather jacket
    "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=800&auto=format&fit=crop", # t-shirt
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=800&auto=format&fit=crop", # sneakers
    "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?q=80&w=800&auto=format&fit=crop", # chair
    "https://images.unsplash.com/photo-1495474472201-4475459345ee?q=80&w=800&auto=format&fit=crop", # coffee maker
    "https://images.unsplash.com/photo-1584990347449-a6ebbc4122d4?q=80&w=800&auto=format&fit=crop"  # pan
]

for i, p in enumerate(products):
    if not p.main_image:
        url = image_urls[i % len(image_urls)]
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                p.main_image.save(f"product_{p.id}.jpg", ContentFile(resp.content), save=True)
                print(f"Saved image for {p.name}")
        except Exception as e:
            print(f"Failed image for {p.name}: {e}")

print("Done assigning images!")
