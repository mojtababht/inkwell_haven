from django.db import models

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



