from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Products
from .factory import ProductFactory
from users.models import Users
from users.factory import UserFactory
from users.utils import Authentication

class ProductsTestCase(TestCase):
    """
    Test class for creating, managing, and browsing products.
    Inherits from TestCase to run integration tests with the API.

    This class tests various API endpoints related to product management,
    including creating, listing, retrieving, updating, partially updating,
    and deleting products. It also tests filtering products by category,
    value, and name.
    """

    def setUp(self):
        """
        Sets up initial data for the tests.
        
        Creates a superuser and generates a token for authentication.
        Configures the client to use the generated token for authentication.
        Creates two products for testing.
        """
        self.user = Users.objects.create(**UserFactory.create(True))
        self.token = Authentication.get_tokens_for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.product1 = Products.objects.create(**ProductFactory.create())
        self.product2 = Products.objects.create(**ProductFactory.create())

    def test_create_product(self):
        """
        Test creating a new product.
        
        Sends a POST request to create a product and verifies that the response 
        status is HTTP 201 Created. Checks if the product is saved in the database.
        """
        url = reverse('product-list')
        data = ProductFactory.create()

        response = self.client.post(url, data)
        
        # Assert that the product is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Products.objects.filter(name=data['name'], category=data['category']).exists())

    def test_list_product(self):
        """
        Test listing all products.
        
        Sends a GET request to retrieve the list of products and verifies that
        the response status is HTTP 200 OK. Checks if the first product in the
        response matches the expected product.
        """
        url = reverse('product-list')
        response = self.client.get(url)
        
        # Assert that the product list is retrieved successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.product1.name)

    def test_get_product(self):
        """
        Test retrieving a specific product.
        
        Sends a GET request to retrieve a product by ID and verifies that the response 
        contains the correct product data with HTTP status 200.
        """
        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        response = self.client.get(url)
        
        # Assert that the product data matches and the status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_update_product(self):
        """
        Test updating a product's information.
        
        Sends a PUT request to update a product's details and verifies that the update 
        is reflected in the database. Verifies that the response status is 200.
        """
        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        data = ProductFactory.create()

        response = self.client.put(url, data)
        
        # Assert that the product information is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Products.objects.filter(name=data['name'], category=data['category']).exists())

    def test_partial_update_product(self):
        """
        Test partially updating a product's information.
        
        Sends a PATCH request to update specific fields of a product and verifies 
        that the change is applied in the database.
        """
        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        data = {"name": "Laptop ABC", "category": "Computers"}
        
        response = self.client.patch(url, data)
        
        # Assert that the product is updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Products.objects.filter(name=data['name'], category=data['category']).exists())

    def test_delete_product(self):
        """
        Test deleting a product.
        
        Sends a DELETE request to remove a product and verifies that the product is 
        deleted with an HTTP 204 No Content status.
        """
        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        response = self.client.delete(url)
        
        # Assert that the product is deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_browse_products_by_category(self):
        """
        Test browsing products by category.
        
        Sends a GET request to filter products by category and verifies that all 
        products in the response belong to the specified category. Also tests
        error handling for missing or invalid category parameters.
        """
        url = reverse('product-browse-products-by-category')
        data = {"category": self.product1.category}
        response = self.client.get(url, data)
        
        # Assert that products are filtered correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data:
            self.assertEqual(product['category'], data['category'])

        # Test error handling
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"category": "invalid_category"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_browse_products_by_value(self):
        """
        Test browsing products by price range.
        
        Sends a GET request to filter products based on min and max prices and verifies 
        the response. Also tests error handling for invalid price ranges and missing parameters.
        """
        url = reverse('product-browse-products-by-value')

        data = {"min_price": 0.00, "max_price": self.product1.value}
        response = self.client.get(url, data)
        
        # Assert that products are filtered correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

        data = {"min_price": 200.00, "max_price": 100.00}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_browse_products_by_name(self):
        """
        Test browsing products by name.
        
        Sends a GET request to filter products by name and verifies the response. 
        Also tests error handling for missing or invalid name parameters.
        """
        url = reverse('product-browse-products-by-name')

        data = {"name": self.product1.name}
        response = self.client.get(url, data)
        
        # Assert that products are filtered correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"name": "invalid_name"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
