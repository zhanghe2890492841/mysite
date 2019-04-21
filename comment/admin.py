from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('id','content_type','content_object','object_id','text','comment_time','user','parent','root')
# Register your models here.
