# BookWorld - Technical Architecture & Design

## 🏢 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│                                                                   │
│    Browser                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  HTML/Bootstrap UI                                       │  │
│  │  ├─ Home Page                                            │  │
│  │  ├─ Book Browse & Search                                │  │
│  │  ├─ Cart & Checkout                                     │  │
│  │  ├─ User Account Management                             │  │
│  │  └─ Recommendations & Analytics                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│                                                                   │
│  Django Framework (4.2.13)                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ URL Router (urls.py)                                    │  │
│  │  ├─ /accounts/ → accounts app                           │  │
│  │  ├─ /books/ → books app                                │  │
│  │  ├─ /cart/ → cart app                                  │  │
│  │  ├─ /orders/ → orders app                              │  │
│  │  ├─ /recommendations/ → recommendations app             │  │
│  │  └─ /analytics/ → analytics app                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Views Layer (views.py)                                  │  │
│  │  ├─ accounts: login, register, profile                 │  │
│  │  ├─ books: list, search, detail, review               │  │
│  │  ├─ cart: add, remove, update items                    │  │
│  │  ├─ orders: checkout, confirmation, tracking          │  │
│  │  ├─ recommendations: personalized suggestions          │  │
│  │  └─ analytics: dashboard, reports                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Forms Layer (forms.py)                                  │  │
│  │  ├─ UserSignUpForm                                     │  │
│  │  ├─ BookSearchForm                                     │  │
│  │  ├─ CheckoutForm                                       │  │
│  │  └─ BookReviewForm                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Model Layer (models.py)                                 │  │
│  │  ├─ accounts.UserProfile, Address                      │  │
│  │  ├─ books.Book, Category, Review, WishList             │  │
│  │  ├─ cart.Cart, CartItem                                │  │
│  │  ├─ orders.Order, OrderItem, Payment, Receipt          │  │
│  │  ├─ recommendations.UserRating, RecommendedBook        │  │
│  │  └─ analytics.DailySalesMetric, CategoryAnalytics      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ SQL Queries via ORM
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│                                                                   │
│  MySQL (8.0+)                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Tables:                                                 │  │
│  │  ├─ auth_user (Django built-in)                        │  │
│  │  ├─ accounts_userprofile                               │  │
│  │  ├─ accounts_address                                   │  │
│  │  ├─ books_category                                     │  │
│  │  ├─ books_book                                         │  │
│  │  ├─ books_bookreview                                   │  │
│  │  ├─ books_wishlist                                     │  │
│  │  ├─ books_wishlist_books (M2M)                         │  │
│  │  ├─ cart_cart                                          │  │
│  │  ├─ cart_cartitem                                      │  │
│  │  ├─ orders_order                                       │  │
│  │  ├─ orders_orderitem                                   │  │
│  │  ├─ orders_payment                                     │  │
│  │  ├─ orders_receipt                                     │  │
│  │  ├─ recommendations_userrating                         │  │
│  │  ├─ recommendations_recommendedbook                    │  │
│  │  ├─ analytics_dailysalesmetric                         │  │
│  │  └─ analytics_categoryanalytics                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↑
                    ML/Analytics Layer
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML LAYER                                 │
│                                                                   │
│  Recommendation Engine (engine.py)                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Collaborative Filtering with NMF                        │  │
│  │  (Non-Negative Matrix Factorization)                    │  │
│  │                                                          │  │
│  │  1. Build Rating Matrix: User × Item                    │  │
│  │  2. Factorize: NMF decomposition                        │  │
│  │  3. Predict: User-Item similarity scores                │  │
│  │  4. Rank: Top-N recommendations                         │  │
│  │                                                          │  │
│  │  Libraries: scikit-learn, numpy, pandas                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Architecture

### User Registration & Authentication Flow

