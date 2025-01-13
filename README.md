# E-commerce

The e-commerce system aims to provide a platform where users can browse products, add items to their cart, place orders, and register delivery addresses. It supports the management of products, shopping carts, orders, and addresses associated with users.

## 🚀 Features

- User Authentication
    - Secure login and registration process with JWT-based authentication.
    - Refresh token support for seamless session management.
    - Passwords securely stored using hashing algorithms.

- Product Management (CRUD)
    - Create, update, and delete products (administrator access only).
    - List products with advanced filtering options: by category, price range, or name.
    - Detailed product view for users.

- Shopping Cart
    - Add products to a cart with quantity validation based on stock availability.
    - Update or remove items from the cart.
    - View cart details, including subtotal per item and total value.

- Order Management
    - Create orders with associated items, total value, and selected delivery address.
    - Automatic stock adjustment upon order placement.
    - Administrators can manage order statuses: awaiting payment, payment approved, in preparation, shipped, delivered, or canceled.
    - Users can view their own orders, while administrators can access all orders.

- Address Management
    - Register and manage multiple delivery addresses.
    - Select a delivery address during checkout.

- Security and Validation
    - Ensure positive values for product prices and quantities.
    - Validate user input for product and order creation.
    - Restrict access to administrative features and sensitive routes to authorized users only.

- API and Documentation
    - Well-documented API with Swagger for easy integration and testing.
    - Organized endpoints for products, users, cart, orders, and addresses.

- Testing and Quality Assurance
  - Implement unit tests to validate individual components and functions.
  - Write integration tests to ensure the end-to-end functionality of key workflows.
  - Include tests for authentication, product management, cart operations, and order processing.
  - Ensure high code coverage to minimize bugs and maintain reliability.

## 🛠️ Technologies

- Python 3.12
- Django 5.1
- Django REST Framework
- JWT-based authentication

## 📋 Prerequisites

- Python 3.12
- pip
- virtualenv

## ⚙️ Installation

1. Clone the repository
```bash
git clone https://github.com/RenanCosta2/e-commerce.git
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env file with your configurations
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## 🏗️ Project Structure

```
e-commerce/
├── cart/
|   ├── admin.py
|   ├── apps.py
|   ├── factory.py
|   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
├── e_commerce/
|   ├── asgi.py
|   ├── settings.py
|   ├── urls.py
|   ├── wsgi.py
├── orders/
|   ├── admin.py
|   ├── apps.py
|   ├── factory.py
|   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
├── products/
|   ├── admin.py
|   ├── apps.py
|   ├── factory.py
|   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
├── users/
|   ├── services/
|   |   ├── address_service.py
|   |   ├── user_service.py
|   ├── tests/
|   |   ├── address_tests.py
|   |   ├── user_tests.py
|   ├── views/
|   |   ├── address_views.py
|   |   ├── user_views.py
|   ├── admin.py
|   ├── apps.py
|   ├── factory.py
|   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── utils.py
└── manage.py
```

## 📚 API Documentation

### Authentication

For this project, I'm using JWT (JSON Web Tokens) for authentication, a widely adopted method for handling user authentication in modern web applications.

- A user must first log in by providing their credentials (username and password).
- If the credentials are correct, the backend generates a JWT token.
- The token contains claims (such as user ID) and an expiration date.
- The token is then sent back to the client (usually in the response body or a header).
- For any API requests that require authentication, the client sends the JWT token in the Authorization header, like this:
```bash
    Authorization: Bearer <JWT_TOKEN>
```

You can find the interactive API documentation at:

[http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test app
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## 👥 Authors

- Renan Costa - Initial work - [RenanCosta2](https://github.com/RenanCosta2)
