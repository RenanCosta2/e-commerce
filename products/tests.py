from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Products
from django.contrib.auth import get_user_model

class ProductsTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="testuser",
            password="password123"
        )
        
        url = reverse('token_obtain_pair')
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        self.token = response.data['access']

        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        url = reverse('product-list')
        self.product1 = Products.objects.create(
            name="Smartphone XYZ 5G",
            category="Electronics",
            description="Smartphone com 5G e câmera de 64MP.",
            value=99.99,
            storage=50
        )

        self.product2 = Products.objects.create(
            name="Camiseta Masculina Slim Fit",
            category="Clothing",
            description="Camiseta slim fit em algodão.",
            value=49.99,
            storage=100
        )

    def test_create_product(self):
        """
        Test creation of a product
        """
        
        url = reverse('product-list')
        data = {
            "name": "Laptop ABC",
            "category": "Computers",
            "description": "A lightweight and powerful laptop with a 15.6-inch display, Intel i7 processor, and 16GB of RAM.",
            "value": 1299.99,
            "storage": 30
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Products.objects.filter(name="Laptop ABC",category="Computers").exists())

    def test_list_product(self):
        """
        Test listing of products
        """

        url = reverse('product-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.product1.name)

    def test_get_product(self):
        """
        Test retrieving a product
        """

        url = reverse('product-detail', kwargs={'pk': self.product1.id})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_update_product(self):
        """
        Test update of a product
        """

        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        data = {
            "name": "Laptop ABC",
            "category": "Computers",
            "description": "A lightweight and powerful laptop with a 15.6-inch display, Intel i7 processor, and 16GB of RAM.",
            "value": 1299.99,
            "storage": 30
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Products.objects.filter(name="Laptop ABC",category="Computers").exists())

    def test_partial_update_product(self):
        """
        Test partial update of a product
        """

        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        data = {
            "name": "Laptop ABC",
            "category": "Computers"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Products.objects.filter(name="Laptop ABC",category="Computers").exists())

    def test_delete_product(self):
        """
        Test product deletion
        """

        url = reverse('product-detail', kwargs={'pk': self.product1.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_browse_products_by_category(self):
        """
        Test product browsing by category
        """

        url = reverse('product-browse-products-by-category')

        data = {
            "category": "Electronics"
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data:
            self.assertEqual(product['category'], data['category'])

        # Test bad request error when category parameter is missing
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test not found error when no product was found
        data = {
            "category": "not found category"
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_browse_products_by_value(self):
        """
        Test product browsing by values
        """

        url = reverse('product-browse-products-by-value')

        # Browsing products between two values
        data = {
            "min_price": 40.00,
            "max_price": 100.00
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

        # Browsing products with only min price
        data = {
            "min_price": 40.00
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

        # Browsing products with only max price
        data = {
            "max_price": 100.00
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

        # Test bad request error when min price is higher than max price
        data = {
            "min_price": 200.00,
            "max_price": 100.00
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

        # Test bad request error when min_price and max_price parameter is missing
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test not found error when no product was found
        data = {
            "min_price": 200.00,
            "max_price": 300.00
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_browse_products_by_name(self):
        """
        Test product browsing by name
        """

        url = reverse('product-browse-products-by-name')

        data = {
            "name": "smartphone"
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

        # Test bad request error when name parameter is missing
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test not found error when no product was found
        data = {
            "name": "not a name"
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)