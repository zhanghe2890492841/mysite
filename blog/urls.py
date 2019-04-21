from django.urls import path

##设置博客列表路由http://localhost:8000/blog/1
#设置主页http://localhost:8000

from .import views
#start with blog，默认其开始的时候是从blog\开始的
urlpatterns=[
#http://localhost:8000/blog/1
path('',views.blog_list,name='blog_list'),
path('<int:blog_pk>',views.blog_detail,name="blog_detail"),
path('type/<int:blog_type_pk>',views.blogs_with_type,name="blogs_with_type"),
path('date/<int:year>/<int:month>',views.blogs_with_date,name='blogs_with_date'),
##匹配是要注意优先级别的，第一个如果匹配成功就不会查看后边的了,所以为了不混淆，则需要再加一个\type的前缀
]