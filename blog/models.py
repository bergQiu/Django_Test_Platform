# coding:utf-8
from __future__ import unicode_literals

from django.db import models
# Create your models here.
# 數據庫基本模型，代表數據存取層面

from django.utils import timezone
from django.contrib.auth.models import User

# 编好数据模型后，在MYSITE/manage.py 位置执行python manage.py makemigrations,完成在blog/migrations创建了BlogArticles模型
class BlogArticles(models.Model):
    # title的类型是Char，最长不超过300
    title = models.CharField(max_length = 300)
    # 规定文章和用户的关系，ForeignKey()反映了这种“一对多”的关系，类User就是BlogArticles的对应对象，related_name 允许通过类User反向查询到BlogArticles
    author = models.ForeignKey(User,related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)

    class Meta:
        # 规定BlogArticles实例对象的显示数据，按照publish的倒序显示,注意后面的逗号
        ordering = ('-publish',)

    def __str__(self):
        return self.title
