import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser('admin@shopai.com', 'adminpass123')

# Create realistic categories
categories = [
    {"name": "Electronics", "description": "Gadgets and tech"},
    {"name": "Apparel", "description": "Clothing and fashion"},
    {"name": "Home & Garden", "description": "Furniture and tools"},
]

cat_objs = {}
for c in categories:
    cat, _ = Category.objects.get_or_create(name=c["name"], defaults={"description": c["description"]})
    cat_objs[c["name"]] = cat

# Create products
products = [
    ("Smartphone X Pro", "Electronics", 999.99, "Latest flagship smartphone with 120Hz OLED display, pro camera system, and all-day battery life."),
    ("Noise-Cancelling Headphones", "Electronics", 299.50, "Premium wireless headphones with active noise cancellation and spatial audio."),
    ("Gaming Laptop", "Electronics", 1499.00, "High-performance laptop featuring RTX graphics, 32GB RAM, and 1TB SSD for seamless gaming."),
    ("Smartwatch Series 5", "Electronics", 399.00, "Track your fitness, heart rate, and notifications on the go with this sleek smartwatch."),
    ("Vintage Leather Jacket", "Apparel", 199.99, "Classic brown leather jacket, tailored for a perfect fit and timeless style."),
    ("Organic Cotton T-Shirt", "Apparel", 24.99, "Super soft, breathable 100% organic cotton tee for everyday comfort."),
    ("Running Sneakers", "Apparel", 129.00, "Lightweight athletic shoes with shock-absorbing soles for long-distance runs."),
    ("Ergonomic Office Chair", "Home & Garden", 249.99, "Adjustable lumbar support and breathable mesh back for all-day comfort while working."),
    ("Smart Coffee Maker", "Home & Garden", 149.50, "Brew your morning coffee from your phone with this Wi-Fi enabled smart coffee maker."),
    ("Ceramic Non-Stick Pan", "Home & Garden", 45.00, "Durable, easy-to-clean frying pan perfect for healthy, oil-free cooking.")
]

for name, cat_name, price, desc in products:
    Product.objects.get_or_create(
        name=name,
        defaults={
            "category": cat_objs[cat_name],
            "seller": admin_user,
            "description": desc,
            "short_description": desc[:50],
            "price": Decimal(str(price)),
            "status": "PUBLISHED", 
            "is_featured": random.choice([True, False]),
        }
    )

print("Successfully added realistic e-commerce products and categories!")
