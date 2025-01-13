from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import Users, Address
from users.factory import UserFactory, AddressFactory
from users.utils import Authentication

class AddressTestCase(TestCase):
    """
    Test class for creating and managing user addresses.
    Inherits from TestCase to run integration tests with the API.
    """

    def setUp(self):
        """
        Method executed before each test.
        
        Creates a user and generates a token for authentication. Also creates two 
        addresses associated with this user to test address-related operations.
        """
        self.user1 = Users.objects.create(**UserFactory.create())  # Create a user
        self.token = Authentication.get_tokens_for_user(self.user1)  # Generate an authentication token
        self.client = APIClient()  # Create a test API client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # Set authentication using the token

        # Create two addresses for the user
        self.address1 = Address.objects.create(**AddressFactory.create(self.user1), is_default=True)
        self.address2 = Address.objects.create(**AddressFactory.create(self.user1))

    def test_create_address(self):
        """
        Test creating a new address.
        
        Verifies that the address is created correctly and that the returned status is 201 (Created).
        """
        url = reverse('address-list')

        # Verify if the default address is already present before creating a new one
        self.assertTrue(Address.objects.filter(street=self.address1.street, is_default=True).exists())
        
        data = AddressFactory.create(self.user1)
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Verify that the status is 201 Created
        
        # Verify that the new address is saved in the database
        self.assertTrue(Address.objects.filter(street=data['street'], is_default=False).exists())

    def test_list_address(self):
        """
        Test listing user addresses.
        
        Verifies if the response contains the user's addresses and the status is 200 (OK).
        """
        url = reverse('address-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK
        self.assertEqual(response.data[0]['street'], self.address1.street)  # Verify if the first returned address is correct

    def test_get_address(self):
        """
        Test retrieving a specific address.
        
        Verifies that the address is returned correctly by its ID.
        """
        url = reverse('address-detail', kwargs={'pk': self.address1.id})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK
        self.assertEqual(response.data['street'], self.address1.street)  # Verify if the address street is correct

    def test_update_address(self):
        """
        Test updating an address.
        
        Verifies that the address is updated and the status is 200 (OK).
        """
        url = reverse('address-detail', kwargs={'pk': self.address1.id})
        data = {
                "street": "Rua do Comércio",
                "city": "Belo Horizonte",
                "state": "MG",
                "zip_code": "54321-876"
            }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK
        self.assertTrue(Address.objects.filter(street="Rua do Comércio").exists())  # Verify that the updated address is saved in the database

    def test_partial_update_address(self):
        """
        Test partially updating an address.
        
        Verifies that only a specific field (street) is updated and the change is applied.
        """
        url = reverse('address-detail', kwargs={'pk': self.address1.id})
        data = {
                "street": "Rua do Comércio"
            }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK
        self.assertTrue(Address.objects.filter(street="Rua do Comércio").exists())  # Verify that the street is updated in the database

    def test_delete_address(self):
        """
        Test deleting an address.
        
        Verifies that the address is deleted and the status is 204 (No Content).
        """
        url = reverse('address-detail', kwargs={'pk': self.address1.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Verify that the status is 204 No Content

    def test_set_as_default_address(self):
        """
        Test setting an address as the default address.
        
        Verifies that the default address is updated and the correct address is set as default.
        """
        url = reverse('address-set-as-default', kwargs={'pk': self.address2.id})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Verify that the status is 200 OK

        addresses = Address.objects.filter(user=self.user1)
        self.assertFalse(addresses[0].is_default)  # Verify that the first address is no longer the default
        self.assertTrue(addresses[1].is_default)  # Verify that the second address is set as the default
