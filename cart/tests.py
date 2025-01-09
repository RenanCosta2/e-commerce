from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Carts, ItensCart
from .factory import ItemCartFactory
from products.models import Products
from products.factory import ProductFactory
from users.models import Users
from users.factory import UserFactory
from users.utils import Authentication


class ItemCartTestCase(TestCase):

    def setUp(self):
        """
        Set up the initial data for the tests.
        
        Creates a user, generates a token for authentication, and configures the client.
        Sets up a cart and two products for testing the cart item operations.
        """
        self.user1 = Users.objects.create(**UserFactory.create())  # Create a user
        self.token = Authentication.get_tokens_for_user(self.user1)  # Generate JWT token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Authenticate the client

        self.cart = Carts.objects.create(user=self.user1)  # Create a cart for the user

        # Create two products in the database
        self.product1 = Products.objects.create(**ProductFactory.create())
        self.product2 = Products.objects.create(**ProductFactory.create())

        # Create items for the cart with products and quantity
        self.item1 = ItensCart.objects.create(
            product=self.product1,
            cart=self.cart,
            quantity=4
        )
        self.item2 = ItensCart.objects.create(
            product=self.product1,
            cart=self.cart,
            quantity=2
        )

    def test_create_item_cart(self):
        """
        Test the creation of an item in the cart.
        
        Sends a POST request to create an item in the cart, checks if the response 
        status is HTTP 201 Created, and verifies if the item is stored in the database.
        """
        url = reverse('item-cart-list')
        data = ItemCartFactory.create(self.product1)  # Generate valid data for the item cart

        response = self.client.post(url, data)
        # Assert that the item was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ItensCart.objects.filter(product=self.product1).exists())

        # Attempt to create an item with a quantity that exceeds the stock
        quantity_exceeded = self.product2.storage + 1
        data = ItemCartFactory.create(self.product2, quantity_exceeded)

        response = self.client.post(url, data)
        # Assert that creating an item with excess quantity returns HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_item_cart(self):
        """
        Test listing items in the cart.
        
        Sends a GET request to retrieve the list of items in the cart and verifies 
        if the correct products are listed in the response.
        """
        url = reverse('item-cart-list')

        response = self.client.get(url)
        # Assert that the list of items is retrieved successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['product'], self.product1.id)

    def test_get_item_cart(self):
        """
        Test retrieving a specific item from the cart.
        
        Sends a GET request to retrieve an item by its ID and checks that the response 
        contains the correct item data with HTTP status 200.
        """
        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})

        response = self.client.get(url)
        # Assert that the item data matches and the status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product'], self.product1.id)

    def test_update_item_cart(self):
        """
        Test updating an item in the cart.
        
        Sends a PUT request to update an item’s information and checks if the update 
        is reflected in the database. Verifies the response status is HTTP 200 OK.
        """
        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})
        data = ItemCartFactory.create(self.product2, 10)

        response = self.client.put(url, data)
        # Assert that the item was updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ItensCart.objects.filter(product=self.product2.id, quantity=10).exists())

    def test_partial_update_item_cart(self):
        """
        Test partially updating an item in the cart.
        
        Sends a PATCH request to update only specific fields (e.g., quantity) and verifies 
        that the change is applied in the database.
        """
        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})
        data = {"quantity": 20}

        response = self.client.patch(url, data)
        # Assert that the quantity was updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ItensCart.objects.filter(product=self.product1.id, quantity=20).exists())

    def test_delete_item_cart(self):
        """
        Test deleting an item from the cart.
        
        Sends a DELETE request to remove an item from the cart and verifies that the item 
        is deleted successfully with HTTP 204 No Content status.
        """
        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})

        response = self.client.delete(url)
        # Assert that the item was deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reduce_quantity_item_cart(self):
        """
        Test reducing the quantity of an item in the cart.
        
        Sends a PATCH request to reduce the quantity of an item and verifies if the quantity 
        is reduced by one with each request until the item is deleted.
        """
        url = reverse('item-cart-reduce-quantity', kwargs={'pk': self.item1.id})

        response = self.client.patch(url)
        # Assert that the quantity was reduced successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ItensCart.objects.filter(id=self.item1.id, quantity=self.item1.quantity - 1).exists())

        # Continue reducing the quantity until it is removed
        for _ in range(self.item1.quantity - 1):
            response = self.client.patch(url)

        # Assert that the item was removed after reducing the quantity to zero
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ItensCart.objects.filter(id=self.item1.id).exists())

    def test_get_cart(self):
        """
        Test retrieving the cart’s total amount.
        
        Sends a GET request to retrieve the cart’s details and checks if the total 
        amount is calculated correctly, including the price of all items in the cart.
        """
        url = reverse('cart-detail', kwargs={'pk': self.cart.id})

        response = self.client.get(url)

        precision = Decimal('0.01')
        
        # Calculate the expected total amount for the cart
        total_amount = (self.item1.product.value * self.item1.quantity) +  (self.item2.product.value * self.item2.quantity)

        # Assert that the cart total matches the expected value
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total']).quantize(precision), Decimal(total_amount).quantize(precision))
