from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail
from django.contrib.contenttypes.fields import GenericRelation

class BlogType(models.Model):
    type_name=models.CharField(max_length=15)
    def __str__(self):
        return self.type_name
    # 保证在后台界面可以显示
class Blog(models.Model,ReadNumExpandMethod):
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(BlogType,on_delete=models.CASCADE,related_name='blog_blog')
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    #readed_num=models.IntegerField(default=0)##数值字段
    created_time=models.DateTimeField(auto_now_add=True)
    read_details=GenericRelation(ReadDetail)#ReadDetail为包含contenttypes字段的模型，建立反向关联。
    ##通过这个可以得到与具体blog相关联的通过定义contenttype字段的模型实例的具体情况
    last_updataed_time=models.DateTimeField(auto_now=True)
    #这其实都是描述符函数来描述

    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except Exception as e:
            return 0
    '''
    ##使用公共模型
    '''
    def get_read_num(self):
        ct=ContentType.objects.get_for_model(self)
        try:
            readnum=ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    '''
    #模型表中需要有函数
    #把这个内容写成一个方法，这样可以在admin中那个对应修饰对象中直接用字符串访问。
    
    #self.read_num=self.readnum.read_num
    #把这个内容直接写成一个属性是不可以的，self不能直接这样用
    def __str__(self):
        return "<Blog:%s>" % self.title
    class Meta:
        ordering=['-created_time']
        # 根据创建时间倒序，主义这个类要放在模型类下边。
#为了方便建立公共APP，方便其他APP调用

'''
class ReadNum(models.Model):
    read_num=models.IntegerField(default=0)
    blog=models.OneToOneField(Blog,on_delete=models.CASCADE)
    def __str__(self):
        return "<Blog_readnum:%s>" % self.blog.title
'''



