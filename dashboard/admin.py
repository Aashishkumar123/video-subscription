from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Course,Lectures
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','user','course_name','thumbnail','desc','approved','datetime']
    

@admin.register(Lectures)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['id','course_id','user','lecture_name','video','desc']
    
