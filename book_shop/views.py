from .models import Product, Author, Genre, Publisher, Cart, CartItem, Order
from .permission import AdminPermissionOrReadOnly
from .serializers import ProductSerializer, AuthorSerializer, GenreSerializer, PublisherSerializer, \
    CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer,\
    CreateOrderSerializer, UpdateOrderSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
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


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items', 'items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method =='POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        if self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(customer=self.request.user)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}



