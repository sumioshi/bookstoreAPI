from rest_framework.test import APITestCase
from product.models import Product, Category
from product.serializers import ProductSerializer

class ProductSerializerTest(APITestCase):
    def test_product_serialization(self):
        category = Category.objects.create(
            title='Fiction',
            slug='fiction',
            description='Fiction books',
            active=True
        )
        # Cria o produto sem associar a categoria inicialmente
        product = Product.objects.create(
            title='Test Book',
            description='Test Description',
            price=100,
            active=True
        )
        # Associa a categoria usando o método `set`
        product.category.set([category])
        product.save()

        serializer = ProductSerializer(product)
        data = serializer.data

        self.assertEqual(data['title'], 'Test Book')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['price'], 100)
        self.assertEqual(data['active'], True)
        self.assertEqual(len(data['category']), 1)
        self.assertEqual(data['category'][0]['title'], 'Fiction')
