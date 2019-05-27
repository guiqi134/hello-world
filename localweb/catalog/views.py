from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse
from catalog.models import Account, Customer, Restaurant, Rider, Food, Order
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from catalog import forms
from cart.cart import Cart
from cart import models
import time
import hashlib

# Create your views here.


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


@csrf_exempt
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    index_form = forms.IndexForm()
    rest_list = Restaurant.objects.all().exclude(RName__isnull=True)
    customer_info = Customer.objects.get(AName=request.session['user_name'])

    if request.POST.get('click', False): # check if called by click
        address = request.POST.get('address')
        customer = Customer.objects.get(AName_id=request.session['user_name'])
        customer.address = address
        customer.save()
        return HttpResponse(address)

    context = {
        'index_form': index_form,
        'rest_list': rest_list,
        'customer_info': customer_info
    }

    return render(request, 'index.html', context=context)


def restaurant_detail(request, pk):
    restaurant_info = get_object_or_404(Restaurant, pk=pk)
    food_list = Food.objects.filter(RName=restaurant_info.RName).exclude(count=0)

    context = {
        'restaurant_info': restaurant_info,
        'food_list': food_list
    }

    return render(request, 'restaurant_detail.html', context)


def add_to_cart(request, food_id):
    food = Food.objects.get(food_id=food_id)
    cart = Cart(request)
    cart.add(food, food.price, quantity=1)
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, food_id):
    food = Food.objects.get(food_id=food_id)
    cart = Cart(request)
    cart.remove(food)
    return redirect('/index/cart/')


def get_cart(request):
    message = ''

    if request.POST:
        # 下单食物数量减少，创建order,购物车清空
        cart_id = request.session.get('CART-ID')

        # 下单的食物count数量减少
        items = models.Item.objects.filter(cart_id=cart_id).values('quantity', 'unit_price', 'object_id')
        total_price = 0
        food_list = []
        rest_set = set()  # check if there more than one restaurant
        for item in items:
            food_id = item['object_id']
            total_price += item['quantity'] * item['unit_price']
            food = Food.objects.get(food_id=food_id)
            rest_set.add(food.RName)

        if len(rest_set) != 1:
            message = '商家必须相同'
        else:
            for item in items:
                food_id = item['object_id']
                food = Food.objects.get(food_id=food_id)
                food.count -= 1
                food_list.append(food)
                food.save()

            # 成功下单的cart
            cart = models.Cart.objects.get(id=cart_id)
            cart.checked_out = True
            cart.save()
            
            # 创建order
            new_order = Order()
            customer_id = Customer.objects.get(AName=request.session['user_name'])
            new_order.total_price = total_price
            new_order.save()
            new_order.foods.add(*food_list)
            new_order.restaurant_id = list(rest_set)[0]
            new_order.customer_id = customer_id
            new_order.address = Customer.objects.filter(AName=request.session['user_name']).values('address')[0]['address']
            new_order.save()

            # 购物车清空
            request.session['CART-ID'] = False
            new_cart = Cart(request)

            return redirect('/index/customer_order/')
    
    context = {
        'cart': Cart(request),
        'message': message
    }

    return render(request, 'cart.html', context=context)


@csrf_exempt
def customer_order(request):
    orders = Order.objects.filter(customer_id=request.session['user_name'])

    if request.POST.get('status') == 'restaurant':
        rest_rating = float(request.POST.get('rest_rating'))
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.rest_rating = rest_rating
        order.save()
        return HttpResponse(rest_rating)

    elif request.POST.get('status') == 'rider':
        rider_rating = float(request.POST.get('rider_rating'))
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.rider_rating = rider_rating
        order.save()
        return HttpResponse(rider_rating)

    return render(request, 'customer_order.html', {'orders': orders})


