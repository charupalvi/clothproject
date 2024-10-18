from django.shortcuts import render,redirect
from django.views import View
from clothapp.models import Cloth,Cart,Profile,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

categories=Cloth.objects.values('category').distinct()

# Create your views here.
def home(request):
    print('Login in Home Page:',request.user.is_authenticated)
    context={}
    data=Cloth.objects.all()
    context['cloths']=data
    # categories = Cloth.objects.values('category').distinct()
    print(categories)
    context['types']=categories
    return render(request,'index.html',context)

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        context={}
        u = request.POST['username']   #username entered by user must be unique.
        e= request.POST['email']
        p= request.POST['password']
        cp= request.POST['confirmpassword']
        print(u,e,p,cp)
        if u=='' or e=='' or p=='' or cp=='':
            context['error']='Please fill all the details'
            return render(request,'register.html',context)
        elif p != cp:
            context['error']='Password & Confirm Password must be same'
            return render(request,'register.html',context)
        elif User.objects.filter(username=u).exists():
            context['error']='Username already exist. Enter unique username'
            return render(request,'register.html',context)
        else: 
            user=User.objects.create(username=u,email=e) #add the data in db
            user.set_password(p)  # password encryption
            user.save()
            # context['success']='Registration Successfully!!! Please Login'
            # return render(request,'login.html',context)
            messages.success(request,'Registration Successfully!!! Please Login')
            return redirect('/login')

def userLogin(request):  # name can't be login
    if request.method=='GET':
        return render(request,'login.html')
    else:
        # user login code
        context={}
        u = request.POST['username']   #username entered by user must be unique.
        p= request.POST['password']
        user=authenticate(username=u,password=p)
        if user is None:
            context['error']='Invalid Credentials!!!'
            return render(request,'login.html',context)
        else:
            print('successfully authenticated')
            print(request.user.is_authenticated)
            login(request,user)  # session login
            messages.success(request,'Login Successfully!!')
            return redirect('/')

def userLogout(request):
    logout(request)
    messages.warning(request,'Logout Successfully')
    return redirect('/')

def about(request):
    context={}
    context['types']=categories
    return render(request,'about.html',context)

def contact(request):
    context={}
    context['types']=categories
    return render(request,'contact.html',context)

def clothDetails(request,clothid):
    data=Cloth.objects.get(id=clothid)
    context={}
    context['cloth']=data
    return render(request,'details.html',context)

def searchByCat(request,cat):
    data = Cloth.objects.filter(category = cat)
    context = {}
    context['cloths']=data
    return render(request,'index.html',context)

def searchByRange(request):
    # seelct * from cloth where price>=100 and price<=1000
    minprice=request.GET['min']
    maxprice=request.GET['max']
    c1=Q(price__gte=minprice) # condition 1
    c2=Q(price__lte=maxprice) # condition 2
    data=Cloth.objects.filter(c1 & c2)
    context={}
    context['cloths']=data
    return render(request,'index.html',context)

def sortClothsByPrice(request,dir):
    if dir == 0:
        col='price'
    else:
        col='-price'
    data = Cloth.objects.all().order_by(col)
    context={}
    context['cloths']=data
    return render(request,'index.html',context)

def addToCart(request,clothid):
    userid=request.user.id
    if userid:
        cloth=Cloth.objects.get(id = clothid)
        cart=Cart.objects.create(clothid=cloth,uid=request.user)
        cart.save()
        messages.success(request,'Item Added To Cart')
        return redirect('/')
    else:
        messages.error(request,'Please Login')
        return redirect('/login')

def showMyCart(request):
    userid=request.user.id
    data = Cart.objects.filter(uid = userid)
    context={}
    context['cartlist']=data
    count=len(data)
    total=0
    for cart in data:
        total+=cart.clothid.price*cart.quantity
    context['count']=count
    context['total']=total
    return render(request,'cart.html',context)

def removeCart(request,cartid):
    cart=Cart.objects.filter(id = cartid)
    cart.delete()
    messages.error(request,'Product Removed')
    return redirect('/mycart')

def updateQuantity(request,cartid,oprn):
    if oprn == 'incr':
        cart =Cart.objects.filter(id = cartid)
        qty=cart[0].quantity
        cart.update(quantity=qty+1)
        return redirect('/mycart')
    else:
        cart =Cart.objects.filter(id = cartid)
        qty=cart[0].quantity
        cart.update(quantity=qty-1)
        return redirect('/mycart')
    
def confirmOrder(request):
    userid=request.user.id
    data = Cart.objects.filter(uid = userid)
    context={}
    context['cartlist']=data
    count=len(data)
    total=0
    final=0
    gst=(18/100)
    delivery=40
    for cart in data:
        total+=cart.clothid.price*cart.quantity
        final=total+delivery+gst
    context['count']=count
    context['total']=total
    context['delivery']=delivery
    context['final']=final
    context['profile']=Profile.objects.get(id = userid)
    return render(request,'confirmorder.html',context)

def editProfile(request):
    if request.method=='GET':
        userid=request.user.id
        context={}
        # context['profile']=Profile.objects.get(id = userid)
        return render(request,'profile.html',context)
    else:
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        m=request.POST['mobile']
        a=request.POST['address']

        userid = request.user.id
        user = User.objects.filter(id=userid)
        user.update(first_name=fn,last_name=ln)

        profile=Profile.objects.create(id = user[0], mobile = m,address = a)
        profile.save()
        messages.success(request,'Profile Updated!!!')
        # return render(request,'profile.html')
        return redirect('/')
    
def makePayment(request):
    userid=request.user.id
    data = Cart.objects.filter(uid = userid)
    total=0
    final=0
    gst=(18/100)
    delivery=40
    for cart in data:
        total+=cart.clothid.price*cart.quantity
        final=total+delivery+gst
    client = razorpay.Client(auth=("rzp_test_HvIGtSTMlJFiX8", "DBCOWH1HZktdTqlBVBCLm6gX"))
    data = { "amount": final*100, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    context['profile']=Profile.objects.get(id = userid)
    return render(request,'pay.html',context)

def placeOrder(request,oid):
    '''
    1.userid
    2.cart fetch
    3.insert order details
    4.cart clear
    5.send email
    6.print message on homepage
    '''

    userid=request.user.id
    # user=User.objects.get(id=userid)
    cartlist = Cart.objects.filter(uid = userid)
    for cart in cartlist:
        # cloth=Cloth.objects.get(id=cart.clothid)
        order=Order.objects.create(orderid=oid,userid=cart.uid,clothid=cart.clothid,quantity=cart.quantity)
        order.save()
    cartlist.delete()
    # sending email
    msg='Thank You for Placing the order. Your Order Id is: '+oid
    send_mail(
        "Order Placed Successfully!!!",
        msg,
        "dcharlie919@gmail.com",
        [request.user.email],
        fail_silently=False,
    )
    messages.success(request,'Order Placed Successfully!!!')
    return redirect('/')
        

