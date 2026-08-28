"""
Management command to seed the database with realistic sample data.

Usage:
    python manage.py seed_data
    python manage.py seed_data --clear     # Clear existing data first
    python manage.py seed_data --minimal   # Create minimal data only

Generates:
- 1 Admin user
- 3 Seller accounts with profiles
- 20 Customer accounts
- 10 Product categories
- 100 Products
- Inventory for each product
- 200 Orders with items
- Payments
- Reviews
- Notifications
- Sample recommendations

⚠️ Uses synthetic data only — no real personal information.
"""

import random
import logging
from decimal import Decimal
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db import transaction

logger = logging.getLogger(__name__)


CATEGORIES = [
    ('Electronics', 'Gadgets, phones, laptops, and accessories'),
    ('Clothing', 'Fashion, apparel, and accessories'),
    ('Books', 'Fiction, non-fiction, textbooks, and more'),
    ('Home & Kitchen', 'Furniture, appliances, and kitchenware'),
    ('Sports & Fitness', 'Exercise equipment and sportswear'),
    ('Beauty & Health', 'Skincare, makeup, and wellness products'),
    ('Toys & Games', 'Toys, board games, and educational items'),
    ('Automotive', 'Car accessories and parts'),
    ('Food & Grocery', 'Packaged food and beverages'),
    ('Office Supplies', 'Stationery and work essentials'),
]

