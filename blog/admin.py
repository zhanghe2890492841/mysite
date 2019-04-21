from django.contrib import admin
from .models import BlogType,Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display=('id','type_name')
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('title','id','get_read_num','content','author','created_time','last_updataed_time')#这个readnum是通过dir在blog对象中查找出来的

'''
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display=('read_num','blog')
'''
