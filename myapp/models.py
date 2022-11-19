import numbers

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100, default="Windsor", blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    length = models.IntegerField()
    pub_date = models.DateField()

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(max_length=100, blank=True)
    interested = models.PositiveIntegerField(default=0, blank=False)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock = self.stock+100


class Client(User):
    PROVINCE_CHOICES = [('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ]
    company = models.CharField(max_length=50 , blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20 , default="Windsor")
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category, related_name="clients")


class Order(models.Model):
    order_choices = [(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'Order Shipped'), (3, 'Order Delivered')]
    product = models.ForeignKey(Product, related_name="products", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="clients", on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=100)
    order_status = models.IntegerField(default=1, choices=order_choices)
    status_date = models.DateField(max_length=30, blank=True, null=True)

    # def __str__(self):
    #     return self.product.name, self.product.price

    @staticmethod
    def total_cost():
        total = 0
        queryset = Order.objects.all()
        for x in queryset:
            total += x.product.price
        return total

