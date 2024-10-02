from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item
from django.contrib.auth import get_user_model

class ItemAPITests(APITestCase):
    
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']  # Adjust based on your token response format

        # Set the token in the authorization header for future requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.item_url = reverse('item-create')  # Adjust the name based on your URLs


    def test_create_item(self):
        data = {
            "name": "Test Item",
            "description": "A test item description.",
            "quantity": 10,
            "price": 99.99
        }
        response = self.client.post(self.item_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)

    def test_read_item(self):
        item = Item.objects.create(
            name="Test Item",
            description="A test item description.",
            quantity=10,
            price=99.99
        )
        response = self.client.get(reverse('item-detail', kwargs={'item_id': item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item.name)

    def test_update_item(self):
        item = Item.objects.create(
            name="Test Item",
            description="A test item description.",
            quantity=10,
            price=99.99
        )
        data = {
            "name": "Updated Item",
            "description": "An updated description.",
            "quantity": 5,
            "price": 49.99
        }
        response = self.client.put(reverse('item-detail', kwargs={'item_id': item.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, "Updated Item")

    def test_delete_item(self):
        item = Item.objects.create(
            name="Test Item",
            description="A test item description.",
            quantity=10,
            price=99.99
        )
        response = self.client.delete(reverse('item-detail', kwargs={'item_id': item.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
