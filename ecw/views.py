
from django.shortcuts import render,redirect
from .models import CustomerData
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from .models import CartItem, Order
from .models import CustomerData, Cart,Product
from django.conf import settings
import razorpay
from django.contrib.auth.models import User

def home(request):
    return render(request,'ecw/home.html')

def signup(request):
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': "Passwords do not match"
            })
        user=CustomerData.objects.create(
            name=name,
            email=email,
            password=make_password(password)
           )
        request.session['user_id'] = user.id
        return redirect('login')

    return render(request, 'ecw/signup.html')

def profile(request):
    user_id = request.session.get('user_id')
    user = CustomerData.objects.get(id=user_id)
    if not user_id:
        return redirect('login')
    return render(request, 'ecw/profile.html', {
        'user': user
    })

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomerData.objects.filter(email=email).first()

        if not user:
            return render(request, 'ecw/login.html', {
                "error_message": "User does not exist"
            })

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session.modified = True  
            return redirect('dashboard')

        return render(request, 'ecw/login.html', {
            "error_message": "Incorrect password"
        })

    return render(request, 'ecw/login.html')




def dashboard(request):
    return render(request,'ecw/dashboard.html')


def electronics(request):
      products=Product.objects.all()
      return render(request,'ecw/electronics.html',{'products':products})




def view(request, id):

    product = Product.objects.get(id=id)
    return render(request, 'ecw/electronics_details.html', {'product': product})

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    return redirect('electronics')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity
        total_price += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'ecw/view_cart.html', {'cart_items': cart_items ,'total_price': total_price})

def logout(request):
    request.session.flush()
    return redirect('home')

def place_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = CustomerData.objects.get(id=user_id)
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('view_cart')

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        Order.objects.create(
            user=user,
            product=product.name,
            subtotal=product.price,
            quantity=quantity,
            image=product.image
        )
    request.session['cart'] = {}

    return redirect('dashboard')


def order_success(request):
    return render(request, 'ecw/order_success.html')

def my_orders(request):
    user_id = request.session.get('user_id')
    user = CustomerData.objects.get(id=user_id)
    orders = Order.objects.filter(user=user)


    return render(request, 'ecw/my_orders.html', {'orders': orders})

def order(request,id):
   
    product = Product.objects.get(id=id)
    return render(request, 'ecw/order_view.html', {'product': product})

def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    return redirect('view_cart')

def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]   
    request.session['cart'] = cart
    return redirect('view_cart')

def pl_order(request):

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')
    
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total += float(product.price) * quantity
    
    if total <= 0:
        return redirect('view_cart')
    
    amount = (total * 100)

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })
    user=CustomerData.objects.get(id=user_id)
    return render(request, 'ecw/check.html', {
        'order_id':order['id'],
        'amount': total,
        'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID,
         'Name' : user.name,
         'Email' : user.email
    })  