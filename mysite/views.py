from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse

from django.http import JsonResponse

from django.contrib.auth.models import User


from .forms import LoginForm,RegForm
def get_7_days_hot_blogs():
    today=timezone.now().date()
    date=today-datetime.timedelta(days=7)
    blogs=Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date)\
    .values('id','title')\
    .annotate(read_num_sum=Sum('read_details__read_num'))\
    .order_by('-read_num_sum')
    return blogs[:7]
def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    dates,read_nums=get_seven_days_read_data(blog_content_type)

    #获取7天热门博客的缓存数据
    hot_data_for_7_days=cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days=get_7_days_hot_blogs()
        cache.set('hot_data_for_7_days',hot_data_for_7_days,3600)#3600秒之后就删除了

    context={}
    context['read_nums']=read_nums
    context['dates']=dates
    context['today_hot_data']=get_today_hot_data(blog_content_type)
    context['yesterday_hot_data']=get_yesterday_hot_data(blog_content_type)
    context['hot_data_for_7_days']=hot_data_for_7_days
    return render(request,'home.html',context)
    from .form import LoginForm,RegForm
    ##用戶登陸
def login(request):
    '''
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(request,username=username,password=password)
    referer=request.META.get('HTTP_REFERER',reverse('home'))#获取进来时候的路径
    #用reverse函数，来将别名给解析成地址
    if user is not None:
        auth.login(request,user)
        return redirect(referer)#重新定向一個頁面
    else:
        return render(request,'error.html',{'message':'用戶名或密碼不正確'})
    '''
    ##使用form的原始版本
    '''
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():#使用这个方法，过程中调用clean函数调用form类中的clean函数，返回一个.cleaned_data数据
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            ##cleaned_data表示有一个干净的数据
            user=auth.authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect(request.GET.get('form',reverse('home')))#重新定向一個頁面
            else:
                login_form.add_error(None,'用户名或密码不正确')
    else:
        login_form=LoginForm()
    context={}
    context['login_form']=login_form
    return render(request,'login.html',context)
    '''
    ##使用form类的终极版本
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():#使用这个方法，过程中调用了form类中的clean函数，返回值是固定的返回一个.cleaned_data数据
            user=login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('form',reverse('home')))#重新定向一個頁面
    else:
        login_form=LoginForm()
    context={}
    context['login_form']=login_form
    return render(request,'login.html',context)
def login_for_medal(request):
    data={}
    login_form=LoginForm(request.POST)
    if login_form.is_valid():#使用这个方法，过程中调用了form类中的clean函数，返回值是固定的返回一个.cleaned_data数据
        user=login_form.cleaned_data['user']
        auth.login(request,user)
        data['status']='SUCCESS'
    else:
        data['status']='ERROR'
    return JsonResponse(data) 
def register(request):
    if request.method=='POST':
        reg_form=RegForm(request.POST)##实例化的可以使用request传过来的
        if reg_form.is_valid():#使用这个方法，过程中调用了form类中的clean函数，返回值是固定的返回一个.cleaned_data数据
            username=reg_form.cleaned_data['username']
            email=reg_form.cleaned_data['email']
            password=reg_form.cleaned_data['password']
            user=User.objects.create_user(username,email,password)
            user.save()
            
            '''user.User()
            user.name=username
            user.email=email
            user.set_password(password)'''##set_password这个保存加密后的密码
            user=auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('form',reverse('home')))#重新定向一個頁面
    else:
        reg_form=RegForm()
    context={}
    context['reg_form']=reg_form
    return render(request,'register.html',context)
