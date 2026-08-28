# AI-Powered E-Commerce Management & Recommendation SaaS

A full-stack Django SaaS platform with machine learning capabilities for e-commerce management, analytics, and AI-powered product recommendations.

## 🚀 Features

- **Multi-role system**: Customer, Seller, Admin
- **Product management**: Full CRUD with categories, search, filtering, pagination
- **Shopping cart & wishlist**
- **Order management** with status tracking
- **Mock payment system** (Card, UPI, Net Banking, COD)
- **Inventory management** with low-stock alerts
- **Seller dashboard** with sales analytics
- **Admin dashboard** with full control
- **ML Recommendation Engine** (content-based + popularity)
- **Customer Segmentation** (K-Means clustering)
- **Demand Forecasting** (time-series ML)
- **Churn Prediction** (classification)
- **Fraud/Anomaly Detection** (Isolation Forest)
- **Review & Rating system**
- **Internal notifications**
- **Audit logging**
- **REST API** (Django REST Framework)
- **Charts & visualizations** (Chart.js)

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Django 4.2, DRF |
| Frontend | HTML5, CSS3, Vanilla JS, Chart.js |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ML | scikit-learn, Pandas, NumPy |
| Testing | pytest-django, Django TestCase |

## 📋 Prerequisites

- Python 3.10+
- pip
- Git
- (Optional) PostgreSQL for production

## ⚡ Quick Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd "E-COMMERCE MANAGEMENT & RECOMMENDATION SAAS"
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your settings (SQLite works out of the box)
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create admin user
```bash
python manage.py createsuperuser
```

### 7. Seed sample data
```bash
python manage.py seed_data
```

### 8. Start the server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 👤 Default Development Credentials

After running `seed_data`:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@shopai.com | Admin@123 |
| Seller | seller@shopai.com | Seller@123 |
| Customer | customer@shopai.com | Customer@123 |

## 🗄️ Database Setup

### SQLite (Default — no setup required)
The app uses SQLite by default. Just run migrations.

### PostgreSQL (Production)
```bash
# Create database
createdb ecommerce_saas

# Update .env
USE_SQLITE=False
DB_NAME=ecommerce_saas
DB_USER=your_user
DB_PASSWORD=your_password
```

## 🧪 Running Tests
```bash
# All tests
pytest

# Specific app
pytest apps/products/tests.py

# With coverage
pytest --cov=apps

# Django test runner
python manage.py test apps
```

## 🤖 ML Pipeline

### Train all models
```bash
python manage.py train_ml_models
```

### Generate recommendations
```bash
python manage.py generate_recommendations
```

### Run segmentation
```bash
python manage.py run_segmentation
```

### Run forecasting
```bash
python manage.py run_forecasting
```

## 📁 Project Structure

```
ecommerce_saas/
├── manage.py
├── requirements.txt
├── .env.example
├── config/           # Django settings
├── apps/
│   ├── accounts/     # Auth & user management
│   ├── customers/    # Customer profiles
│   ├── products/     # Products & categories
│   ├── cart/         # Shopping cart
│   ├── wishlist/     # Wishlist
│   ├── orders/       # Order management
│   ├── payments/     # Mock payment system
│   ├── inventory/    # Inventory management
│   ├── sellers/      # Seller management
│   ├── reviews/      # Reviews & ratings
│   ├── recommendations/ # ML recommendations
│   ├── analytics/    # Analytics & dashboards
│   ├── ml/           # ML pipelines
│   ├── forecasting/  # Demand forecasting
│   ├── fraud_detection/ # Anomaly detection
│   ├── notifications/ # Internal notifications
│   ├── reports/      # Reporting module
│   ├── audit/        # Audit logging
│   └── dashboard/    # Dashboard aggregation
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── data/             # Sample & processed data
├── ml_models/        # Saved ML model files
└── tests/            # Test suite
```

## 🔌 API Documentation

The REST API is available at `/api/v1/`

Key endpoints:
- `POST /api/v1/auth/login/` — Login
- `GET /api/v1/products/` — Product listing
- `GET /api/v1/products/{id}/` — Product detail
- `GET /api/v1/cart/` — Cart contents
- `POST /api/v1/cart/add/` — Add to cart
- `GET /api/v1/orders/` — Order listing
- `POST /api/v1/orders/create/` — Create order
- `GET /api/v1/recommendations/` — Get recommendations
- `GET /api/v1/analytics/dashboard/` — Dashboard data

## 🔒 Security Notes

- CSRF protection enabled on all forms
- Password hashing via Django's PBKDF2
- Role-based access control
- Input validation on all endpoints
- SQL injection protection via Django ORM
- XSS-safe template rendering

## ⚠️ Disclaimer

The payment system is **simulated for demonstration purposes only**. No real financial transactions occur. The fraud detection module is an educational demo, not a production banking system.

## 📄 License

MIT License — Educational/Portfolio Use
