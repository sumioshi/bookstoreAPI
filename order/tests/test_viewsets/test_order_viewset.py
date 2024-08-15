import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from order.models import Order

class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product], user=self.user)

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = response.json()
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        product = ProductFactory()
        data = {
            "products_id": [product.id],
            "user": self.user.id
        }
        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=json.dumps(data),
            content_type="application/json",
        )
        print(response.content)  # Adicione esta linha para ver a resposta completa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
