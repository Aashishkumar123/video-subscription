from django.contrib import auth
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as authview

urlpatterns = [
    path('',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('signup/otp/',views.signupOTP,name="signup-otp"),
    path('login/',views.Login,name="login"),
    path('login/otp/',views.loginOTP,name="login-otp"),
    path('logout/',authview.LogoutView.as_view(),name="logout"),
    path('email-verify/',views.email_verification,name="email-verify"),
    path('forget-password/',views.ForgetPassword,name="forget-password"),
    path('reset-password/<slug:uid>/',views.ResetPassword,name="reset-password"),
    path('subscribe/',views.subscribe,name="subscribe"),
    path('subscribe/<type>/',views.subscriptionType,name="subscription-type"),
    path('payment-success/',views.payment_success,name="payment-success"),
    path('<str:course_name>/<int:id>/',views.FullCourse,name="FullCourse"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)