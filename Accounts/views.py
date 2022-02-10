from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm,UserProfileForm
from .models import Pricing, Profile, Comment
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from .sms import send_otp
from .email import send_email
from django.contrib.auth.models import Group
from .models import Subscription_bill
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Profile
from dashboard.models import Course,Lectures

# Create your views here.

def home(request):
    if request.method == "POST":
        otp = random.randint(1000,9999)
        request.session['email_otp'] = otp
        message = f'your otp is {otp}'
        user_email = request.user.email
        send_email(message,user_email)
        return redirect('/email-verify/')

    course = Course.objects.filter(approved=True)

    context = {'course':course}
    return render(request,'home.html',context)

def signup(request):
    if request.method == "POST":
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        if fm.is_valid() and up.is_valid():
            e = fm.cleaned_data['email']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password1']
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = up.cleaned_data['phone_number']
            request.session['number'] = p_number
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            message = f'your otp is {otp}'
            send_otp(p_number,message)
            return redirect('/signup/otp/')

    else:
        fm  = UserRegistrationForm()
        up = UserProfileForm()
    context = {'fm':fm,'up':up}
    return render(request, 'signup.html',context)



def signupOTP(request):
    try:
        if request.method == "POST":
            u_otp = request.POST['otp']
            otp = request.session.get('otp')
            user = request.session['username']
            hash_pwd = make_password(request.session.get('password'))
            p_number = request.session.get('number')
            email_address = request.session.get('email') 

            if int(u_otp) == otp:
                User.objects.create(
                                username = user,
                                email=email_address,
                                password=hash_pwd
                )
                user_instance = User.objects.get(username=user)
                Profile.objects.create(
                                user = user_instance,phone_number=p_number
                )
                request.session.delete('otp')
                request.session.delete('user')
                request.session.delete('email')
                request.session.delete('password')
                request.session.delete('phone_number')

                messages.success(request,'Registration Successfully Done !!')

                return redirect('/login/')
            
            else:
                messages.error(request,'Wrong OTP')
    except:
        return redirect('/')


    return render(request,'signup-otp.html')


def Login(request):

    # try :
    #     if request.session.get('failed') > 2:
    #         return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    # except:
    #     request.session['failed'] = 0
    #     request.session.set_expiry(100)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['username'] = username
            request.session['password'] = password
            u = User.objects.get(username=username)
            p = Profile.objects.get(user=u)
            p_number = p.phone_number
            otp = random.randint(1000,9999)
            request.session['login_otp'] = otp
            message = f'your otp is {otp}'
            send_otp(p_number,message)
            return redirect('/login/otp/')
        else:
            messages.error(request,'username or password is wrong')
    return render(request,'login.html')

def loginOTP(request):
    try:
        if request.method == "POST":
            username = request.session['username']
            password = request.session['password']
            otp = request.session.get('login_otp')
            u_otp = request.POST['otp']
            if int(u_otp) == otp:
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    request.session.delete('login_otp')
                    # messages.success(request,'You are Logged in successfully')
                    return redirect('/')
            else:
                messages.error(request,'Wrong OTP')
    except:
        return redirect('/')
    return render(request,'login-otp.html')



def email_verification(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session['email_otp']
        if int(u_otp) == otp:
           p =  Profile.objects.get(user=request.user)
           p.email_verified = True
           p.save()
           messages.success(request,f'Your email {request.user.email} is verified now')
           return redirect('/')
        else:
            messages.error(request,'Wrong OTP')


    return render(request,'email-verified.html')





def subscribe(request):
    pricing = Pricing.objects.all()
    basic = Pricing.objects.get(type="BASIC")
    advance = Pricing.objects.get(type="ADVANCE")
    vip = Pricing.objects.get(type="VIP")
    premium = Pricing.objects.get(type="PREMIUM")
    context = {'pricing':pricing,'basic':basic,'advance':advance,'vip':vip,'premium':premium}
    return render(request,'subscribe.html',context)

@login_required
def subscriptionType(request,type):
    pricing = Pricing.objects.get(type=type.upper())
    if request.user.groups.all().exists():
        return redirect('/subscribe/')
    elif request.method == "POST":
        my_group = Group.objects.get(name=type.upper()) 
        my_group.user_set.add(request.user)
        Subscription_bill.objects.create(user=request.user,subscription_type=pricing,price=pricing.price,datetime = datetime.now())
        request.session['type'] = type.upper()
        request.session['price'] = pricing.price
        return redirect('/payment-success/')
    
    context = {'type':type,'pricing':pricing}
    return render(request,'subscription-type.html',context)

@login_required
def payment_success(request):
   
    return render(request, 'payment-success.html')

def ForgetPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            uid = User.objects.get(email=email)
            url = f'http://127.0.0.1:8000/reset-password/{uid.profile.unique_id}'
            send_email(url,email)
            messages.success(request,'A Reset password link has send to you email')
        else:
            messages.error(request,'This email is not regsitered')
    return render(request,'forget-password.html')


def ResetPassword(request,uid):
    try:
        if Profile.objects.filter(unique_id = uid).exists():
            if request.method == "POST":
                pass1 = 'password1' in request.POST and request.POST['password1']
                pass2 =  'password2' in request.POST and request.POST['password2']
                if pass1 == pass2:
                    p = Profile.objects.get(unique_id=uid)
                    u = p.user
                    user = User.objects.get(username=u)
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(request,'Password has been reset successfully')
                    return redirect('/login/')
                else:
                    messages.error(request,'Password did not matched')
                
        else:
            return HttpResponse('Wrong URL')
    except:
        return HttpResponse('Wrong URL')
    return render(request,'reset-password.html')



def FullCourse(request,course_name,id):

    if request.method == "POST":
        cmt = 'comment' in request.POST and request.POST['comment']
        c_id = Course.objects.get(id=id)
        Comment.objects.create(user=request.user,comment=cmt,course_id=c_id)

    comment = Comment.objects.filter(course_id=id)
    course = Course.objects.get(id=id)
    lecture = Lectures.objects.filter(course_id=id)
    context = {"lecture":lecture,"course_name":course_name,"course":course,"comment":comment}
    return render(request,'full-course.html',context)