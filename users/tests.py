from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Users
from django.contrib.auth import get_user_model

class UsersTestCase(TestCase):

    def setUp(self):
        self.user1 = Users.objects.create(
            username="lucaspaulo",
            first_name="Lucas",
            last_name="Paulo",
            cpf="112.233.445-66",
            email="lucas.paulo@example.com",
            password="Senha@789",
            is_staff=False,
            is_superuser=False
        )

        self.user1.set_password("Senha@789")
        self.user1.save()

        self.user2 = Users.objects.create(
            username="mariasilva",
            first_name="Maria",
            last_name="Silva",
            cpf="987.654.321-00",
            email="maria.silva@example.com",
            password="Senha@123"
        )

        self.user2.set_password("Senha@123")
        self.user2.save()

        url = reverse('token_obtain_pair')
        data = {"username": "lucaspaulo", "password": "Senha@789"}
        response = self.client.post(url, data)
        self.token = response.data['access']

        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_user(self):
        """
        Test creation of a user
        """

        url = reverse('user-list')
        data = {
                "username": "joaosilva",
                "first_name": "João",
                "last_name": "Silva",
                "cpf": "435.435.432-00",
                "email": "joao.silva@example.com",
                "password": "Aleatoria@456"
            }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(username="joaosilva").exists())

    def test_list_user(self):
        """
        Test listing of users
        """

        url = reverse('user-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_user_by_superuser(self):
        """
        Test listing of users
        """

        superuser = get_user_model().objects.create_superuser(
            username="testuser",
            password="password123"
        )
    
        url = reverse('token_obtain_pair')
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        self.token = response.data['access']

        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        url = reverse('user-list')

        response = self.client.get(url)

        url = reverse('user-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], self.user1.username)

    def test_get_user(self):
        """
        Test retrieving a user
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.id})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)

    def test_update_user(self):
        """
        Test update of a user
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {
            "username": "lucasp",
            "first_name": "Lucas",
            "last_name": "Paulo",
            "cpf": "112.233.445-66",
            "email": "lucas.paulo@example.com",
            "password": "Senha@789",
            "is_staff": True,
            "is_superuser": True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Users.objects.filter(username="lucasp").exists())

    def test_partial_update_user(self):
        """
        Test partial update of a user
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {
            "username": "lucasp"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Users.objects.filter(username="lucasp").exists())

    def test_delete_user(self):
        """
        Test user deletion
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)