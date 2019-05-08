#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# 表示對應這在數據庫中建立account_userprofile的數據庫表  （應用名稱+數據模型名稱）
class UserProfile(models.Model):
    # 定義了名為user的字段，OneToOneFile代表通過user這個字段，申明UserProfile類與user類的關係是一對一
    user = models.OneToOneField(User,unique = True)
    birth = models.DateField(blank = True,null = True)
    phone = models.CharField(max_length = 20 ,null = True)

    def __str__(self):
        return "user {}".format(self.user.username)

class UserInfo(models.Model):
    user = models.OneToOneField(User,unique = True )
    school = models.CharField(max_length = 100 ,blank = True)
    company = models.CharField(max_length = 100 ,blank = True)
    profession = models.CharField(max_length = 100 ,blank = True)
    address = models.CharField(max_length = 100 ,blank = True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank = True)

    def __str__(self):
        return "user {}".format(self.user.username)