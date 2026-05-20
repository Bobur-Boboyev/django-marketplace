<div align="center">
  <img src="https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django&logoColor=white" alt="Django Badge">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  <img src="https://img.shields.io/badge/DRF-3.17-red?style=for-the-badge&logo=django&logoColor=white" alt="DRF Badge">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL Badge">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Badge">
  <img src="https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis Badge">
  <img src="https://img.shields.io/badge/Celery-Task%20Queue-37B24D?style=for-the-badge&logo=celery&logoColor=white" alt="Celery Badge">
</div>

---

<h1 align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/833/833340.png" width="50" alt="Marketplace Icon">
  <br>Django Marketplace
</h1>

<p align="center">
  <strong>A powerful, scalable, and production-ready e-commerce marketplace platform built with Django REST Framework</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/Bobur-Boboyev/django-marketplace?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/last-commit/Bobur-Boboyev/django-marketplace?style=flat-square" alt="Last Commit">
</p>

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Docker Deployment](#docker-deployment)
- [Database](#database)
- [Authentication](#authentication)
- [Payment Integration](#payment-integration)
- [Background Tasks](#background-tasks)
- [Contributing](#contributing)
- [Support](#support)

---

## Features

<table>
  <tr>
    <td align="center" width="50%">
      <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png" width="40" alt="User Management">
      <br><b>User Management</b><br>
      Complete authentication & authorization system with JWT tokens
    </td>
    <td align="center" width="50%">
      <img src="https://cdn-icons-png.flaticon.com/512/950/950157.png" width="40" alt="Product Catalog">
      <br><b>Product Catalog</b><br>
      Dynamic product management with categories & filtering
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/512/924/924514.png" width="40" alt="Shopping Cart">
      <br><b>Shopping Cart</b><br>
      Persistent cart with real-time updates
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/512/3050/3050159.png" width="40" alt="Orders">
      <br><b>Order Management</b><br>
      Complete order lifecycle tracking & management
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/512/3597/3597084.png" width="40" alt="Payments">
      <br><b>Payment Integration</b><br>
      Payme & PayTech payment gateway support
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/512/1998/1998925.png" width="40" alt="Admin Panel">
      <br><b>Admin Dashboard</b><br>
      Jazzmin-powered admin interface
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/512/875/875122.png" width="40" alt="Task Queue">
      <br><b>Async Tasks</b><br>
      Celery & Redis for background processing
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/512/1995/1995505.png" width="40" alt="API">
      <br><b>REST API</b><br>
      Fully documented RESTful API endpoints
    </td>
  </tr>
</table>

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| <img src="https://cdn-icons-png.flaticon.com/512/3702/3702126.png" width="30"> | **Framework** | Django REST Framework | 5.2.x |
| <img src="https://cdn-icons-png.flaticon.com/512/919/919825.png" width="30"> | **Language** | Python | 3.9+ |
| <img src="https://cdn-icons-png.flaticon.com/512/4248/4248443.png" width="30"> | **Database** | PostgreSQL | 12+ |
| <img src="https://cdn-icons-png.flaticon.com/512/3371/3371940.png" width="30"> | **Cache/Queue** | Redis | 6.0+ |
| <img src="https://cdn-icons-png.flaticon.com/512/919/919836.png" width="30"> | **Task Queue** | Celery | 5.3.x |
| <img src="https://cdn-icons-png.flaticon.com/512/2066/2066393.png" width="30"> | **Authentication** | JWT (djangorestframework-simplejwt) | 5.5.x |
| <img src="https://cdn-icons-png.flaticon.com/512/1182/1182948.png" width="30"> | **Web Server** | Gunicorn | 23.0.0 |
| <img src="https://cdn-icons-png.flaticon.com/512/3596/3596061.png" width="30"> | **Containerization** | Docker & Docker Compose | Latest |

---

## Project Structure

```
django-marketplace/
│
├── config/                    # Project configuration
│   ├── settings.py           # Main settings
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── apps/                      # Django applications
│   ├── users/                # User management & authentication
│   ├── products/             # Product catalog
│   ├── orders/               # Order management
│   ├── payments/             # Payment processing
│   ├── cart/                 # Shopping cart
│   └── reviews/              # Product reviews & ratings
│
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS)
├── docker/                   # Docker configuration
│   └── entrypoint.sh         # Container startup script
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Multi-container setup
├── .env.sample              # Environment variables template
└── README.md                # This file
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- Redis 6.0 or higher
- Docker & Docker Compose (optional)
- pip (Python package manager)

### Method 1: Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bobur-Boboyev/django-marketplace.git
   cd django-marketplace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.sample .env
   ```

5. **Edit .env file with your configuration**
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@localhost:5432/django_marketplace
   REDIS_URL=redis://localhost:6379/0
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

### Method 2: Docker Installation

```bash
# Clone repository
git clone https://github.com/Bobur-Boboyev/django-marketplace.git
cd django-marketplace

# Build and run containers
docker-compose up -d

# Run migrations inside container
docker-compose exec web python manage.py migrate

# Create superuser inside container
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

---

## Configuration

### Environment Variables (.env)

```env
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://marketplace_user:password@db:5432/django_marketplace
DB_NAME=django_marketplace
DB_USER=marketplace_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis & Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Payment Gateway Keys
PAYME_MERCHANT_ID=your-payme-merchant-id
PAYME_ACCOUNT_KEY=your-payme-account-key
PAYTECH_MERCHANT_ID=your-paytech-merchant-id
PAYTECH_SECRET_KEY=your-paytech-secret-key

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (Optional)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

---

## Running the Application

### Development Server

```bash
# Start Django development server
python manage.py runserver

# Access application
# Frontend: http://localhost:3000 (if frontend configured)
# API: http://localhost:8000/api/
# Admin Panel: http://localhost:8000/admin/
```

### Production Server with Gunicorn

```bash
# Install gunicorn (already in requirements.txt)
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
```

### Start Celery Worker (for background tasks)

```bash
# Terminal 1: Start Celery worker
celery -A config worker -l info

# Terminal 2: Start Celery Beat (scheduler)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| POST | `/api/auth/logout/` | User logout |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/{id}/` | Get product details |
| POST | `/api/products/` | Create product (Admin) |
| PUT | `/api/products/{id}/` | Update product (Admin) |
| DELETE | `/api/products/{id}/` | Delete product (Admin) |

### Shopping Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/` | View cart |
| POST | `/api/cart/add/` | Add item to cart |
| PUT | `/api/cart/update/` | Update cart item |
| DELETE | `/api/cart/remove/{id}/` | Remove item from cart |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List user orders |
| POST | `/api/orders/` | Create new order |
| GET | `/api/orders/{id}/` | Get order details |
| PUT | `/api/orders/{id}/cancel/` | Cancel order |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/initiate/` | Initiate payment |
| POST | `/api/payments/callback/` | Payment callback |
| GET | `/api/payments/{id}/status/` | Check payment status |

---

## Docker Deployment

### Docker Compose Services

```yaml
Services:
  - web: Django application (Gunicorn)
  - db: PostgreSQL database
  - redis: Redis cache & message broker
  - celery_worker: Celery worker for async tasks
  - celery_beat: Celery scheduler
```

### Docker Commands

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Remove volumes (WARNING: Data loss)
docker-compose down -v

# Execute command in container
docker-compose exec web python manage.py migrate
```

### Accessing Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Django API | `http://localhost:8000` | N/A |
| Admin Panel | `http://localhost:8000/admin/` | Superuser |
| PostgreSQL | `localhost:5432` | Check .env |
| Redis | `localhost:6379` | N/A |

---

## Database

### Models Overview

**User Model**
- Custom user model with email authentication
- Role-based access control (Admin, Seller, Buyer)
- Profile information & contact details

**Product Model**
- Title, description, price, quantity
- Category & subcategory relationship
- Image uploads & media management
- Rating & review system

**Order Model**
- Order items with quantities & prices
- Order status tracking (Pending, Processing, Shipped, Delivered)
- Payment status tracking
- Timestamps for creation & updates

**Payment Model**
- Payment method (Payme, PayTech, Card)
- Transaction ID & reference
- Payment status & timestamps
- Refund tracking

### Running Migrations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations

# Reverse migration
python manage.py migrate app_name 0001
```

---

## Authentication

### JWT Token Authentication

1. **Register User**
   ```bash
   POST /api/auth/register/
   {
     "email": "user@example.com",
     "password": "securepassword123",
     "first_name": "John",
     "last_name": "Doe"
   }
   ```

2. **Login**
   ```bash
   POST /api/auth/login/
   {
     "email": "user@example.com",
     "password": "securepassword123"
   }
   ```

3. **Response**
   ```json
   {
     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "id": 1,
       "email": "user@example.com",
       "first_name": "John"
     }
   }
   ```

4. **Using Token in Requests**
   ```bash
   Authorization: Bearer <access_token>
   ```

---

## Payment Integration

### Supported Payment Providers

**1. Payme**
- Merchant ID setup
- Account key configuration
- Transaction verification

**2. PayTech**
- API key setup
- Merchant configuration
- Payment status tracking

### Example Payment Flow

```python
# 1. Initialize payment
POST /api/payments/initiate/
{
  "order_id": 123,
  "amount": 100000,
  "payment_method": "payme"
}

# 2. User completes payment on provider's portal
# 3. Payment callback received
POST /api/payments/callback/
{
  "transaction_id": "...",
  "status": "SUCCESS"
}

# 4. Order status updated automatically
```

---

## Background Tasks

### Celery Tasks Configuration

Tasks are executed asynchronously using Celery:

```python
# Example tasks
- send_order_confirmation_email()
- process_payment_status()
- update_inventory()
- generate_invoice()
- cleanup_expired_carts()
```

### Running Tasks

```bash
# Start Celery worker
celery -A config worker -l info

# Start Celery Beat scheduler
celery -A config beat -l info

# Monitor tasks
celery -A config events
```

---

## Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.products

# Run with verbose output
python manage.py test -v 2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Generate coverage report
coverage run --source='.' manage.py test
coverage report --omit="*/migrations/*,*/tests/*"
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
# Update DATABASE_URL in .env
# Run migrations again
python manage.py migrate
```

**2. Redis Connection Error**
```bash
# Ensure Redis is running
redis-server
# Check REDIS_URL in .env
```

**3. Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput
```

**4. Module Not Found**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**5. Port Already in Use**
```bash
# Change port in runserver
python manage.py runserver 8001
```

---

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/django-marketplace.git
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open Pull Request**
   - Describe changes clearly
   - Add screenshots if UI-related
   - Reference related issues

---

## Security

### Important Security Practices

- ✅ Change `SECRET_KEY` in production
- ✅ Set `DEBUG=False` in production
- ✅ Use HTTPS only
- ✅ Enable CSRF protection
- ✅ Validate all user inputs
- ✅ Use environment variables for secrets
- ✅ Regular security updates
- ✅ SQL injection prevention via ORM

---

## Performance Optimization

### Implemented Optimizations

- Database query optimization with `select_related()` & `prefetch_related()`
- Redis caching for frequently accessed data
- Celery async tasks for long-running operations
- CDN support for static files
- Database indexing on frequently queried fields
- Pagination for large result sets

---

## Roadmap

- [ ] Mobile app (Flutter/React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-vendor marketplace
- [ ] AI-powered recommendations
- [ ] Real-time notifications
- [ ] Subscription model
- [ ] Advanced search & filters
- [ ] Wishlist functionality

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support & Contact

<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://cdn-icons-png.flaticon.com/512/2504/2504839.png" width="40"><br>
      <b>Email</b><br>
      <a href="mailto:support@marketplace.com">support@marketplace.com</a>
    </td>
    <td align="center" width="33%">
      <img src="https://cdn-icons-png.flaticon.com/512/3128/3128222.png" width="40"><br>
      <b>GitHub Issues</b><br>
      <a href="https://github.com/Bobur-Boboyev/django-marketplace/issues">Report Bug</a>
    </td>
    <td align="center" width="33%">
      <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" width="40"><br>
      <b>Telegram</b><br>
      <a href="https://t.me/django_marketplace">@django_marketplace</a>
    </td>
  </tr>
</table>

---

## Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL](https://www.postgresql.org/)
- All open-source contributors

---

<div align="center">
  <img src="https://img.shields.io/badge/Built%20with-❤️-red?style=for-the-badge" alt="Built with love">
  <br>
  <p><b>Made with ❤️ by Bobur Boboyev</b></p>
  <p>If you found this helpful, please give it a ⭐ on GitHub!</p>
</div>
