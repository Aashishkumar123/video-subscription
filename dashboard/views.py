from django.contrib.auth.models import User
from django.shortcuts import redirect,render
from Accounts.forms import CtryForm,UserProfileForm
from Accounts.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from Accounts.email import send_email
from Accounts.sms import send_otp
from .models import Course,Lectures
import random
# Create your views here.

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def Editprofile(request):
    if request.method == "POST":
        img = 'image' in request.FILES and request.FILES['image']
        f_name = 'first_name' in request.POST and request.POST['first_name']
        l_name = 'last_name' in request.POST and request.POST['last_name']
        gen = 'gender' in request.POST  and request.POST['gender']
        facebook = 'facebook' in request.POST and request.POST['facebook']
        instagram = 'instagram' in request.POST and request.POST['instagram']
        bio = 'bio' in request.POST and request.POST['bio']
        country = CtryForm(request.POST,instance=request.user)
        if country.is_valid():
           c = country.cleaned_data['country']
           profile = Profile.objects.get(user=request.user)
           profile.country = c
           profile.gender = gen
           profile.facebook_link = facebook
           profile.instagram_link = instagram
           profile.bio = bio
           if img:
                profile.image = img
           profile.save()

           user = User.objects.get(username = request.user)
           user.first_name = f_name
           user.last_name = l_name
           user.save()

           messages.success(request,'Profile Updated')
        
    country = CtryForm(instance = request.user.profile)
    return render(request,'edit-profile.html',context={'country':country})

@login_required
def ChangePassword(request):
    if request.method == "POST":
        old_pwd = 'old_pwd' in request.POST and request.POST['old_pwd']
        new_pwd = 'new_pwd' in request.POST and request.POST['new_pwd']
        crfm_pwd = 'crfm_pwd' in request.POST and request.POST['crfm_pwd']
        auth_pwd = authenticate(request,username=request.user,password=old_pwd)
        if auth_pwd is not None:
            if new_pwd != crfm_pwd:
                messages.error(request,'Two password did not matched')
            elif len(new_pwd) and len(crfm_pwd) < 8:
                messages.error(request,'Password must contain at least 8 characters')
            else:
                user = User.objects.get(username=request.user)
                user.password = make_password(new_pwd)
                user.save()
                messages.success(request,'Password Changed Successfully')
        else:
            messages.error(request,'old password did not matched')
    return render(request,'change-password.html')


@login_required
def ChangeEmail(request):
    if request.method == "POST":
        email = 'email' in request.POST and request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.error(request,'This email is already exists')
        else:
            request.session['email'] = email
            otp = random.randint(1000,9999)
            request.session['email_otp'] = otp
            message = f'your otp is {otp}'
            user_email = email
            send_email(message,user_email)
            messages.success(request,'An OTP has been send to your email')
            return redirect('/dashboard/profile/edit/email/otp/')
    return render(request,'change-email.html')

@login_required
def ChangeEmailOTP(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session['email_otp']
        if int(u_otp) == otp:
           user = User.objects.get(username=request.user)
           p =  Profile.objects.get(user=request.user)
           user.email = request.session['email']
           user.save()
           p.email_verified = True
           p.save()
           
           messages.success(request,f'Your email {request.session["email"]} is now updated')
           return redirect('/dashboard/profile/edit/email/')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'change-email-otp.html')

@login_required
def ChangePhoneNumber(request):
    if request.method == "POST":
        phoneForm = UserProfileForm(request.POST, instance=request.user.profile)
        if phoneForm.is_valid():
            number = phoneForm.cleaned_data['phone_number']
            if Profile.objects.filter(phone_number=number).exists():
                messages.error(request,'This phone number is already exists')
            else:
                request.session['number'] = number
                otp = random.randint(1000,9999)
                request.session['otp'] = otp
                message = f'your otp is {otp}'
                send_otp(number,message)
                messages.success(request,'An OTP has been send to your phone number')
                return redirect('/dashboard/profile/edit/phone-number/otp/')
    else:
        phoneForm = UserProfileForm(instance=request.user.profile)
    context = {'pf':phoneForm}
    return render(request,'change-phone-number.html',context)


@login_required
def ChangePhoneNumberOTP(request):
    try:
        if request.method == "POST":
            u_otp = request.POST['otp']
            otp = request.session.get('otp')
            p_number = request.session.get('number')

            if int(u_otp) == otp:
                p = Profile.objects.get(user = request.user)
                p.phone_number = p_number
                p.save()
                messages.success(request,'Phone number has been updated successfully')
                return redirect('/dashboard/profile/edit/phone-number/')
            else:
                messages.error(request,'Wrong OTP')
    except:
        return redirect('/dashboard/profile/edit/phone-number/')
    return render(request,'change-phone-number-otp.html')


def Settings(request):
    if request.method == "POST":
        acc_type = 'account-type' in request.POST and request.POST['account-type']
        profile = Profile.objects.get(user=request.user)
        print(acc_type)
        if acc_type:
            profile.account_type = "Business"
            profile.save()
            messages.success(request,'Settings changed')
        else:
            profile.account_type = "Student"
            profile.save()
            messages.success(request,'Settings changed')

    return render(request,'settings.html')


def courseView(request):
    if request.method == "POST":
        name = 'name' in request.POST and request.POST['name']
        description = 'desc' in request.POST and request.POST['desc']
        thumb = 'thumbnail' in request.FILES and request.FILES['thumbnail']
        course_add = Course(user = request.user,
                            course_name=name,
                            desc = description,
                            thumbnail = thumb)
        course_add.save()
        request.session['course_id'] = course_add.id
        return redirect('/dashboard/add-lectures/')
    return render(request,'course.html')

def lectureView(request):
    if request.method == "POST" and 'lect1' in request.POST:
        name = 'name' in request.POST and request.POST['name']
        description = 'desc' in request.POST and request.POST['desc']
        vid = 'video' in request.FILES and request.FILES['video']
        c_id = Course.objects.get(id=request.session['course_id']) 
        Lectures.objects.create(user = request.user,
                course_id = c_id,
                lecture_name=name,
                video = vid,
                desc = description,
               )
        
    return render(request,'add-lectures.html')