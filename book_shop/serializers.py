from rest_framework import serializers
from .models import Product, Author, Genre, Publisher



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'author', 'genre', 'publisher', 'publish_date', 'price', 'quantity', 'avatar']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'product_set']

    product_set = serializers.HyperlinkedRelatedField(many=True, view_name='product-detail', read_only=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title', 'description']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']

