from django.urls import path
from myapp import views
app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path(r'myorders/', views.my_orders, name='orders'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>', views.detail, name='cat_no'),
    path(r'products/', views.products, name='products'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'products/<int:prod_id>', views.productdetail, name='productdetail')
]
