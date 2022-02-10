from django.db import models
from django.contrib.auth.models import User



class Course(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course_name = models.CharField(max_length=500)
    thumbnail = models.ImageField(upload_to="course thumbnail")
    desc = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)



class Lectures(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    lecture_name = models.CharField(max_length=500)
    video = models.FileField(upload_to="Lectures")
    desc = models.TextField(max_length=1000)

    