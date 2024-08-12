import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order

class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(reverse('order-list', kwargs={'version': 'v1'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['product'][0]['category'][0]['title'], self.category.title)

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({
            'products_id': [product.id],
            'user': user.id
        })
        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
        self.assertIsNotNone(created_order)

    def test_update_order(self):
        # Cria um novo produto e atualiza a ordem existente
        new_product = ProductFactory(title='keyboard', price=150)
        print("Before update:", [p.id for p in self.order.product.all()])

        data = {
            'products_id': [new_product.id],
            'user': self.order.user.id
        }
        response = self.client.put(
            reverse('order-detail', kwargs={'version': 'v1', 'pk': self.order.pk}),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order.refresh_from_db()
        print("After update:", [p.id for p in self.order.product.all()])
        self.assertEqual(self.order.product.first().id, new_product.id)

    def test_delete_order(self):
        order = OrderFactory()
        response = self.client.delete(
            reverse('order-detail', kwargs={'version': 'v1', 'pk': order.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())
