from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()#表示正整数
    content_object = GenericForeignKey('content_type', 'object_id')
    #这个定义的就是具体的表实例化后的实例内容
    ##上面这三个，参数输入前两个就不用管第三个，参数输入第三个就不用管前两个
    text=models.TextField()
    comment_time=models.DateTimeField(auto_now_add=True)
    ##定义评论的用户
    user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    ##设计根评论,设置null允许次字段为空
    root=models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
    ##树结构中的上一层评论
    parent=models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)##自己关联到自己，允许为空
    ##定义反向关联的名字，定义要回复的用户
    reply_to=models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE)
    ##定义反向关联的名字,防止冲突

    def __str__(self):
        return self.text
    class Meta:
        ordering=['comment_time']
class Replay(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)