from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone



class ReadNum(models.Model):
    read_num=models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()#表示正整数
    content_object = GenericForeignKey('content_type', 'object_id')#把以上两个组合起来变成一个通用的外键

##用于拓展模型计数功能的模块
class ReadNumExpandMethod():
    def get_read_num(self):
        ct=ContentType.objects.get_for_model(self)
        try:
            readnum=ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
class ReadDetail(models.Model):
    read_num=models.IntegerField(default=0)
    date=models.DateField(default=timezone.now)#只有天数没有具体的日期
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()#表示正整数
    # content_object = GenericForeignKey('content_type', 'object_id')#把以上两个组合起来变成一个通用的外键,通过
    # 这个可以直接得到对应的具体的模型
    content_object = GenericForeignKey('content_type', 'object_id')#把以上两个组合起来变成一个通用的外键