```
Browser                    Django App                Database
  │                           │                         │
  ├──Register Form────────────►│                         │
  │                           │                         │
  │  ◄─────Validation─────────┤                         │
  │                           │                         │
  ├──Submit Data─────────────►│                         │
  │                           │                         │
  │                           ├──Check Unique──────────►│
  │                           │◄─────Result────────────│
  │                           │                         │
  │                           ├──Hash Password         │
  │                           │                         │
  │                           ├──Create User──────────►│
  │                           │◄──User ID──────────────│
  │                           │                         │
  │                           ├──Create UserProfile───►│
  │                           │◄──Profile ID───────────│
  │                           │                         │
  │  ◄────Redirect to Login───┤                         │
```

### Shopping Flow

```
Customer                   App                     Database
   │                        │                         │
   ├─Browse /books/────────►│                         │
   │                        ├─Get Books──────────────►│
   │◄───List of Books────────┤◄──Book Data────────────│
   │                        │                         │
   ├─View Details──────────►│                         │
   │                        ├─Get Book & Reviews────►│
   │◄───Book Page───────────┤◄──Data─────────────────│
   │                        │                         │
   ├─Add to Cart──────────►│                         │
   │                        ├─Get/Create Cart────────►│
   │                        ├─Get Cart ID            │
   │                        ├─Add CartItem──────────►│
   │◄───Added Message────────┤◄──CartItem────────────│
   │                        │                         │
   ├─View Cart───────────►│                         │
   │                        ├─Get User's Cart───────►│
   │◄───Cart Items──────────┤◄──CartItems + Prices──│
   │                        │                         │
   ├─Checkout───────────►│                         │
   │                        ├─Create Order──────────►│
   │                        ├─Create OrderItems─────►│
   │                        ├─Create Payment────────►│
   │                        ├─Create Receipt────────►│
   │                        ├─Update Book Stock─────►│
   │                        ├─Clear Cart────────────►│
   │◄───Confirmation────────┤◄──Order Details───────│
```

### Recommendation Generation Flow

```
1. User Interactions Tracking
   ┌──────────────────────────────────┐
   │ Review book → UserRating created  │
   │ Purchase book → UserRating created│
   │ Add to wishlist → UserRating      │
   │ View book → UserRating            │
   └──────────────────────────────────┘
                    ↓
2. Matrix Construction
   ┌──────────────────────────────────┐
   │ Build User × Item matrix:         │
   │                                   │
   │     Book1 Book2 Book3 ... Book N │
   │ U1   5     0     3      ...  0   │
   │ U2   4     5     0      ...  2   │
   │ U3   0     3     0      ...  4   │
   │ ... (with weights)                │
   └──────────────────────────────────┘
                    ↓
3. Matrix Factorization (NMF)
   ┌──────────────────────────────────┐
   │ R ≈ W × H where:                  │
   │ - W: User Factor Matrix (n_factors) │
   │ - H: Item Factor Matrix            │
   │                                   │
   │ Optimization: minimize ||R - WH||²│
   │ + regularization terms            │
   └──────────────────────────────────┘
                    ↓
4. Prediction & Ranking
   ┌──────────────────────────────────┐
   │ For each user:                    │
   │   For each unrated item:          │
   │     predicted_rating =            │
   │       user_factors · item_factors │
   │                                   │
   │ Sort by predicted_rating DESC     │
   │ Return top-N recommendations      │
   └──────────────────────────────────┘
                    ↓
5. Store Results
   ┌──────────────────────────────────┐
   │ RecommendedBook.objects.create(   │
   │   user=user,                      │
   │   book=book,                      │
   │   recommendation_score=score      │
   │ )                                 │
   └──────────────────────────────────┘
                    ↓
6. Display to User
   ┌──────────────────────────────────┐
   │ /recommendations/                 │
   │ Shows top recommended books       │
   │ Sorted by score                   │
   └──────────────────────────────────┘
```

---

## 🗂️ Database Schema

### Core Tables & Relationships

