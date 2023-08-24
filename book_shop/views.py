from rest_framework.viewsets import ModelViewSet
from .models import Product, Author, Genre, Publisher
from .permission import AdminPermissionOrReadOnly
from .serializers import ProductSerializer, AuthorSerializer, GenreSerializer, PublisherSerializer
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefualtPagination




class ProductViewSet(ModelViewSet):
    permission_classes = [AdminPermissionOrReadOnly]
    queryset=Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # pagination_class = DefualtPagination
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'publish_date', 'price']





class AuthorViewSet(ModelViewSet):
    permission_classes = [AdminPermissionOrReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['last_name']

    def destroy(self, request, *args, **kwargs):
        author=self.get_object()
        if author.product_set.count() > 0 :
            return Response({'error': 'instance cannot be deleted because it is associated with some products.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(AuthorViewSet, self).destroy(request, *args, **kwargs)


class GenreViewSet(ModelViewSet):
    permission_classes = [AdminPermissionOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        genre=self.get_object()
        if genre.product_set.count() > 0 :
            return Response({'error': 'instance cannot be deleted because it is associated with some products.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(GenreViewSet, self).destroy(request, *args, **kwargs)



class PublisherViewSet(ModelViewSet):
    permission_classes = [AdminPermissionOrReadOnly]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def destroy(self, request, *args, **kwargs):
        publisher = self.get_object()
        if publisher.product_set.count() > 0:
            return Response({'error': 'instance cannot be deleted because it is associated with some products.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(PublisherViewSet, self).destroy(request, *args, **kwargs)

