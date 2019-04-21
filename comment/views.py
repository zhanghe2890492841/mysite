from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
def update_comment(request):

    ##不用djangoform
    '''
    referer=request.META.get('HTTP_REFERER',reverse('home'))#获取进来时候的路径
    #用reverse函数，来将别名给解析成地址

    ##數據檢查
    if request.user.is_authenticated is False:
        return  render(request,'error.html',{'message':'用戶未登錄','redirect_to':referer})
    text=request.POST.get('text','').strip()
    if text == '':
        return  render(request,'error.html',{'message':'評論内容為空','redirect_to':referer})
    try:
        content_type=request.POST.get('content_type','')
        object_id=int(request.POST.get('object_id',''))
        model_class=ContentType.objects.get(model=content_type).model_class()
        #传入模型名称的字符串model,而get_for_model函数则传入的是Blog或者具体的实例
        #此处返回的是一个ContentType的查询结果，但是如果再使用
        #.model_class函数则返回的是大写的Blog的这个模型的类即表
        #这样就可以对Blog进行操作了
        model_obj=model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request,'error.html',{'message':'評論對象不存在','redirect_to':referer})

    ##檢查通過，保存數據
    comment=Comment()
    comment.user=request.user
    comment.text=text
    comment.content_object=model_obj
    comment.save()

    return redirect(referer)
    '''
    #使用dajango form优化
    referer=request.META.get('HTTP_REFERER',reverse('home'))#获取进来时候的路径
    #用reverse函数，来将别名给解析成地址
    comment_form=CommentForm(request.POST,user=request.user)##使用关键字传参数
    data={}
    if comment_form.is_valid():
            ##檢查通過，保存數據
            comment=Comment()
            comment.user=comment_form.cleaned_data['user']
            comment.text=comment_form.cleaned_data['text']
            comment.content_object=comment_form.cleaned_data['content_object']
            parent=comment_form.cleaned_data['parent']
            if not parent is None:
                comment.root=parent.root if not parent.root is None else parent
                comment.parent=parent
                comment.reply_to=parent.user
            comment.save()

            ##返回數據
            data['status']='SUCCESS'
            data['username']=comment.user.username
            # data['comment_time']=comment.comment_time.strftime('%y-%m-%d %H:%M:%S')##日期對象轉換為字符串,但是轉換過程中會將時區信息給除掉
            data['comment_time']=comment.comment_time.timestamp()
            data['text']=comment.text
            data['content_type']=ContentType.objects.get_for_model(comment).model
            if not parent is None:
                data['reply_to']=comment.reply_to.username
            else:
                 data['reply_to']=''
            data['pk']=str(comment.pk)
            data['root_pk']=str(comment.root.pk) if not comment.root is None else ''
            # return redirect(referer)
    else:
            data['status']='ERROR'
            data['message']=list(comment_form.errors.values())[0][0]
    return JsonResponse(data)##這個可以返回JSON到前端模板頁面
        # ender(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
# Create your views here.表單有兩類數據信息，一類是字段的錯誤信息，一類是整體字段的信息
#整體錯誤信息沒有登陸、評論内容沒有、評論對象不存在

