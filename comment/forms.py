from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

from ckeditor.widgets import CKEditorWidget

from .models import Comment
class CommentForm(forms.Form):
    content_type=forms.CharField(widget=forms.HiddenInput)
    object_id=forms.IntegerField(widget=forms.HiddenInput)
    text=forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),error_messages={'required':'評論能容不能為空'})
    reply_comment_id=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs.keys():
            self.user=kwargs.pop('user')##不一定有这个参数可以使用，使用get方法
        super(CommentForm,self).__init__(*args,**kwargs)##会检查'user'关键字是否合法,要在这一步之前剔除掉

    ##字段验证
    def clean_reply_comment_id(self):
        reply_comment_id=self.cleaned_data['reply_comment_id']
        if reply_comment_id<0:
            raise form.ValidationError('回复出错')
        elif reply_comment_id==0:
            self.cleaned_data['parent']=None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent']=Comment.objects.get(pk=reply_comment_id)
        else:
            raise form.ValidationError('回复出错')
        return  reply_comment_id

    ##整体验证
    def clean(self):
        ##判斷用戶是否登陸
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用戶尚未登陸')
        #评论验证
        content_type=self.cleaned_data['content_type']
        object_id=self.cleaned_data['object_id']
        try:
            model_class=ContentType.objects.get(model=content_type).model_class()
            ##通过字符串，得到一个具体的ContentType类，通过model_class方法直接得到，次查询结果所对应的类表。
            model_obj=model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object']=model_obj
        except ObjectDoseNotExist:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data