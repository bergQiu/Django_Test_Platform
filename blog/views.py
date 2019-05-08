# coding:utf-8
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
from django.template.response import TemplateResponse
# from django.views.decorators.http import require_POST
# Create your views here
from .models import BlogArticles

@login_required(login_url = "/account/new-login/")
def blog_title(request,template_name):# tmplate_name 接受傳來的模板參數
    blogs = BlogArticles.objects.all()# 得到所有的BlogArticles實例對象
    # return render(request,"blog/titles.html",{"blogs":blogs})
    # return render(request,"mytest/jquery.html")
    return TemplateResponse(request,template_name,{"blogs":blogs})#和render一樣的功效

@login_required(login_url = "/account/new-login/")
def blog_article(request,article_id):
    # blog = BlogArticles.objects.get(id = article_id)
    blog = get_object_or_404(BlogArticles, id = article_id)
    pub  = blog.publish
    return render(request,"blog/content.html",{"article":blog,"publish":pub})
