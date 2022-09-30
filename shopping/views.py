from math import prod
from django.http import HttpResponseRedirect, JsonResponse , HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from .forms import LoginForm , SignupForm , UserEditForm , AdminEditForm , createproductform
from .models import BuyerProfile , SellerProfile , Product , Cart , OrderDetail
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout , update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
import stripe
from Hexashop import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as stt
from django.core.mail import send_mail

# Create your views here.
def index(request):
    all_post = Product.objects.all()
    paginator = Paginator(all_post,3,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'shopping/index.html',{'page_obj':page_obj})

#------------------------------------------------

# def search(request):
#     q = request.GET['q']
#     all_post = Product.objects.filter(title__icontains=q)    
#     return render(request,'shopping/search.html',{'page_obj':all_post})

def search(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Product.objects.filter(name__contains=query_name)
            return render(request, 'shopping/search.html', {"page_obj":results})

    return render(request, 'shopping/search.html')

#-----------------------------

def about(request):
    return render(request,'shopping/about.html')

def contact(request):
    return render(request,'shopping/contact.html')

def products(request):
    return render(request,'shopping/products.html')

def single_product(request):
    return render(request,'shopping/single_product.html')

#----------------------------------------------------------

def signup(request):
    return render(request,'shopping/signup.html')

#-------------------------------------------------------
def buyer_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST) 
        if form.is_valid() :            
            user = form.save()
            mob= form.cleaned_data['mob']
            dob= form.cleaned_data['dob']
            hobby= form.cleaned_data['hobby']
            gender= form.cleaned_data['gender']
            # user_type= form.cleaned_data['user_type']  
            profile = BuyerProfile(user = user, mob = mob , dob=dob , hobby=hobby , gender = gender )
            profile.save()
            subject = 'welcome to Hexashop world'
            message = f'Hi {user.username}, thank you for registering in Hexashop!!!!!.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list ) 
            messages.success(request,"Email sent successfully!!!!!")                       
            form.save()
                        
            form = SignupForm()            
    else:
        form = SignupForm()        
    return render(request,'shopping/buyer_signup.html',{'form':form})

#------------------------------------------------------------------

def seller_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST) 
        if form.is_valid() :            
            user = form.save()
            mob= form.cleaned_data['mob']
            dob= form.cleaned_data['dob']
            hobby= form.cleaned_data['hobby']
            gender= form.cleaned_data['gender']
            # user_type= form.cleaned_data['user_type']  
            profile = SellerProfile(user = user, mob = mob , dob=dob , hobby=hobby , gender = gender)
            profile.save()            
            form.save()
            form = SignupForm()            
    else:
        form = SignupForm()        
    return render(request,'shopping/seller_signup.html',{'form':form})
#--------------------------------------------------------------------------

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully!!!')
                    return HttpResponseRedirect('/')
                form.save()
        else:
            form = LoginForm()
        return render(request,'shopping/login.html',{'form':form})
    return HttpResponseRedirect('/')

#------------------------------------------------------------------

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#-----------------------------------------------------------------

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = AdminEditForm(request.POST, instance=request.user)
                users = User.objects.all()      
            else:
                fm = UserEditForm(request.POST,instance=request.user)
                users = None
            if fm.is_valid():
                messages.success(request,'Changed Successfully!!!!')
                fm.save()            
        else:
            if request.user.is_superuser == True:
                fm = AdminEditForm(instance=request.user)
                users = User.objects.all()
            else:
                fm = UserEditForm(instance=request.user)
                users = None
        return render(request , 'shopping/profile.html',{'name':request.user,"form":fm,'users':users})
    else:
        return HttpResponseRedirect('/login/')

#-------------------------------------------------------------

