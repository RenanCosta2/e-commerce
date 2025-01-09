from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from cart.models import Carts, ItensCart
from products.models import Products
from products.factory import ProductFactory
from users.models import Users, Address
from users.factory import UserFactory, AddressFactory
from users.utils import Authentication

class OrderTestCase(TestCase):
    """
    Test class for creating and managing user orders.
    Inherits from TestCase to run integration tests with the API.
    """

    def setUp(self):
        """
        Method executed before each test.
        
        Creates a user and generates a token for authentication. Also creates a cart, 
        products, cart items, and addresses associated with the user to test order-related operations.
        """
        self.user1 = Users.objects.create(**UserFactory.create())  # Create a user
        self.token = Authentication.get_tokens_for_user(self.user1)  # Generate JWT token
        self.client = APIClient()  # Create a test API client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Set authentication using the token

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

        self.address1 = Address.objects.create(**AddressFactory.create(self.user1), is_default=True)
        self.address2 = Address.objects.create(**AddressFactory.create(self.user1))

    def create_order(self):
        """
        Helper method to create an order for the user.
        
        Creates and returns the response from the API when creating an order with the default address.
        """
        url = reverse('order-list')
        data = {
            "address": self.address1.id
        }

        response = self.client.post(url, data)

        return response.data

    def test_create_order(self):
        """
        Test creating a new order.
        
        Verifies that the order is created successfully, the status is 201 (Created),
        and the correct product is added to the order.
        """
        url = reverse('order-list')
        data = {
            "address": self.address1.id
        }
        
        response = self.client.post(url, data)

        actual_storage = self.product1.storage

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Verify that the status is 201 Created
        self.assertEqual(response.data['data']['items'][0]['product'], self.product1.id)  # Verify the correct product

        # Check if the product's storage has been updated correctly after the order
        product = Products.objects.filter(id=self.product1.id).first()
        self.assertEqual(product.storage, actual_storage-self.item1.quantity) # Verify that the stock is reduced by the ordered quantity

    def test_list_order(self):
        """
        Test listing all orders.
        
        Verifies that the list of orders is returned and that the status is 200 (OK).
        The response should include the correct product in the first order.
        """
        self.create_order()

        url = reverse('order-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK
        self.assertEqual(response.data[0]['items'][0]['product'], self.product1.id)  # Verify the correct product in the list

    def test_get_order(self):
        """
        Test retrieving a specific order by its ID.
        
        Verifies that the order is returned correctly by its ID, and the status is 200 (OK).
        The response should include the correct product in the order.
        """
        order = self.create_order()

        url = reverse('order-detail', kwargs={'pk': order['data']['id']})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK
        self.assertEqual(response.data['items'][0]['product'], self.product1.id)  # Verify the correct product

    def test_update_order(self):
        """
        Test updating an order.
        
        Verifies that an update request returns a 403 Forbidden status when attempting 
        to change the order address.
        """
        order = self.create_order()

        url = reverse('order-detail', kwargs={'pk': order['data']['id']})

        data = {
            "address": self.address2.id
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Verify that the status is 403 Forbidden

    def test_partial_update_order(self):
        """
        Test partially updating an order.
        
        Verifies that a partial update request returns a 403 Forbidden status when attempting 
        to change the order address.
        """
        order = self.create_order()

        url = reverse('order-detail', kwargs={'pk': order['data']['id']})

        data = {
            "address": self.address2.id
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Verify that the status is 403 Forbidden

    def test_delete_order(self):
        """
        Test deleting an order.
        
        Verifies that a delete request returns a 403 Forbidden status when attempting 
        to delete the order.
        """
        order = self.create_order()

        url = reverse('order-detail', kwargs={'pk': order['data']['id']})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Verify that the status is 403 Forbidden
