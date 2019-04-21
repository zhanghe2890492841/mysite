from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount,LikeRecord

register=template.Library()
##創建注冊的函數庫
@register.simple_tag
def get_like_count(obj):
    content_type=ContentType.objects.get_for_model(obj)
    like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
    return like_count.liked_num

@register.simple_tag(takes_context=True)##可以获取当前页面中context中变量信息，当然也可以直接user传入
def get_like_status(context,obj):
    content_type=ContentType.objects.get_for_model(obj)
    user=context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type,object_id=obj.pk,user=context['user']).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type=ContentType.objects.get_for_model(obj)
    return content_type.model
    
