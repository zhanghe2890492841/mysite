from django.shortcuts import get_object_or_404,render
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count#C是大写
from read_statistics.utils import read_statistics_once_read

from mysite.forms import LoginForm
from django.contrib.contenttypes.models import ContentType
#from comment.models import Comment

#from comment.forms import CommentForm
#from datetime import datetime
def get_blog_list_common_date(request,blogs_all_list):
    page_num=request.GET.get("page",1)#获取url页码参数使用get请求
    paginator=Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) #每2篇进行分页
    page_of_blogs=paginator.get_page(page_num)#如果字符出错，自动返回1
    # 如果什么也没有也返回1
    # print（）可以在后台打印出想看的信息来
    ##显示页码范围
    current_page_num=page_of_blogs.number#获取当前页面
    #python3中range是个生成器,python2中range是个列表
    page_range=list(range(max(current_page_num-2,1),current_page_num))+\
               list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    
    # 添加省略号
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')

    #添加第一页和第最后页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)


    ##获取博客分类的对应数量
    ##使用一般的方法
    ''''blog_types=BlogType.objects.all()
    blog_type_list=[]
    for blog_type in blog_types:
        blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)'''
    ##使用python库来加入数量属性,最后解析成为一条数据库语言
    #BlogType.objects.annotate(blog_count=Count('blog_blog'))#由于Blog与BlogType关联，所以count统计的是，每一个Blogtype对应的Blog的个数
    
    ##获取日期归档对应的博客数量
    blog_dates=Blog.objects.dates('created_time','month',order="DESC")
    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count=Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count
    ##使用python库来加入数量属性,最后解析成为一条数据库语言    
    ##fiter中加入双下划线用于访问对象中的对象
    #blog_dates=Blog.objects.dates('created_time','month',order="DESC")
    #blog_dates.annotate(blog_count=Count('created_time'))
    context={}
    context['blogs']=page_of_blogs.object_list
    context['page_of_blogs']=page_of_blogs
    #context['blog_types']=blog_type_list
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog_blog'))#将每一个BlogType添加一条注释的属性
    context['page_range']=page_range
    context['blogs_count']=Blog.objects.all().count()
    context['blog_dates']=blog_dates_dict#倒序,仅显示月和年,筛选出来的是个日期属性


    return context
def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context=get_blog_list_common_date(request,blogs_all_list)
    return render(request,'blog/blog_list.html',context)
def blogs_with_type(request,blog_type_pk):
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    context=get_blog_list_common_date(request,blogs_all_list)
    context['blog_type']=blog_type
    return render(request,'blog/blogs_with_type.html',context)
def blogs_with_date(request,year,month):
    blogs_all_list=Blog.objects.filter(created_time__year=year,created_time__month=month)
    context=get_blog_list_common_date(request,blogs_all_list)
    context['blogs_with_date']='%s年%s月'% (year,month)
    return render(request,'blog/blogs_with_date.html',context)
def blog_detail(request,blog_pk):
    blog=get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key=read_statistics_once_read(request,blog)
    '''
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        ct=ContentType.objects.get_for_model(blog)
        if ReadNum.objects.filter(content_type=ct,object_id=blog.pk).count():
            readnum=ReadNum.objects.get(content_type=ct,object_id=blog.pk)
            #存在记录
        else:
            #不存在记录
            readnum=ReadNum(content_type=ct,object_id=blog.pk)
        #技术+1
        readnum.read_num+=1
        readnum.save()
    '''    
    ##如果已经打开过，即已经有cookie则不会加1
    #必须要存储下来，否则会出错,但是当这个字段更改的时候，最后更改日期也变换了
    #blog_content_type=ContentType.objects.get_for_model(blog)
    #comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None).order_by('-comment_time')
    
 

    context={}
    context['blog']=blog
    context['login_form']=LoginForm()
    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 使用__双下划线魔法方法来进行对属性筛选范围的锁定
    context['next_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()

    #context['user']=request.user 使用render的话，就直接有user
    #context['comments']=comments.order_by('-comment_time')[:7]#这里倒叙，但是在插入的是也是从后边插，所以显示就正了。
    ##需要先order_by再使用切片
    # data={}
    # data['content_type']=blog_content_type.model##将类型变为字符串
    # data['object_id']=blog_pk
    #context['comment_form']=CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk,'reply_comment_id':0})##要输入一个实例化的form对象，必须用initial不能直接
    #context['comment_count']=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk).count()
    response= render(request,'blog/blog_detail.html',context)##获得这个响应与请求是对应的
    response.set_cookie(read_cookie_key,'true')#阅读cookie标记
    #max_age=60,expires=datetime#让浏览器保存信息,cookie有个有效期，过了有效期，浏览器就不提交了
    # 主要有4个参数，字典键、字典键值、最大有效期单位为秒、指定一个时间（datetime类型）,这两个参数是冲突的，如果后两个都不写，表示浏览器结束cookie才失效
    ##返回評論的數量
    
    return response