from django.http import HttpResponse
from django.shortcuts import render,redirect
from app.models import Categories,Product,contactus,order,Brand

from django.contrib.auth import authenticate,login
from app.models import UserCreateForm

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def Home(request):
    categories = Categories.objects.all()

    brand = Brand.objects.all()

    categoryID = request.GET.get('category')

    brandid = request.GET.get('brand')


    if categoryID:
        product = Product.objects.filter(subCategory = categoryID).order_by('-id')
    elif brandid:
        product = Product.objects.filter(brand = brandid).order_by('-id')
    else:
        product = Product.objects.all()[:9]

    data = {
        'categories':categories,
        'product':product,
        'brand':brand,
    }

    return render(request, 'index.html', data)


def Signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()

    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html',context)

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('index')

@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product=product)
    return redirect('cart_detail')

@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('cart_detail')

@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect('cart_detail')

@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)    
    cart.clear()
    return redirect('cart_detail')
    
@login_required(login_url="/accounts/login/")
def cart_detail(request):
    
    cart = request.session['cart']

    context = {
        'cart':cart
    }

    return render(request, 'cart/cart_detail.html',context)
        

# contact us

def Contact(request):
    if request.method == "POST":

        contact = contactus(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )

        contact.save()
    return render(request, 'contactus.html')


def Checkout(request):

    if request.method == "POST":
        Phone = request.POST.get('Phone')
        Address = request.POST.get('Address')
        PostalCode = request.POST.get('PostalCode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)

        # print(Phone, Address, PostalCode, cart, user)

        for i in cart:
            
            a = cart[i]['quantity']
            b = (int(cart[i]['price']))
            total = a * b

            Order = order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = Address,
                phone = Phone,
                pincode = PostalCode,
                total = total,
            )
            Order.save()

        request.session['cart'] = {}
        return redirect('index')

    return HttpResponse("checkout page")
    

def YourOrder(request):

    # uid = request.session.get('_auth_user_id')
    # user = User.objects.get(pk = uid)

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk = uid)

    Order = order.objects.filter(user = user)

    context = {
        'order' : Order
    }

    return render(request, 'order.html', context)



def Product_Page(request):

    categories = Categories.objects.all()

    brand = Brand.objects.all()

    categoryID = request.GET.get('category')

    brandid = request.GET.get('brand')


    if categoryID:
        product = Product.objects.filter(subCategory = categoryID).order_by('-id')
    elif brandid:
        product = Product.objects.filter(brand = brandid).order_by('-id')
    else:
        product = Product.objects.all()

    data = {
        'categories':categories,
        'product':product,
        'brand':brand,
    }

    return render(request, 'product_page.html',data)

def ProductDetails(request, id):
    product = Product.objects.filter(id = id).first()
    
    context = {
        'product':product
    }

    return render(request, 'product_details.html',context)

def Search(request):

    search = request.GET['search']

    product = Product.objects.filter(name__icontains = search)
    
    context = {
        'product':product
    }

    return render(request, 'search.html',context)

