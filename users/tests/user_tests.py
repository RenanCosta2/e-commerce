from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import Users
from users.factory import UserFactory
from users.utils import Authentication

class UserTestCase(TestCase):
    """
    Test class for creating, managing, and deleting users.
    Inherits from TestCase to run integration tests with the API.
    
    This class tests various API endpoints related to user management,
    including creating, listing, retrieving, updating, partially updating,
    and deleting users. It also tests the behavior of the system for 
    different user roles (admin and non-admin).
    """

    def setUp(self):
        """
        Sets up initial data for the tests.
        
        Creates a user and generates a token for authentication. 
        Configures the client to use the generated token for authentication.
        """
        self.user1 = Users.objects.create(**UserFactory.create())
        self.token = Authentication.get_tokens_for_user(self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_user(self):
        """
        Test creating a new user.
        
        Sends a POST request to create a user, checks if the response status is 
        HTTP 201 Created and if the user is saved in the database.
        """
        url = reverse('user-list')
        data = UserFactory.create()
        
        response = self.client.post(url, data)
        
        # Assert that the user is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(username=data['username']).exists())

    def test_list_user(self):
        """
        Test listing users.
        
        Verifies the behavior when trying to list users with different roles. 
        A non-admin user should receive a 403 Forbidden status, while an 
        admin user should be able to access the list of users.
        """
        url = reverse('user-list')

        # Try to access the user list with a non-admin user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Create a superuser and get a token for them
        superuser = Users.objects.create(**UserFactory.create(True))
        self.token = Authentication.get_tokens_for_user(superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Try to access the user list with an admin user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], self.user1.username)

    def test_get_user(self):
        """
        Test retrieving a specific user.
        
        Sends a GET request to retrieve a user by ID and checks that the response 
        contains the correct user data with HTTP status 200.
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.get(url)
        
        # Assert that the user data matches and the status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)

    def test_update_user(self):
        """
        Test updating a user's information.
        
        Sends a PUT request to update a user's details and checks if the update 
        is reflected in the database. Verifies that the response status is 200.
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = UserFactory.create()

        response = self.client.put(url, data)
        
        # Assert that the user information is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Users.objects.filter(username=data['username']).exists())

    def test_partial_update_user(self):
        """
        Test partially updating a user's information.
        
        Sends a PATCH request to update only a specific field (username in this case)
        and verifies that the change is applied in the database.
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {"username": "lucasp"}
        
        response = self.client.patch(url, data)
        
        # Assert that the username is updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Users.objects.filter(username="lucasp").exists())

    def test_delete_user(self):
        """
        Test deleting a user.
        
        Sends a DELETE request to remove a user and verifies that the user is deleted 
        with an HTTP 204 No Content status.
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.delete(url)
        
        # Assert that the user is deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
