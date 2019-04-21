"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
##from blog.views import blog_list
from django.conf import settings
from django.conf.urls.static import static
from .import views


#设置总路由
urlpatterns = [
    path('admin/',admin.site.urls),
    path('blog/',include('blog.urls')),
    path('',views.home,name='home'),#因为是首页所以给了一个home
    path('comment/',include('comment.urls')),
    path('likes/',include('likes.urls')),#不仅APP中要有子路径，在总的路由里面也要有哦
    path('ckeditor',include('ckeditor_uploader.urls')),#名字库里面定好的不要修改#
    path('login/',views.login,name='login'),
    path('login_for_medal/',views.login_for_medal,name='login_for_medal'),
    path('register/',views.register,name='register'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#使用url静态访问服务器文件夹下的文件，保存上传的文件
