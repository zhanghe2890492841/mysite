from django.urls import path

##设置博客列表路由http://localhost:8000/blog/1
#设置主页http://localhost:8000

from .import views
#start with blog，默认其开始的时候是从blog\开始的
urlpatterns=[
#http://localhost:8000/blog/1
path('like_change',views.like_change,name='like_change')
]