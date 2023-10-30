from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)
    author=models.ForeignKey('Author', on_delete=models.PROTECT)
    genre=models.ForeignKey('Genre', on_delete=models.PROTECT)
    publisher=models.ForeignKey('Publisher', on_delete=models.PROTECT)
    publish_date=models.DateField()
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField(default=0)
    avatar=models.ImageField()

    def __str__(self):
        return self.name




class Author(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Publisher(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4)
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return str(self.product)
    class Meta:
        unique_together = [['cart', 'product']]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]


    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey('profiles.User', on_delete=models.PROTECT)

    def __str__(self):
        return self.customer.first_name + ' ' + self.customer.last_name + 's order. order_id = ' + str(self.id)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name



