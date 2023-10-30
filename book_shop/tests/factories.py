import factory
from book_shop.models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    name = 'test_product'
    class Meta:
        model = Product