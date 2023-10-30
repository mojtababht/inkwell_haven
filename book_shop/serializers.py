from rest_framework import serializers
from .models import Product, Author, Genre, Publisher, Cart, CartItem, Order, OrderItem
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'author', 'genre', 'publisher', 'publish_date', 'price', 'quantity', 'avatar']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'product_set']




class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title', 'description']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'avatar']
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']



class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('No product whit given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
            return self.instance
        except CartItem.DoesNotExist:
            return super(AddCartItemSerializer, self).save(cart_id=cart_id)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()
    def save(self, **kwargs):
        with transaction.atomic():
            cart_items = CartItem.objects.select_related('product').filter(cart_id=self.validated_data['cart_id'])
            order=Order.objects.create(customer_id=self.context['user_id'])
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=self.validated_data['cart_id']).delete()
            return order

    def validate_cart_id(self, value):
        if not Cart.objects.filter(id=value).exists():
            raise serializers.ValidationError('No cart whit given ID was found.')
        if CartItem.objects.filter(cart_id=value).count() == 0:
            raise serializers.ValidationError('The cart is empty.')

        return value

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']



