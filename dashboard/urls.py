from django.urls import path
from .import views

urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('profile/edit/',views.Editprofile,name='edit-profile'),
    path('profile/edit/password/', views.ChangePassword,name="change-password"),
    path('profile/edit/email/', views.ChangeEmail,name="change-email"),
    path('profile/edit/email/otp/', views.ChangeEmailOTP,name="change-email-otp"),
    path('profile/edit/phone-number/', views.ChangePhoneNumber,name="change-phone-number"),
    path('profile/edit/phone-number/otp/', views.ChangePhoneNumberOTP,name="change-phone-number-otp"),
    path('courses/', views.courseView,name="Course"),
    path('add-lectures/', views.lectureView,name="Lecture"),
    path('settings/',views.Settings,name="Settings"),

]

