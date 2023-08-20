from django_filters.rest_framework import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'author_id': ['exact'],
            'genre_id': ['exact'],
            'publisher_id': ['exact'],
            'publish_date': [ 'gte', 'lte'],
            'price': ['gte', 'lte'],
        }