import os
import django
import requests
import random
from decimal import Decimal
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

# Create Categories if missing
watch_cat, _ = Category.objects.get_or_create(name="Watches", defaults={"description": "Luxury and smart watches"})
apparel_cat, _ = Category.objects.get_or_create(name="Apparel", defaults={"description": "Clothing and dresses"})
accessories_cat, _ = Category.objects.get_or_create(name="Accessories", defaults={"description": "Fashion accessories"})

# New Products Data
new_products = [
    ("Elegant Evening Dress", apparel_cat, 150.00, "A stunning evening dress perfect for formal occasions.", "https://images.unsplash.com/photo-156616098393ce-6a75f1b26857?q=80&w=800&auto=format&fit=crop"),
    ("Summer Floral Dress", apparel_cat, 45.99, "Light and breezy floral dress for warm summer days.", "https://images.unsplash.com/photo-1572804013309-8c98e25e172a?q=80&w=800&auto=format&fit=crop"),
    ("Classic Chronograph Watch", watch_cat, 250.00, "Stainless steel chronograph watch with water resistance and premium build.", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?q=80&w=800&auto=format&fit=crop"),
    ("Minimalist Leather Watch", watch_cat, 120.00, "Slim, minimalist watch with a genuine leather strap.", "https://images.unsplash.com/photo-1508656986681-309199c0da5c?q=80&w=800&auto=format&fit=crop"),
    ("Luxury Gold Watch", watch_cat, 1200.00, "18k gold-plated luxury timepiece for the modern professional.", "https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?q=80&w=800&auto=format&fit=crop"),
    ("Designer Handbag", accessories_cat, 350.00, "Premium leather handbag with gold accents.", "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?q=80&w=800&auto=format&fit=crop"),
    ("Polarized Sunglasses", accessories_cat, 85.00, "UV400 polarized sunglasses with a stylish matte frame.", "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=800&auto=format&fit=crop"),
    ("Casual Denim Jacket", apparel_cat, 75.00, "Classic fit denim jacket, perfect for layering.", "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?q=80&w=800&auto=format&fit=crop"),
    ("Cocktail Party Dress", apparel_cat, 110.00, "Chic cocktail dress with intricate lace detailing.", "https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=800&auto=format&fit=crop"),
    ("Smart Fitness Watch", watch_cat, 199.99, "Advanced fitness tracking watch with heart-rate and sleep monitoring.", "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b0?q=80&w=800&auto=format&fit=crop"),
]

for name, cat, price, desc, url in new_products:
    p, created = Product.objects.get_or_create(
        name=name,
        defaults={
            "category": cat,
            "seller": admin_user,
            "description": desc,
            "short_description": desc[:50],
            "price": Decimal(str(price)),
            "status": "PUBLISHED", 
            "is_featured": random.choice([True, False])
        }
    )
    if created or not p.main_image:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                p.main_image.save(f"new_prod_{p.id}.jpg", ContentFile(resp.content), save=True)
                print(f"Added {name} with image!")
        except Exception as e:
            print(f"Failed image for {name}: {e}")

print("Successfully added watches, dresses, and accessories with images!")