```
auth_user (Django)
├─ id (PK)
├─ username (UNIQUE)
├─ email
├─ password (hashed)
├─ first_name
├─ last_name
├─ is_staff
├─ is_superuser
└─ date_joined

accounts_userprofile (1:1 with auth_user)
├─ id (PK)
├─ user_id (FK → auth_user)
├─ phone
├─ address
├─ city, state, postal_code, country
├─ profile_picture (image)
├─ bio
├─ role (customer/admin)
├─ preferred_genre
└─ date_of_birth

accounts_address (1:N with auth_user)
├─ id (PK)
├─ user_id (FK → auth_user)
├─ street_address
├─ city, state, postal_code, country
├─ is_default (boolean)
└─ created_at

books_category
├─ id (PK)
├─ name (UNIQUE)
├─ description

books_book
├─ id (PK)
├─ title
├─ author
├─ description (text)
├─ category_id (FK → books_category)
├─ price (decimal)
├─ stock (int)
├─ isbn (UNIQUE)
├─ publication_date
├─ publisher
├─ pages
├─ language
├─ cover_image (image field)
├─ average_rating (decimal)
├─ total_reviews (int)
├─ is_bestseller (boolean)
├─ discount_percentage
├─ created_at
└─ updated_at

books_bookreview
├─ id (PK)
├─ book_id (FK → books_book)
├─ user_id (FK → auth_user)
├─ rating (1-5)
├─ title
├─ review_text
├─ helpful_count
├─ created_at
├─ updated_at
└─ UNIQUE(book_id, user_id)

books_wishlist (1:1 with auth_user)
├─ id (PK)
├─ user_id (FK → auth_user, UNIQUE)
├─ books (M2M → books_book)
├─ created_at
└─ updated_at

cart_cart (1:1 with auth_user)
├─ id (PK)
├─ user_id (FK → auth_user, UNIQUE)
├─ created_at
└─ updated_at

cart_cartitem
├─ id (PK)
├─ cart_id (FK → cart_cart)
├─ book_id (FK → books_book)
├─ quantity (int)
├─ added_at
└─ UNIQUE(cart_id, book_id)

orders_order
├─ id (PK)
├─ order_id (UNIQUE, UUID format)
├─ user_id (FK → auth_user)
├─ shipping_address_id (FK → accounts_address)
├─ total_amount (decimal)
├─ discount_amount (decimal)
├─ tax_amount (decimal)
├─ final_amount (decimal)
├─ status (pending/confirmed/shipped/delivered/cancelled)
├─ payment_method
├─ payment_status (pending/completed/failed)
├─ notes
├─ created_at
├─ updated_at
└─ delivered_at

orders_orderitem
├─ id (PK)
├─ order_id (FK → orders_order)
├─ book_id (FK → books_book)
├─ quantity
├─ price_at_purchase (decimal)
└─ discount_percentage

orders_payment (1:1 with orders_order)
├─ id (PK)
├─ order_id (FK → orders_order)
├─ payment_method (credit_card/debit/upi/etc)
├─ amount (decimal)
├─ transaction_id (UNIQUE)
├─ status (success/failed/pending)
├─ payment_date
└─ notes

orders_receipt (1:1 with orders_order)
├─ id (PK)
├─ order_id (FK → orders_order)
├─ receipt_number (UNIQUE)
├─ subtotal (decimal)
├─ discount (decimal)
├─ tax (decimal)
├─ total (decimal)
└─ generated_at

recommendations_userrating
├─ id (PK)
├─ user_id (FK → auth_user)
├─ book_id (FK → books_book)
├─ rating (0-5)
├─ interaction_type (view/wishlist/purchase/review)
├─ interaction_weight (float)
├─ created_at
├─ updated_at
└─ UNIQUE(user_id, book_id, interaction_type)

recommendations_recommendedbook
├─ id (PK)
├─ user_id (FK → auth_user)
├─ book_id (FK → books_book)
├─ recommendation_score (float, 0-5)
├─ recommendation_type
├─ reason (text, optional)
├─ is_clicked (boolean)
├─ created_at
└─ UNIQUE(user_id, book_id)

analytics_dailysalesmetric
├─ id (PK)
├─ date (UNIQUE)
├─ total_revenue (decimal)
├─ total_orders (int)
├─ total_items_sold (int)
├─ unique_customers (int)
└─ average_order_value (decimal)

analytics_categoryanalytics
├─ id (PK)
├─ category_id (FK → books_category)
├─ total_sales (int)
├─ total_revenue (decimal)
├─ average_rating (decimal)
└─ last_updated
```

