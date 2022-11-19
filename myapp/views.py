import datetime

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone

from .forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of categories: ' + '</p>'
    # response.write(heading1)
    # for category in cat_list:
    #     para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
    #     response.write(para)
    # heading2 = '<p>' + 'List of Products: ' + '</p>'
    # response.write(heading2)
    # product_list = Product.objects.all().order_by('-price')[:5]
    # for product in product_list:
    #     para = '<p>' + str(product.id) + ': ' + str(product.name) + '</p>'
    #     response.write(para)
    # return response
    context = {
        'cat_list': cat_list,
        'user': request.user
    }
    return render(request, 'myapp/index.html', context=context)


def about(request):
    # para = '<h1>' + "This is an Online Store APP" + '</h1>'
    if 'about_visits' in request.COOKIES.keys():
        number_visits = request.COOKIES['about_visits']
        number_visits = int(number_visits) + 1
    else:
        number_visits = 1

    response = render(request, 'myapp/about.html', {'number_visits': number_visits})
    response.set_cookie('about_visits', value=number_visits, max_age=300)
    return response
    # return render(request, 'myapp/about.html')
    # if request.session.get('about_visits', False):
    #     request.session['about_visits'] = request.session.get('about_visits') +1
    # else:
    #     request.session['about_visits']=1
    #
    # return render(request, 'myapp/about.html', {'about_visits':  request.session.get('about_visits')})


def detail(request, cat_no):
    cat_obj = get_object_or_404(Category, pk=cat_no)
    # response = HttpResponse()
    # response.write('<h1>' + cat_obj.warehouse + '</h1>')
    prod_obj = Product.objects.filter(category=cat_obj)
    #     para = '<p>' + str(product.id) + ': ' + str(product.name) + '</p>'
    #     response.write(para)
    return render(request, 'myapp/detail.html', {'cat_obj': cat_obj, 'prod_obj': prod_obj})


def products(request):
    prodlist = Product.objects.all().order_by('id')
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully.'
                order.product.refill()
                order.save()
            else:
                msg = 'We do not have sufficient stock to fill yourorder.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    prod_obj = get_object_or_404(Product, pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        # breakpoint()
        if form.is_valid():
            # detailform = form.save(commit=False)
            if int(form.data['interested']) == 1:
                prod_obj.interested = prod_obj.interested+1

                prod_obj.save()
                # form.save()
            return render(request, 'myapp/productdetail.html', {'form': form, 'prod_obj': prod_obj})
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form': form, 'prod_obj': prod_obj})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                HttpResponse(user.last_login)
                # if request.session.get_expiry_age()==0:
                #     msg = "Your last login was more than 1 hour ago"
                if 'last_login' in request.session:
                    session_obj = str(request.session['last_login'])
                    msg = "Last login date and time:" + str(request.session['last_login'])
                    messages.success(request, 'Last login date and time: ' + str(request.session['last_login']))
                    render(request, 'myapp/index.html', {'last_login': session_obj})
                else:
                    request.session['last_login'] = str(timezone.now())
                    # print(request.session['last_login'])
                    msg = "Your last login was more than 1 hour ago"
                    render(request, 'myapp/index.html', {'last_login': msg})

                # request.session['last_login'] = str(timezone.now())

                request.session['username'] = username
                request.session['user_first_name'] = user.first_name
                request.session['user_last_name'] = user.last_name
                request.session.set_expiry(30)

                return HttpResponseRedirect(reverse('myapp:index'))

            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def my_orders(request):
    # username = login.__name__
    user = request.user
    client_obj = Client.objects.filter(id=user.id)
    if client_obj:
        orderobj = Order.objects.filter(client__id=client_obj[0].id)
        return render(request, 'myapp/myorders.html', {'orderobj': orderobj})
    else:
        return HttpResponse('You are not a registered client!')