def login(request):
    login_form = forms.LoginForm()
    message = ''
    redirect_page = ''


    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = Account.objects.get(AName=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_name'] = user.AName
                    request.session['account_type'] = user.account_type
                    if user.account_type == 'customer':
                        customer = Customer.objects.get(AName_id=user.AName)
                        # request.session['address'] = customer.address
                        redirect_page = '/index/'
                    elif user.account_type == 'restaurant':
                        redirect_page = '/restaurant/'
                    elif user.account_type == 'rider':
                        redirect_page = '/rider/'
                    return redirect(redirect_page)
                else:
                    message = '密码错误!'
            except:
                message = '用户不存在!'
        else:
            message = '请正确填写内容!'

    context = {
        'login_form': login_form,
        'message': message
    }

    return render(request, 'login.html', context=context)


def register(request):
    register_form = forms.RegisterForm()
    message = ''

    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            confirm_pw = register_form.cleaned_data.get('confirm_pw')
            sex = register_form.cleaned_data.get('sex')
            last_name = register_form.cleaned_data.get('last_name')
            first_name = register_form.cleaned_data.get('first_name')
            birth = register_form.cleaned_data.get('birth')
            email = register_form.cleaned_data.get('email')
            personal_ID = register_form.cleaned_data.get('personal_ID')
            phone = register_form.cleaned_data.get('phone')
            role = register_form.cleaned_data.get('role')

            if password != confirm_pw:
                message = '两次密码不同!'
            else:
                sanme_name_user = Account.objects.filter(AName=username)
                same_email_user = Account.objects.filter(email=email)
                same_phone_user = Account.objects.filter(phone=phone)
                same_personal_ID_user = Account.objects.filter(personal_ID=personal_ID)
                if sanme_name_user:
                    message = '账户已存在'
                elif same_email_user:
                    message = '邮箱已存在'
                elif same_phone_user:
                    message = '手机号已存在'
                elif same_personal_ID_user:
                    message = '身份证已存在'
                else:
                    new_user = Account()
                    new_user.AName = username
                    new_user.password = hash_code(password)
                    new_user.sex = sex
                    new_user.last_name = last_name
                    new_user.first_name = first_name
                    new_user.birth = birth
                    new_user.email = email
                    new_user.personal_ID = personal_ID
                    new_user.phone = phone
                    new_user.account_type = role
                    new_user.save()
                    if new_user.account_type == 'customer':
                        new_customer = Customer()
                        new_customer.AName_id = username
                        new_customer.save()
                    elif new_user.account_type == 'restaurant':
                        new_restaurant = Restaurant()
                        new_restaurant.AName_id = username
                        new_restaurant.save()
                    elif new_user.account_type == 'rider':
                        new_rider = Rider()
                        new_rider.AName_id = username
                        new_rider.save()
                    
                    return redirect('/login/')

    context = {
        'register_form': register_form,
        'message': message
    }

    return render(request, 'register.html', context=context)


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()

    return redirect('/login/')


def get_password(request):
    pass
    return render(request, 'get_password.html')


@csrf_exempt
def restaurant(request):
    rest_info = Restaurant.objects.get(AName_id=request.session['user_name'])
    rest_name = Restaurant.objects.filter(AName_id=request.session['user_name']).values('RName')[0]['RName']
    request.session['rest_name'] = rest_name
    rest_foods = Food.objects.filter(RName_id=rest_name).exclude(count=0)
    rest_ratings = Order.objects.filter(restaurant_id=rest_name).values('rest_rating')

    rating_list = []
    for rest_rating in rest_ratings:
        rating = rest_rating['rest_rating']
        if rating != -1:
            rating_list.append(rating)
    if len(rating_list) == 0:
        avg_rating = 0
    else:
        avg_rating = sum(rating_list) / len(rating_list)

    # 更改商家信息
    if request.POST.get('status') == 'change_FName':
        change_FName = request.POST.get('food_name')
        food_id = request.POST.get('food_id')
        food = Food.objects.get(food_id=food_id)
        food.FName = change_FName
        food.save()
        return HttpResponse(change_FName)

    elif request.POST.get('status') == 'change_price':
        change_price = request.POST.get('food_price')
        food_id = request.POST.get('food_id')
        food = Food.objects.get(food_id=food_id)
        food.price = change_price
        food.save()
        return HttpResponse(change_price)
    
    elif request.POST.get('status') == 'change_count':
        change_count = request.POST.get('food_count')
        food_id = request.POST.get('food_id')
        food = Food.objects.get(food_id=food_id)
        food.count = change_count
        food.save()
        return HttpResponse(change_count)

    context = {
        'rest_info': rest_info,
        'rest_foods': rest_foods,
        'rest_rating': avg_rating,
    }

    return render(request, 'restaurant.html', context=context)


@csrf_exempt
def restaurant_order(request):
    orders = Order.objects.filter(restaurant_id=request.session['rest_name'])

    if request.POST.get('status') == 'change_status':
        order_status = request.POST.get('order_status')
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.order_status = order_status
        order.save()
        return HttpResponse(order_status)

    return render(request, 'restaurant_order.html', {'orders': orders})


@csrf_exempt
def rider(request):
    orders = Order.objects.filter(order_status='未起送')
    
    if request.POST.get('status') == 'take_order':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.rider_id = request.session['user_name']
        order.order_status = '正在配送'
        order.save()
        return HttpResponse()
    
    return render(request, 'rider.html', {'orders': orders})


@csrf_exempt
def rider_order(request):
    orders = Order.objects.filter(rider_id=request.session['user_name'])

    if request.POST.get('status') == 'end_order':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.order_status = '已送达'
        # HH:MM[:ss[.uuuuuu]]
        now = time.strftime("%H:%M[:%S[.%f]]", time.localtime(time.time()))
        order.end_time = now
        order.save()
        return HttpResponse()

    return render(request, 'rider_order.html', {'orders': orders})