---

## 🔐 Security Architecture

### Authentication & Authorization

```
┌─────────────────────────────────┐
│    HTTP Request (no session)    │
└──────────────┬──────────────────┘
               ↓
        ┌──────────────┐
        │ Check if URL │
        │ requires auth│
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Has session? │
        └──┬───────┬───┘
           │       │
        YES│       │NO
           │       │
           │       └───► 404 Page or
           │            Redirect to Login
           │
           ▼
        ┌─────────────┐
        │ Check role: │
        │ - Customer  │
        │ - Admin     │
        └──────┬──────┘
               │
        ┌──────▼─────────┐
        │ Has permission?│
        └──┬──────────┬──┘
          YES        NO
           │          │
           │          └──► 403 Forbidden
           │
           ▼
        ┌──────────────┐
        │Execute View  │
        │Render HTML   │
        └──────────────┘
```

### Password Security

- **Hashing**: Django uses PBKDF2 by default
- **Salt**: Unique salt per password
- **Iterations**: 260000 iterations (configurable)
- **Algorithm**: SHA256

---

## 🔄 Request-Response Cycle

### Typical Web Request

```
1. Browser sends HTTP Request
   GET /books/?category=Fiction&sort_by=rating
   Headers: User-Agent, Cookie, Accept, etc.

2. Django URL Router matches pattern
   /books/ → books.views.book_list

3. Middleware processes request
   - Security checks
   - Session loading
   - CSRF verification

4. View executes
   a. Query database
      books = Book.objects.filter(category='Fiction')
      .order_by('-average_rating')
   
   b. Prepare context
      context = {'books': books, ...}
   
   c. Render template
      render(request, 'books/book_list.html', context)

5. Template rendering
   - Load base.html
   - Insert content blocks
   - Process template variables
   - Generate HTML string

6. Response object created
   - Content-Type: text/html; charset=utf-8
   - Status: 200 OK
   - Headers: Set-Cookie, CSRF token, etc.

7. Browser receives and renders HTML
   - Parse HTML
   - Load CSS styles
   - Load JavaScript
   - Load images
   - Display page
```

---

## 📈 Performance Optimization Strategies

```
┌─────────────────────────────┐
│   Database Optimization     │
├─────────────────────────────┤
│ ✓ Indexes on frequently     │
│   searched columns          │
│ ✓ select_related() for FK   │
│ ✓ prefetch_related() for M2M│
│ ✓ Query caching             │
│ ✓ Connection pooling        │
└─────────────────────────────┘

┌─────────────────────────────┐
│  Frontend Optimization      │
├─────────────────────────────┤
│ ✓ CSS minification          │
│ ✓ JavaScript minification   │
│ ✓ Image compression         │
│ ✓ CDN for static files      │
│ ✓ Browser caching           │
└─────────────────────────────┘

┌─────────────────────────────┐
│  Application Optimization   │
├─────────────────────────────┤
│ ✓ View caching (@cache)     │
│ ✓ Lazy loading              │
│ ✓ Pagination for large sets │
│ ✓ Async tasks (Celery)      │
│ ✓ Connection pooling        │
└─────────────────────────────┘
```

---

## 🚀 Deployment Architecture

### Production Stack

```
┌──────────┐
│ Browser  │
└────┬─────┘
     │ HTTPS:443
     ▼
┌──────────────┐
│ CloudFront   │ (CDN for static files)
│ or similar   │
└────┬─────────┘
     │
     ▼
┌────────────────────┐
│ Load Balancer      │ (Optional, for scaling)
└────┬───────────────┘
     │
     ▼
┌────────────────────────────┐
│ Web Server (Gunicorn)      │
│ + Nginx (Reverse Proxy)    │
└────┬───────────────────────┘
     │
     ▼
┌────────────────────────────┐
│ Django Application         │
│ (Deployed on EC2/Heroku)   │
└────┬───────────────────────┘
     │
     ▼
┌────────────────────────────┐
│ MySQL Database             │
│ (RDS or self-managed)      │
└────────────────────────────┘
     │
     ▼
┌────────────────────────────┐
│ S3 or File Storage         │
│ (Media files, backups)     │
└────────────────────────────┘
```

