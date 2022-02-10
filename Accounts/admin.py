from django.contrib import admin
from .models import Profile,Subscription_bill,Pricing,Comment
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','bio','phone_number','gender','facebook_link','instagram_link','country','email_verified','unique_id','account_type']


@admin.register(Subscription_bill)
class SubscriptionBillAdmin(admin.ModelAdmin):
    list_display = ['user','subscription_type','price','datetime']


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ['type','price','duration','description'] 
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','comment','course_id','date'] 