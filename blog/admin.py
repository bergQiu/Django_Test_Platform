# coding:utf-8
from django.contrib import admin
# 將BlogArticles引入到當前環境
from  .models import BlogArticles

class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ('title','author','publish')
    list_filter = ('publish','author')
    search_fields = ('title','body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    oridering = ['publish','author']
# 將該類註冊到admin中
admin.site.register(BlogArticles,BlogArticlesAdmin)
# admin.site.register(BlogArticles)

# Register your models here.