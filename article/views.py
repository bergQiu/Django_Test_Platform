# coding:utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import ArticleColumn,ArticlePost
from .forms import ArticleColumnForm,ArticlePostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger # 分頁用到的三種方法
# Create your views here.

@login_required(login_url = '/account/new-login/')
@csrf_exempt
def article_column(request):
    print(request.user)
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user = request.user)
        column_form = ArticleColumnForm()
        return render(request,'article/column/article_column.html',{'columns':columns,'column_form':column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        print column_name
        columns = ArticleColumn.objects.filter(user_id = request.user.id,column = column_name)
        if columns:
            return HttpResponse(2)
        else:
            ArticleColumn.objects.create(user = request.user,column = column_name)
            return HttpResponse(1)

@login_required(login_url = '/account/new-login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    column_name = request.POST["column_name"]
    print column_id
    print request.POST
    try:
        line = ArticleColumn.objects.get( column = column_name)
        # line = ArticleColumn.objects.get(column = )
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url = '/account/new-login/')
@csrf_exempt
@require_POST
def rename_article_column(request):
    print request.POST
    column_id = request.POST["column_id"]
    column_name = request.POST["column_name"]
    old_column_name= request.POST["old_name"]
    try:
        line = ArticleColumn.objects.get(column = old_column_name)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url = '/account/new-login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data = request.POST)
        # print(request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit = False)
                new_article.author =request.user
                new_article.column = request.user.article_column.get(id = request.POST['column_id'])
                new_article.save()
                return HttpResponse(1)
            except:
                return HttpResponse(2)
        else:
            return HttpResponse(3)
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        # print ({"article_post_form":article_post_form,"article_columns":article_columns}) 
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_columns":article_columns})
    
    
@login_required(login_url = '/account/new-login/')
def article_list(request):
    #################################
    # articles = ArticlePost.objects.filter(author = request.user)
    # # articles = request.user.article_column.filter()
    # # articles = ArticlePost.objects.all()
    # # print (articles)
    # return render(request,"article/column/article_list.html",{"articles":articles})
    #################################
    article_list = ArticlePost.objects.filter( author = request.user)
    paginator = Paginator(article_list,5)
    page = request.GET.get("page")
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,"article/column/article_list.html",{"articles":articles,"page":current_page})



@login_required(login_url = '/account/new-login/')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost, id = id,slug = slug)
    return render(request,"article/column/article_detail.html",{"article":article})

@login_required(login_url = '/account/new-login/')
def article_del(request):
    ID = request.POST.getlist('article_id')
    # print ID
    try:
        for i in ID:
            article = ArticlePost.objects.get(id = i)
            article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url = '/account/new-login/')
@csrf_exempt
def article_redit(request,article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id = article_id)
        this_article_form = ArticlePostForm(initial = {"title":article.title})
        this_article_column = article.column
        # print this_article_column
        # this_article_column = "Ajax"
        data = {
            "article":article,
            "article_columns":article_columns,
            "this_article_column":this_article_column,
            "this_article_form":this_article_form
            }
        # print data["article_columns"][2]
        return render(request,"article/column/article_redit.html",data)
    else:
        # print request.POST
        data = request.POST
        article_redit = ArticlePost.objects.get(id = article_id)
        try:
            article_redit.column = request.user.article_column.get(id = data['column_id'])
            article_redit.title = data['title']
            article_redit.body = data['body']
            article_redit.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")