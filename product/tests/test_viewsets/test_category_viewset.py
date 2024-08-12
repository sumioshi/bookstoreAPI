import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='books')

    def test_get_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)
        self.assertEqual(category_data[0]['title'], self.category.title)

    def test_create_category(self):
        data = json.dumps({
            'title': 'technology',
        })
        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_category = Category.objects.get(title='technology')
        self.assertEqual(created_category.title, 'technology')

    def test_update_category(self):
        data = {'title': 'new books'}
        response = self.client.put(
            reverse('category-detail', kwargs={'version': 'v1', 'pk': self.category.pk}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title, 'new books')

    def test_delete_category(self):
        response = self.client.delete(
            reverse('category-detail', kwargs={'version': 'v1', 'pk': self.category.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
