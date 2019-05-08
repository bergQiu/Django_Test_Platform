#-*- coding:utf-8 -*-
from django.contrib import admin
# 將BlogArticles引入到當前環境
from .models import UserProfile,UserInfo

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","birth","phone")
    list_filter = ("phone",)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("school","company","profession","address","aboutme","photo")
    list_filter = ("school","company","profession")

# 將該類註冊到後端admin中
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserInfo,UserInfoAdmin)