---

## 📋 API Design Pattern (REST-style)

```
Books Endpoints:
  GET    /books/              → List all books
  GET    /books/<id>/         → Get single book
  POST   /books/<id>/review/  → Add review
  POST   /books/<id>/wishlist/ → Toggle wishlist

Cart Endpoints:
  GET    /cart/               → View cart
  POST   /cart/add/<book_id>/ → Add to cart
  POST   /cart/update/<id>/   → Update quantity
  POST   /cart/remove/<id>/   → Remove item
  GET    /cart/api/count/     → Get count (JSON)

Orders Endpoints:
  POST   /orders/checkout/    → Create order
  GET    /orders/list/        → List orders
  GET    /orders/<id>/        → Get order
  GET    /orders/<id>/receipt/→ Get receipt

Recommendations:
  GET    /recommendations/    → Get recommendations
  POST   /recommendations/track/...  → Track interaction
```

---

## 🎯 Design Patterns Used

1. **MVC Pattern**: Models, Views, Templates
2. **Factory Pattern**: `get_or_create_cart()`
3. **Middleware Pattern**: Django middleware stack
4. **Decorator Pattern**: `@login_required`, `@cache_page`
5. **Template Inheritance**: Base template with blocks
6. **DRY (Don't Repeat Yourself)**: Reusable components
7. **Observer Pattern**: Signals for validation

---

## 🔄 Business Logic Flow

### Order Processing Workflow

```
START
  │
  ├─ Get User's Cart
  ├─ Validate Cart Not Empty
  ├─ Get Checkout Form
  ├─ Validate Address
  ├─ Validate Payment Method
  │
  ├─ TRANSACTION START
  │  ├─ Create Order
  │  ├─ Create OrderItems (from CartItems)
  │  ├─ Create Payment Record
  │  ├─ Create Receipt
  │  ├─ Update Book Stock
  │  ├─ Clear User's Cart
  │  └─ COMMIT ALL OR ROLLBACK
  │
  ├─ SEND CONFIRMATION EMAIL (async)
  ├─ GENERATE ANALYTICS UPDATE
  ├─ TRIGGER RECOMMENDATION REFRESH
  │
  └─ RETURN Confirmation Page
END
```

---

## 📊 Recommendation Algorithm Details

### Matrix Factorization (NMF)

**Problem**: Predict missing ratings in sparse user-item matrix

**Solution**: Decompose R into two lower-rank matrices:
```
R (m × n) ≈ W (m × k) × H^T (k × n)

Where:
- m = number of users
- n = number of items
- k = number of latent factors (e.g., 10)
- W = user factor matrix
- H = item factor matrix
```

**Algorithm**:
```
1. Initialize W and H randomly
2. For each epoch (iteration):
   a. For each user-item pair (i, j):
      - Calculate: r_ij = W[i] · H[j]
      - Error: e_ij = actual_rating - r_ij
      - Update W[i] += learning_rate * e_ij * H[j]
      - Update H[j] += learning_rate * e_ij * W[i]
   b. Add regularization penalty
3. Repeat for n_epochs
4. Use trained W & H for predictions
```

**Prediction**:
```
For user u and item i:
predicted_rating = W[u] · H[i]
Clamp to [0, 5]
```

**Key Parameters**:
- `n_factors`: Number of latent factors (default: 10)
- `n_epochs`: Training iterations (default: 100)
- `learning_rate`: Optimization step size (default: 0.01)
- `regularization`: L2 penalty (default: 0.01)

**Interaction Weighting**:
```
- View: 0.5x
- Wishlist: 1.5x
- Purchase: 3.0x
- Review: 2.5x

weighted_rating = rating * weight_multiplier
```

---

This architecture ensures:
✓ Scalability
✓ Security
✓ Maintainability
✓ Performance
✓ User Experience

---

**End of Technical Architecture Document**
