# BookWorld - Online Book Store with AI Recommendation System

A full-stack e-commerce application for selling books with an AI-powered recommendation engine using collaborative filtering.

![BookWorld](https://img.shields.io/badge/BookWorld-v1.0-blue)
![Django](https://img.shields.io/badge/Django-4.2.13-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)
- [Recommendation System](#recommendation-system)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)

---

## ✨ Features

### User Features
- **User Authentication**: Register, login, logout with secure password hashing
- **Profile Management**: Edit profile, manage addresses, view preferences
- **Book Browsing**: Search, filter, and browse books by category
- **Shopping Cart**: Add/remove books, update quantities
- **Checkout**: Multi-step checkout with payment simulation
- **Order Tracking**: View order history and status
- **Reviews & Ratings**: Leave reviews and rate books
- **Wishlist**: Save favorite books for later
- **Personalized Recommendations**: AI-powered book suggestions

### Admin Features
- **Admin Dashboard**: View sales statistics and metrics
- **User Management**: Manage users and roles
- **Book Management**: Add, update, delete books and categories
- **Order Management**: View and update order status
- **Analytics**: Sales trends, user engagement, category performance
- **Content Moderation**: Manage reviews and ratings

### AI/ML Features
- **Collaborative Filtering**: Matrix factorization-based recommendations
- **User Similarity**: Find similar users based on preferences
- **Click-through Tracking**: Track user interactions
- **Model Training**: Periodic model retraining for accuracy

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2.13
- **Database**: MySQL 8.0+
- **ORM**: Django ORM
- **Task Queue**: Celery (optional)

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS, jQuery (optional)
- **Icons**: Font Awesome 6

### Machine Learning
- **scikit-learn**: Matrix factorization, similarity calculations
- **NumPy**: Numerical computations
- **Pandas**: Data manipulation
- **SciPy**: Scientific computing

### Development
- **Python 3.8+**
- **pip**: Package manager
- **virtualenv**: Environment management

---

## 📁 Project Structure

```
bookstore/
├── bookworld/                  # Django project settings
│   ├── settings.py            # Settings configuration
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py               
│   └── asgi.py               
│
├── apps/                      # Django applications
│   ├── accounts/              # User authentication & profiles
│   │   ├── models.py          # UserProfile, Address
│   │   ├── views.py           # Auth views
│   │   ├── urls.py
│   │   └── forms.py
│   │
│   ├── books/                 # Book management
│   │   ├── models.py          # Book, Category, Review
│   │   ├── views.py           # Book listing & details
│   │   ├── urls.py
│   │   └── management/
│   │       └── commands/
│   │           └── populate_books.py
│   │
│   ├── cart/                  # Shopping cart
│   │   ├── models.py          # Cart, CartItem
│   │   ├── views.py           # Cart operations
│   │   └── urls.py
│   │
│   ├── orders/                # Order management
│   │   ├── models.py          # Order, OrderItem, Payment
│   │   ├── views.py           # Checkout, order tracking
│   │   └── urls.py
│   │
│   ├── recommendations/       # AI recommendation engine
│   │   ├── models.py          # User ratings, recommendations
│   │   ├── engine.py          # Collaborative filtering
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── analytics/             # Admin analytics
│       ├── models.py          # Sales metrics
│       ├── views.py           # Analytics dashboard
│       └── urls.py
│
├── templates/                 # HTML templates
│   ├── base/
│   │   └── base.html         # Base template
│   ├── accounts/
│   ├── books/
│   ├── cart/
│   ├── orders/
│   └── admin_dashboard/
│
├── static/                    # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                     # User uploads
│   └── book_covers/
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── .gitignore
└── README.md
```

---

## 🗄️ Database Schema

### Key Models

**User (Django Built-in)**
- Contains: username, email, password, is_staff

**UserProfile** (extends User)
- Fields: phone, address, city, state, postal_code, profile_picture, bio, role

**Category**
- Fields: name, description

**Book**
- Fields: title, author, price, category, stock, cover_image, rating, discount_percentage

**BookReview**
- Fields: user, book, rating, title, review_text

**Cart & CartItem**
- Tracks: user shopping cart and items

**Order & OrderItem**
- Tracks: purchases, shipping, payment status

**UserRating** (for recommendations)
- Fields: user, book, rating, interaction_type, interaction_weight

**RecommendedBook**
- Stores: pre-computed recommendations for users

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone and Setup Python Environment

```bash
cd c:\Users\manik\OneDrive\Desktop\bookstore

# Activate virtual environment
.venv\Scripts\activate  # On Windows

# Or on macOS/Linux
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Database

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE bookworld_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4: Setup Environment Variables

```bash
# Copy .env.example to .env and fill in your values
copy .env.example .env

# Edit .env with your database credentials
# DB_NAME=bookworld_db
# DB_USER=root
# DB_PASSWORD=your_password
# DB_HOST=localhost
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Enter username, email, password
```

### Step 7: Populate Sample Data

```bash
python manage.py populate_books
```

---

## ▶️ Running the Project

### Start Development Server

```bash
python manage.py runserver
```

Access the application at: **http://localhost:8000**

### Admin Panel

Go to: **http://localhost:8000/admin**

Login with your superuser credentials

---

## 🤖 Recommendation System

### How It Works

The recommendation engine uses **Collaborative Filtering** with **Matrix Factorization (NMF)**:

1. **Build Rating Matrix**: Create a user-item matrix of interactions
2. **Matrix Factorization**: Decompose into user and item latent factors
3. **Prediction**: Calculate dot product of user-item factors
4. **Ranking**: Recommend top-rated books not Yet interacted with

### Training the Model

```bash
# Train recommendation model
python manage.py shell
>>> from apps.recommendations.engine import train_all_models
>>> train_all_models()
```

### Key Components

**UserRating Model**
- Tracks: views, wishlist additions, purchases, reviews
- Weight: Different interactions have different importance

**CollaborativeFilteringEngine**
- Parameters:
  - n_factors: Number of latent factors (default: 10)
  - n_epochs: Training iterations (default: 100)
  - learning_rate: Gradient step size (default: 0.01)
  - regularization: L2 penalty (default: 0.01)

### Integration with Views

```python
# In views, track interactions
from apps.recommendations.engine import generate_recommendations

# When user rates a book
UserRating.objects.create(
    user=user,
    book=book,
    rating=5,
    interaction_type='review'
)

# Generate fresh recommendations
generate_recommendations(user.id, n_recommendations=10)
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /accounts/register/           # User registration
POST   /accounts/login/              # User login
POST   /accounts/logout/             # User logout
```

### Books
```
GET    /books/                       # List all books
GET    /books/<id>/                  # Book details
GET    /books/category/<id>/         # Books by category
POST   /books/<id>/review/           # Add review
POST   /books/<id>/wishlist/         # Add to wishlist
```

### Cart
```
GET    /cart/                        # View cart
POST   /cart/add/<id>/               # Add to cart
POST   /cart/update/<item_id>/       # Update quantity
POST   /cart/remove/<item_id>/       # Remove item
GET    /cart/api/count/              # Cart count (API)
```

### Orders
```
POST   /orders/checkout/             # Create order
GET    /orders/list/                 # View orders
GET    /orders/<id>/                 # Order details
GET    /orders/<id>/receipt/         # View receipt
```

### Recommendations
```
GET    /recommendations/             # Get recommendations
POST   /recommendations/track/<book_id>/<type>/
```

### Admin Analytics
```
GET    /analytics/dashboard/         # Admin dashboard
GET    /analytics/sales/             # Sales analytics
GET    /analytics/users/             # User analytics
```

---

## 🧪 Testing

### Running Tests

```bash
python manage.py test
```

### Test Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Sample Data for Testing

```bash
python manage.py populate_books
```

### Create Test User

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
```

---

## 📊 Admin Features Walkthrough

### 1. Access Admin Dashboard
- URL: http://localhost:8000/admin
- Login with superuser credentials

### 2. Browse Models
- Users → Manage user profiles and roles
- Books → Add/edit books and categories
- Orders → Track orders and payments
- Analytics → View sales and user metrics

### 3. Manage Books
```bash
python manage.py shell
>>> from apps.books.models import Book, Category
>>> cat = Category.objects.create(name='Science')
>>> book = Book.objects.create(
...     title='Python Basics',
...     author='John Doe',
...     category=cat,
...     price=29.99,
...     isbn='123-456-789',
...     pages=300,
...     publication_date='2023-01-01',
...     publisher='Tech Books',
...     stock=50
... )
```

---

## 🔐 Security Features

- **Password Hashing**: Django's PBKDF2
- **CSRF Protection**: Enabled by default
- **SQL Injection**: Protected by ORM
- **XSS Protection**: Template auto-escaping
- **Session Security**: Secure cookies for production
- **Admin Security**: Django admin access control

### Production Security Checklist

```python
# In settings.py for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📱 Responsive Design

The application uses Bootstrap 5 for full responsiveness:
- Mobile-first design
- Tablet optimization
- Desktop experience
- Touch-friendly buttons

---

## 🚢 Deployment

### Using Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### Using AWS/DigitalOcean

1. **Setup Server**
   - Install Python, MySQL, nginx
   - Configure firewall

2. **Install Application**
   ```bash
   git clone <repo>
   cd bookstore
   pip install -r requirements.txt
   ```

3. **Configure Web Server**
   - Use gunicorn as WSGI server
   - Configure nginx as reverse proxy
   - Setup SSL with Let's Encrypt

4. **Run Application**
   ```bash
   gunicorn bookworld.wsgi -b 0.0.0.0:8000
   ```

---

## 📈 Performance Optimization

### Database Optimization
```python
# Use select_related for foreign keys
books = Book.objects.select_related('category')

# Use prefetch_related for reverse relations
orders = Order.objects.prefetch_related('items')

# Add database indexes in models
class Book(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]
```

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def book_list(request):
    ...
```

---

## 🐛 Troubleshooting

### Issue: Database Connection Error
```
Solution: Check MySQL is running
- Windows: Services → MySQL → Start
- macOS: brew services start mysql
- Linux: systemctl start mysql
```

### Issue: Port 8000 Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Issue: Missing Migrations
```bash
# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Write tests
4. Submit pull request

---

## 📝 License

This project is licensed under the MIT License

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@bookworld.com
- Documentation: See this README

---

## 👥 Team

**Project:** BookWorld - Online Book Store with AI Recommendation System
**Version:** 1.0
**Date:** 2024

---

## 📚 Additional Resources

### Django Documentation
- https://docs.djangoproject.com/

### Bootstrap Documentation
- https://getbootstrap.com/docs/

### Scikit-learn Documentation
- https://scikit-learn.org/

### MySQL Documentation
- https://dev.mysql.com/doc/

---

**Happy Reading! 📖**
