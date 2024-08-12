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

        # Verificações (Asserts)
        self.assertEqual(data['title'], 'Test Book')  # Testa o campo 'title' de Product
        self.assertEqual(data['description'], 'Test Description')  # Testa o campo 'description' de Product
        self.assertEqual(data['price'], 100)  # Testa o campo 'price' de Product
        self.assertEqual(data['active'], True)  # Testa o campo 'active' de Product
        self.assertEqual(len(data['category']), 1)  # Testa a relação 'category' (ManyToMany) do Product
        self.assertEqual(data['category'][0]['title'], 'Fiction')  # Testa o campo 'title' da Category associada
