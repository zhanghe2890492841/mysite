import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct=ContentType.objects.get_for_model(obj)#使用类名和实例名都可以Blog，blog
    key="%s_%s_read" % (ct.model,obj.pk)


    if not request.COOKIES.get(key):
    #     if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
    #         readnum=ReadNum.objects.get(content_type=ct,object_id=obj.pk)
    #         #存在记录
    #     else:
    #         #不存在记录
    #         readnum=ReadNum(content_type=ct,object_id=obj.pk)
        #总阅读数加1
        readnum,created=ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)#如果找不到回创建
        
        #技术+1
        readnum.read_num+=1
        readnum.save()

        #统计当天的明细记录
        #当天阅读数加1
        date=timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=date).count():
        #     readDetail=ReadDetail.objects.get(content_type=ct,object_id=obj.pk,date=date)
        # else:
        #     readDetail=ReadDetail(content_type=ct,object_id=obj.pk,date=date)
        readDetail,created=ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        #如果属于创建的则created是True，#如果不属于创建的则created是false
        readDetail.read_num+=1
        readDetail.save()
    return key


def get_seven_days_read_data(content_type):
    today=timezone.now().date()
    # 取到前七天的时间
    read_nums=[]
    dates=[]
    for i in range(7,0,-1):
        date=today-datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details=ReadDetail.objects.filter(content_type=content_type,date=date)
        result=read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)#0 none false 用or都得0
    return dates,read_nums

def get_today_hot_data(content_type):
    today=timezone.now().date()
    read_details=ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_details[:7]
def get_yesterday_hot_data(content_type):
    today=timezone.now().date()
    yesterday=today-datetime.timedelta(days=1)
    read_details=ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return read_details[:7]