PRODUCTS_DATA = [
    # Electronics
    ('Samsung Galaxy S23', 'Electronics', 'Samsung', 79999, 10, 'Flagship smartphone with 200MP camera, Snapdragon 8 Gen 2 processor, and 5000mAh battery. Comes with S Pen.'),
    ('Apple iPhone 15', 'Electronics', 'Apple', 89999, 15, 'Latest iPhone with A16 Bionic chip, USB-C charging, and ProMotion display. Best-in-class performance.'),
    ('Sony WH-1000XM5', 'Electronics', 'Sony', 29999, 0, 'Industry-leading noise canceling headphones with 30-hour battery life and exceptional sound quality.'),
    ('Dell XPS 15 Laptop', 'Electronics', 'Dell', 149999, 12, '15.6-inch OLED display, Intel Core i9, 32GB RAM, 1TB SSD. Perfect for professionals and creators.'),
    ('Canon EOS R6', 'Electronics', 'Canon', 249999, 8, 'Full-frame mirrorless camera with 20MP sensor, 4K60 video, and advanced autofocus. Ideal for photographers.'),
    ('Apple iPad Pro', 'Electronics', 'Apple', 119999, 5, '12.9-inch Liquid Retina XDR display, M2 chip, Wi-Fi 6E. Perfect for creative professionals.'),
    ('JBL Flip 6', 'Electronics', 'JBL', 9999, 0, 'Portable Bluetooth speaker with 360-degree sound, IP67 waterproof, and 12-hour playtime.'),
    ('Logitech MX Master 3', 'Electronics', 'Logitech', 9999, 5, 'Advanced wireless mouse with ultra-fast scrolling, Bolt USB receiver, and 70-day battery life.'),

    # Clothing
    ('Levi\'s 501 Jeans', 'Clothing', 'Levi\'s', 4999, 20, 'Classic straight-leg jeans in medium wash. Made from 100% cotton for lasting comfort and style.'),
    ('Nike Air Max 270', 'Clothing', 'Nike', 12999, 15, 'Lifestyle sneakers with the largest Air unit in heel for cushioning and comfort all day long.'),
    ('Adidas Ultraboost 23', 'Clothing', 'Adidas', 15999, 10, 'Running shoes with Boost midsole for energy return and Primeknit+ upper for sock-like fit.'),
    ('H&M Slim-Fit Shirt', 'Clothing', 'H&M', 1499, 0, 'Slim-fit oxford shirt in 100% cotton. Perfect for casual or semi-formal occasions.'),
    ('Woodland Trek Boots', 'Clothing', 'Woodland', 6999, 12, 'Full-grain leather trekking boots with anti-skid rubber sole and waterproof construction.'),
    ('Zara Formal Blazer', 'Clothing', 'Zara', 5999, 25, 'Slim-cut blazer in premium fabric blend. Suitable for office, events, and formal occasions.'),

    # Books
    ('The Alchemist', 'Books', 'Paulo Coelho', 299, 0, 'A philosophical novel about a young shepherd\'s journey to find treasure and his personal legend.'),
    ('Atomic Habits', 'Books', 'James Clear', 499, 10, 'A practical guide to building good habits and breaking bad ones using the science of behavior change.'),
    ('Clean Code', 'Books', 'Robert C. Martin', 699, 0, 'A handbook of agile software craftsmanship for writing readable, maintainable, and clean code.'),
    ('Python Crash Course', 'Books', 'Eric Matthes', 599, 15, 'A hands-on, project-based introduction to programming in Python for beginners.'),
    ('Deep Learning', 'Books', 'Ian Goodfellow', 999, 5, 'Comprehensive introduction to deep learning from leading researchers at Google Brain and NYU.'),

    # Home & Kitchen
    ('Instant Pot Duo', 'Home & Kitchen', 'Instant Pot', 7999, 12, '7-in-1 electric pressure cooker — pressure cooker, slow cooker, rice cooker, steamer, sauté, and more.'),
    ('Philips Air Fryer', 'Home & Kitchen', 'Philips', 9999, 8, 'Digital air fryer with TurboStar technology. Fry, bake, grill, and roast with up to 90% less fat.'),
    ('IKEA KALLAX Shelf', 'Home & Kitchen', 'IKEA', 5999, 20, 'Versatile cube shelf unit perfect for storage and display. Available in multiple colors and sizes.'),
    ('Dyson V15 Vacuum', 'Home & Kitchen', 'Dyson', 59999, 5, 'Cordless vacuum with laser dust detection and automatic suction adjustment for thorough cleaning.'),

    # Sports & Fitness
    ('Fitbit Charge 6', 'Sports & Fitness', 'Fitbit', 14999, 10, 'Advanced fitness tracker with built-in GPS, 24/7 heart rate monitoring, and 7-day battery life.'),
    ('Yoga Mat Premium', 'Sports & Fitness', 'Liforme', 4999, 0, 'Eco-friendly, alignment-guided yoga mat with patented GripForest texture and superior grip.'),
    ('Bowflex Dumbbells', 'Sports & Fitness', 'Bowflex', 29999, 15, 'Adjustable dumbbells replacing 15 sets of weights. Quick weight change mechanism, 2kg to 24kg.'),
    ('Trek Marlin 5 Bike', 'Sports & Fitness', 'Trek', 39999, 8, 'Versatile mountain bike with Shimano components, hydraulic disc brakes, and 29-inch wheels.'),

    # Beauty & Health
    ('Cetaphil Moisturizer', 'Beauty & Health', 'Cetaphil', 699, 0, 'Gentle moisturizing lotion for sensitive skin. Non-greasy formula suitable for daily use on face and body.'),
    ('L\'Oreal Serum', 'Beauty & Health', 'L\'Oreal', 1299, 20, 'Vitamin C brightening serum with 12% pure vitamin C, niacinamide, and salicylic acid.'),
    ('Oral-B Electric Toothbrush', 'Beauty & Health', 'Oral-B', 4999, 10, 'Rechargeable electric toothbrush with pressure sensor and smart timer for optimal cleaning.'),

    # Toys & Games
    ('LEGO Technic Set', 'Toys & Games', 'LEGO', 3999, 15, '2-in-1 model building set with 706 pieces. Build a race car or dragster — great for ages 10+.'),
    ('Monopoly Classic', 'Toys & Games', 'Hasbro', 1299, 0, 'The classic real estate trading board game for the whole family. 2-8 players, ages 8+.'),
    ('Nintendo Switch', 'Toys & Games', 'Nintendo', 32999, 8, 'Versatile gaming console that plays at home on TV or on the go in handheld mode. 4000+ games.'),

    # Automotive
    ('Garmin GPS Navigator', 'Automotive', 'Garmin', 14999, 12, '7-inch touchscreen GPS navigator with lifetime maps, Bluetooth, and driver alerts.'),
    ('Bosch Car Vacuum', 'Automotive', 'Bosch', 3999, 0, 'Compact 12V car vacuum with strong suction, washable filter, and 5-meter cord.'),

    # Food & Grocery
    ('Organic Honey 500g', 'Food & Grocery', 'Dabur', 399, 0, '100% pure and natural organic honey. No artificial flavors or preservatives.'),
    ('Tata Tea Premium', 'Food & Grocery', 'Tata', 249, 0, 'Strong and flavorful tea blend made from finest Assam tea leaves. 500g pack.'),

    # Office Supplies
    ('Parker Pen Set', 'Office Supplies', 'Parker', 1999, 15, 'Premium ballpoint pen set in a gift box. Smooth writing with smear-free ink.'),
    ('A4 Printer Paper', 'Office Supplies', 'ITC', 399, 0, 'High-quality 80gsm A4 paper ream (500 sheets). Suitable for all inkjet and laser printers.'),
]


