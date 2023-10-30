from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_nested import routers


router=DefaultRouter()
router.register('products', ProductViewSet)
router.register('authors', AuthorViewSet)
router.register('genres', GenreViewSet)
router.register('publishers', PublisherViewSet)
router.register('carts', CartViewSet)
router.register('orders', OrderViewSet, basename='orders')
item_router=routers.NestedDefaultRouter(router, 'carts', lookup='cart')
item_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('',include(router.urls)),
    path('', include(item_router.urls)),

]