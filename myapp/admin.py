from django.contrib import admin
from .models import Product, Category, Client, Order , Book , Author
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Book)
admin.site.register(Author)