def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'You have successfully changed your password')
                return HttpResponseRedirect('/login/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,'shopping/changepassword.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#--------------------------------------------

# def user_detail(request,id):
#     if request.user.is_authenticated:
#         pi = User.objects.get(pk=id)
#         fm = AdminEditForm(instance=pi)
#         return render(request,'shopping/userdetail.html',{'form':fm})
#     else:
#         return HttpResponseRedirect('/login/')

#----------------------------------------------------

def add_product(request):
    
    if request.method=='POST':
        form=createproductform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    img = Product.objects.all()

    form=createproductform()
    return render(request,'shopping/add_product.html',{'form':form})

#------------------------------------------------------

def cart(request):
    # print("cart")
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.item_quantity * p.product.price)
            # print('-------------------------',tempamount)
            amount += tempamount
            totalamount = amount + shipping_amount  
        
        
        return render(request,'shopping/cart.html',{'carts':cart,'amount':amount,'totalamount':totalamount,'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


#-------------------------------------------
#-------**************Pagination*******************------------------
#
# def post_list(request):
#     all_post = Product.objects.all()
#     paginator = Paginator(all_post,3,orphans=1)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request,'shopping/pagination.html',{'page_obj':page_obj})

#---------------------------------------

def addtocart(request):
    if request.user.is_authenticated:
        user = request.user
        print("---------------------------->",user)
        product_id = request.GET.get('product_id')
        print("--------------------->",product_id)
        product = Product.objects.get(id=product_id)
        print("------------------------------>>>>>>>>>",product)
        Cart(user=user , product=product , item_amount = product.price).save()
        messages.success(request, ' Add product Successfully!')
        return redirect("/")
    else:
        return redirect("/login")

#----------------------------------------

def removetocart(request):
    print("----------------->")
    if request.method == "GET":
        print("--------------!!!!!!!!!!")
        user = request.user
        print("-------------------",user)
        product_id = request.GET.get('id')
        print("------------------>",product_id)
        remove_item = Cart.objects.filter(Q(id=product_id) & Q(user=request.user))
        print("-------------------",remove_item)
        remove_item.delete()
        return redirect('/cart/')

#---------------------------------------

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['product_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user=request.user))
        print('------------------->',c)
        c.item_quantity += 1
        print('----------------->',c.item_quantity)
        a= c.item_quantity
        b= c.product.price
        print('------------>amount',b)
        print("---------------->quntity",a)
        all = a*b
        c.item_amount=all
        c.save()
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == request.user ]
        for p in cart_product:
            tempamount = (p.item_quantity * p.item_amount)
            # print('-------------------------',tempamount)
            amount += tempamount
            totalamount = amount + shipping_amount
            # print('----------------------',totalamount)
        data = {'item_quantity':c.item_quantity,
                    'amount':amount,
                    'totalamount':totalamount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product = product_id) & Q(user=user))
        c.item_quantity -= 1
        a = c.item_quantity
        b = c.product.price
        d = a*b
        c.item_amount = d
        c.save()
        amount = 0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.item_quantity * p.product.price)
            amount += tempamount
            totalamount = amount + shipping_amount
        data = {'item_quantity':c.item_quantity,
                    'amount':amount,
                    'totalamount':totalamount}
        return JsonResponse(data)

@csrf_exempt
def create_checkout_session(request,id):
    print("hello")
    print('-------------------------->>>',type(id))
    # request_data = request.user.email
    user = request.user
    cart = Cart.objects.filter(user=user)
    print("---------------------------->",cart)
    if type(id) == str:
        all_price = 0
        for i in cart:
            all_price += i.item_amount
        print("--------------->all price",all_price)
        # product = get_object_or_404(Cart, pk = id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            customer_email = "abc@gmail.com",
            payment_method_types = ['card'],
            line_items = [

                {
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                        'name': "All Products",
                        },
                        'unit_amount': all_price*100,  
                    },
                    'quantity': 1,
                }
            ],
            mode = 'payment',
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )
        print("--------------->checkout_session",checkout_session)
        order = OrderDetail()
        print("---------------------->",order)
        order.customer_email = "abc@gmail.com"
        order.stripe_payment_intent = checkout_session['payment_intent']
        order.amount = int(all_price * 100)
        order.save()
    # return JsonResponse({'data': checkout_session})
        return JsonResponse({'sessionId': checkout_session.id})
        
def PaymentSuccessView(request):
    return render(request,'shopping/success.html')    


def PaymentFailedView(request):
    return render(request,'shopping/failed.html')    
