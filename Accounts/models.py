from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
import uuid
from dashboard.models import Course
# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

g_choices = (('Male','Male'),
            ('Female','Female'))

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    image = models.ImageField(upload_to='profile',default='default.png')
    phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    gender = models.CharField(max_length=50,choices=g_choices)
    facebook_link = models.URLField(max_length=200)
    instagram_link = models.URLField(max_length=200)
    country = CountryField()
    email_verified = models.BooleanField(default=False)
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False)
    account_type = models.CharField(max_length=100,default="Student",choices=(('Student','Student'),('Business','Business')))
    


plans = (('BASIC','BASIC'),
        ('ADVANCE','ADVANCE'),
        ('VIP','VIP'),
        ('PREMIUM','PREMIUM'))


class Pricing(models.Model):
    type = models.CharField(primary_key = True, unique=True ,max_length=100,choices=plans)
    price = models.CharField(max_length=100)
    duration = models.CharField(max_length=50,choices=(('month','mo'),('year','yr')))
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.type

class Subscription_bill(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(Pricing,on_delete=models.CASCADE)
    price = models.CharField(max_length=100)
    datetime = models.DateTimeField()

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

