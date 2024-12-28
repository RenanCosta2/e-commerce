from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Carts, ItensCart
from products.models import Products
from users.models import Users
from django.contrib.auth import get_user_model

class ItemCartTesteCase(TestCase):

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

        self.cart = Carts.objects.create(user=self.user1)
        
        url = reverse('token_obtain_pair')
        data = {"username": "lucaspaulo", "password": "Senha@789"}
        response = self.client.post(url, data)
        self.token = response.data['access']

        self.client = APIClient()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.product1 = Products.objects.create(
            id=1,
            name="Smartphone XYZ 5G",
            category="Electronics",
            description="Smartphone com 5G e câmera de 64MP.",
            value=99.99,
            storage=50
        )

        self.product2 = Products.objects.create(
            id=2,
            name="Camiseta Masculina Slim Fit",
            category="Clothing",
            description="Camiseta slim fit em algodão.",
            value=49.99,
            storage=100
        )

        self.item1 = ItensCart.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=4
        )

        self.item2 = ItensCart.objects.create(
            cart=self.cart,
            product=self.product2,
            quantity=1
        )

    def test_create_item_cart(self):
        """
        Test creation of an item cart
        """
        
        url = reverse('item-cart-list')
        data = {
            "product": self.product2.id,
            "quantity": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ItensCart.objects.filter(product=self.product2).exists())
        
    def test_list_item_cart(self):
        """
        Test listing of items cart
        """

        url = reverse('item-cart-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['product'], self.product1.id)
        
    def test_get_item_cart(self):
        """
        Test retrieving an item cart
        """

        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product'], self.product1.id)
        
    def test_update_item_cart(self):
        """
        Test update of an item cart
        """

        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})
        data = {
                "product": 2,
                "quantity": 10
            }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ItensCart.objects.filter(product=self.product2.id, quantity=10).exists())
        
    def test_partial_update_item_cart(self):
        """
        Test partial update of an item cart
        """

        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})
        data = {
                "quantity": 20
            }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ItensCart.objects.filter(product=self.product1.id, quantity=20).exists())

    def test_delete_item_cart(self):
        """
        Test item cart deletion
        """

        url = reverse('item-cart-detail', kwargs={'pk': self.item1.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reduce_quantity_item_cart(self):
        """
        Test reduce quantity of an item cart
        """

        url = reverse('item-cart-reduce-quantity', kwargs={'pk': self.item1.id})
        
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ItensCart.objects.filter(id=self.item1.id, quantity=3).exists())

        for _ in range(3):
            response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ItensCart.objects.filter(id=self.item1.id).exists())

    def test_get_cart(self):
        """
        Test retrieving an item cart
        """

        url = reverse('cart-detail', kwargs={'pk': self.cart.id})

        response = self.client.get(url)

        precision = Decimal('0.01')
        
        total_amount = (self.item1.product.value * self.item1.quantity) +  (self.item2.product.value * self.item2.quantity)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total']).quantize(precision), Decimal(total_amount).quantize(precision))