class Command(BaseCommand):
    """Management command to populate the database with sample data."""

    help = 'Seed the database with realistic sample data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )
        parser.add_argument(
            '--minimal',
            action='store_true',
            help='Create minimal data (fewer customers and orders)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Starting seed data generation...'))

        if options['clear']:
            self._clear_data()

        minimal = options.get('minimal', False)

        try:
            with transaction.atomic():
                categories = self._create_categories()
                self.stdout.write(f'  ✓ {len(categories)} categories created')

                admin = self._create_admin()
                self.stdout.write(f'  ✓ Admin user: {admin.email}')

                sellers = self._create_sellers()
                self.stdout.write(f'  ✓ {len(sellers)} seller accounts created')

                num_customers = 5 if minimal else 20
                customers = self._create_customers(num_customers)
                self.stdout.write(f'  ✓ {len(customers)} customer accounts created')

                products = self._create_products(sellers, categories)
                self.stdout.write(f'  ✓ {len(products)} products created')

                num_orders = 10 if minimal else 60
                orders = self._create_orders(customers, products, num_orders)
                self.stdout.write(f'  ✓ {len(orders)} orders created')

                reviews = self._create_reviews(customers, products, orders)
                self.stdout.write(f'  ✓ {len(reviews)} reviews created')

                self._create_notifications(customers, orders)
                self.stdout.write('  ✓ Sample notifications created')

                self.stdout.write(self.style.SUCCESS(
                    '\n✅ Seed data created successfully!\n'
                    '   Login credentials:\n'
                    '   Admin:    admin@shopai.com / Admin@123\n'
                    '   Seller:   seller1@shopai.com / Seller@123\n'
                    '   Customer: customer1@shopai.com / Customer@123\n'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Seed data failed: {e}'))
            logger.exception('Seed data error')
            raise

    def _clear_data(self):
        """Clear all seeded data."""
        from apps.accounts.models import User
        self.stdout.write('  🗑  Clearing existing data...')
        User.objects.filter(email__endswith='@shopai.com').delete()
        self.stdout.write('  ✓ Data cleared')

    def _create_categories(self):
        """Create product categories."""
        from apps.products.models import Category
        categories = []
        for name, description in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={'description': description, 'is_active': True}
            )
            categories.append(cat)
        return categories

    def _create_admin(self):
        """Create the admin superuser."""
        from apps.accounts.models import User, UserRole
        user, created = User.objects.get_or_create(
            email='admin@shopai.com',
            defaults={
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'is_email_verified': True,
            }
        )
        if created:
            user.set_password('Admin@123')
            user.save()
        return user

    def _create_sellers(self):
        """Create seller accounts."""
        from apps.accounts.models import User, UserRole
        from apps.sellers.models import SellerProfile

        sellers_data = [
            ('seller1@shopai.com', 'Rahul', 'Sharma', 'TechMart India', 'Leading electronics and gadgets store'),
            ('seller2@shopai.com', 'Priya', 'Patel', 'Fashion Hub', 'Trendy clothing and accessories'),
            ('seller3@shopai.com', 'Amit', 'Kumar', 'BookWorld', 'Books, stationery, and educational materials'),
        ]

        sellers = []
        for email, first, last, biz_name, bio in sellers_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'role': UserRole.SELLER,
                    'is_active': True,
                    'is_email_verified': True,
                }
            )
            if created:
                user.set_password('Seller@123')
                user.save()

            SellerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'business_name': biz_name,
                    'bio': bio,
                    'verification_status': 'VERIFIED',
                    'commission_rate': Decimal('8.5'),
                }
            )
            sellers.append(user)
        return sellers

    def _create_customers(self, count: int):
        """Create customer accounts."""
        from apps.accounts.models import User, UserRole
        from apps.customers.models import Customer
        from apps.wishlist.models import Wishlist

        first_names = ['Aisha', 'Raj', 'Meera', 'Vikram', 'Sunita', 'Arjun',
                       'Pooja', 'Kiran', 'Deepak', 'Ananya', 'Suresh', 'Nisha',
                       'Rohit', 'Kavya', 'Manish', 'Divya', 'Sanjay', 'Lakshmi',
                       'Harish', 'Sneha']
        last_names = ['Singh', 'Gupta', 'Sharma', 'Patel', 'Kumar', 'Verma',
                      'Joshi', 'Nair', 'Reddy', 'Mehta']
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']
        states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana', 'Maharashtra', 'West Bengal']

        customers = []
        for i in range(count):
            first = first_names[i % len(first_names)]
            last = last_names[i % len(last_names)]
            email = f'customer{i+1}@shopai.com'

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'role': UserRole.CUSTOMER,
                    'is_active': True,
                    'is_email_verified': True,
                    'phone_number': f'+91 9{random.randint(100000000, 999999999)}',
                }
            )
            if created:
                user.set_password('Customer@123')
                user.save()

            # Update profile
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.city = cities[i % len(cities)]
                profile.state = states[i % len(states)]
                profile.address_line1 = f'{random.randint(1, 999)}, Sample Street'
                profile.pincode = f'{random.randint(100000, 999999)}'
                profile.country = 'India'
                profile.save()

            # Create customer profile
            customer, _ = Customer.objects.get_or_create(
                user=user,
                defaults={'loyalty_points': random.randint(0, 500)}
            )

            # Create wishlist
            Wishlist.objects.get_or_create(customer=customer)
            customers.append(customer)

        return customers

    def _create_products(self, sellers, categories):
        """Create products with inventory."""
        from apps.products.models import Product, ProductStatus
        from apps.inventory.models import Inventory

        cat_map = {cat.name: cat for cat in categories}
        products = []

        for i, (name, cat_name, brand, price, discount, description) in enumerate(PRODUCTS_DATA):
            seller = sellers[i % len(sellers)]
            category = cat_map.get(cat_name, categories[0])
            stock = random.randint(0, 200)

            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'seller': seller,
                    'category': category,
                    'brand': brand,
                    'price': Decimal(str(price)),
                    'discount_percent': Decimal(str(discount)),
                    'cost_price': Decimal(str(price * 0.6)),
                    'description': description,
                    'short_description': description[:200],
                    'status': ProductStatus.ACTIVE if stock > 0 else ProductStatus.OUT_OF_STOCK,
                    'is_featured': random.random() < 0.2,
                    'average_rating': round(random.uniform(3.0, 5.0), 1),
                    'review_count': random.randint(0, 150),
                    'purchase_count': random.randint(0, 500),
                    'view_count': random.randint(50, 5000),
                    'tags': f'{cat_name.lower()},{brand.lower()}',
                }
            )

            # Create or update inventory
            Inventory.objects.get_or_create(
                product=product,
                defaults={
                    'quantity': stock,
                    'reorder_point': 10,
                    'reorder_quantity': 50,
                }
            )
            products.append(product)

        return products

    def _create_orders(self, customers, products, count: int):
        """Create sample orders with items and payments."""
        from apps.orders.models import Order, OrderItem, OrderStatus
        from apps.payments.models import Payment, PaymentMethod, PaymentStatus
        from apps.analytics.models import SalesRecord

        statuses = [
            OrderStatus.PENDING, OrderStatus.CONFIRMED,
            OrderStatus.PROCESSING, OrderStatus.SHIPPED,
            OrderStatus.DELIVERED, OrderStatus.DELIVERED,
            OrderStatus.DELIVERED, OrderStatus.CANCELLED,
        ]
        payment_methods = [
            PaymentMethod.CARD, PaymentMethod.UPI,
            PaymentMethod.NET_BANKING, PaymentMethod.CASH_ON_DELIVERY
        ]

        orders = []
        for i in range(count):
            customer = random.choice(customers)
            status = random.choice(statuses)
            days_ago = random.randint(1, 365)
            order_date = timezone.now() - timedelta(days=days_ago)

            order_products = random.sample(products, k=random.randint(1, 4))

            # Calculate totals
            subtotal = sum(p.discounted_price * random.randint(1, 3) for p in order_products)
            total = subtotal

            order = Order.objects.create(
                customer=customer,
                status=status,
                subtotal=subtotal,
                total_amount=total,
                shipping_name=customer.user.get_full_name(),
                shipping_email=customer.user.email,
                shipping_address1='123 Sample Street',
                shipping_city=getattr(customer.user.profile, 'city', 'Mumbai'),
                shipping_state=getattr(customer.user.profile, 'state', 'Maharashtra'),
                shipping_pincode=getattr(customer.user.profile, 'pincode', '400001'),
                created_at=order_date,
            )
            # Override auto_now_add
            Order.objects.filter(pk=order.pk).update(created_at=order_date)

            # Create order items
            for product in order_products:
                qty = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=qty,
                    unit_price=product.discounted_price,
                    total_price=product.discounted_price * qty,
                    seller=product.seller,
                )

                # Create sales record for delivered orders
                if status == OrderStatus.DELIVERED:
                    SalesRecord.objects.create(
                        date=order_date.date(),
                        product=product,
                        category=product.category,
                        seller=product.seller,
                        quantity=qty,
                        revenue=product.discounted_price * qty,
                        order=order,
                    )

            # Create payment
            method = random.choice(payment_methods)
            payment_status = PaymentStatus.SUCCESS if status != OrderStatus.CANCELLED else PaymentStatus.FAILED
            Payment.objects.create(
                order=order,
                amount=total,
                method=method,
                status=payment_status,
            )

            orders.append(order)

        # Update customer stats
        for customer in customers:
            customer.update_stats()

        return orders

    def _create_reviews(self, customers, products, orders):
        """Create product reviews for delivered orders."""
        from apps.orders.models import OrderItem, OrderStatus
        from apps.reviews.models import Review

        reviews = []
        review_templates = [
            ('Excellent product!', 'Really happy with this purchase. Quality is top-notch and delivery was fast.'),
            ('Good value for money', 'Product works as described. Good quality for the price.'),
            ('Satisfied with purchase', 'Decent product. Packaging was good and arrived on time.'),
            ('Amazing quality', 'Exceeded my expectations. Will definitely buy again.'),
            ('Okay but could be better', 'Product is okay, not exceptional. Slightly overpriced.'),
            ('Highly recommended', 'One of the best purchases I\'ve made. Excellent customer experience.'),
            ('Works perfectly', 'Exactly what I needed. Instructions were clear, setup was easy.'),
        ]

        for customer in customers:
            delivered_items = OrderItem.objects.filter(
                order__customer=customer,
                order__status=OrderStatus.DELIVERED,
            ).select_related('product')[:5]

            for item in delivered_items:
                if item.product and not Review.objects.filter(product=item.product, customer=customer).exists():
                    title, body = random.choice(review_templates)
                    rating = random.choices([3, 4, 4, 5, 5], weights=[10, 20, 20, 30, 20])[0]
                    review = Review.objects.create(
                        product=item.product,
                        customer=customer,
                        rating=rating,
                        title=title,
                        body=body,
                        is_approved=True,
                        is_verified_purchase=True,
                    )
                    reviews.append(review)

        return reviews

    def _create_notifications(self, customers, orders):
        """Create sample notifications."""
        from apps.notifications.models import Notification

        for customer in customers[:10]:
            Notification.create_notification(
                user=customer.user,
                notification_type='ORDER_CONFIRMED',
                title='Order Confirmed',
                message='Your order has been confirmed and is being processed.',
                link='/orders/',
            )
            Notification.create_notification(
                user=customer.user,
                notification_type='RECOMMENDATION',
                title='New Recommendations Available',
                message='We have found new products you might love!',
                link='/recommendations/',
            )
