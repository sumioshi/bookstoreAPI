from product.serializers.product_serializer import ProductSerializer
from rest_framework import serializers
from order.models import Order
from product.models import Product


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ['product', 'total', 'user', 'products_id']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        product_data = validated_data.pop('products_id')
        user_data = validated_data.pop('user')

        order = Order.objects.create(user=user_data)
        for product in product_data:
            order.product.add(product)
        return order

    def update(self, instance, validated_data):
        product_data = validated_data.pop('products_id', None)

        if product_data:
            instance.product.clear()
            for product in product_data:
                instance.product.add(product)

        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
