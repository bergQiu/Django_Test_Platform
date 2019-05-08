# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from  django.contrib.auth import authenticate,login
from .forms import LoginForm
from .forms import RegistrationForm,UserProfileForm,UserInfoForm,UserForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,UserInfo
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# from django.core.urlresolves import reverse
from django.core.urlresolvers import reverse

# Create your views here.

def user_login(request):
    # Django 创建包含请求数据的HttpRequest对象，并以参数request传给视图函数
    # print(request.path)
    # print(request.GET)
    # print(request.POST)
    # print(request.user.is_anonymous())
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 判斷表格是否合法
        if login_form.is_valid():
            # 引用的是字典類數據，以鍵值對的形式記錄用戶名和密碼
            cd = login_form.cleaned_data
            user = authenticate(username = cd['username'],password = cd['password'])
            if user:
                login(request,user)
                # HttpResponse是视图向客户端返回的对象
                return HttpResponse('wellcome you, nice job')
            else:
                return HttpResponse('sorry, your username or password is not riight')
        else:
            return HttpResponse('Invalid login')

    if request.method == 'GET':
        login_form = LoginForm()
        return render(request,'account/login.html',{'form':login_form})

def register(request):
    # print (request.POST)
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            new_profile = userprofile_form.save(commit = False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user = new_user)
            # return HttpResponse("Successfully")
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("sorry,you can not register")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        print(user_form)
        return render(request,"account/register.html",{"form":user_form,"profile":userprofile_form})

# Django  自帶的裝飾器，判斷用戶是否登錄，並將未登錄的用戶轉到指定頁面 /account/new-login        
@login_required(login_url = '/account/new-login/')    
def myself(request,template_name):
    # print("*****************nice")    
    user = User.objects.get(username = request.user.username)
    # print(user)
    userprofile = UserProfile.objects.get(user = user )
    userinfo = UserInfo.objects.get(user = user )
    # print(user)
    # print(userprofile)
    # print(userinfo.photo)
    return render(request,template_name,{"user":user,"userprofile":userprofile,"userinfo":userinfo})

@login_required(login_url = '/account/new-login/')
def edit_myself_information(request):
    user = User.objects.get(username = request.user.username)
    userprofile = UserProfile.objects.get(user = user)
    userinfo = UserInfo.objects.get(user = user)
    # print(userinfo)

    if request.method =="POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid()*userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd ['birth']
            userprofile.phone = userprofile_cd ['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/myself')
    else:
        user_form = UserForm(instance = request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={
            "school":userinfo.school,
            "company":userinfo.company,
            "address":userinfo.address,
            "aboutme":userinfo.aboutme,
            "profession":userinfo.profession,
            })
        return render(request,"account/myself_edit.html",{"user_form":user_form,"userprofile_form":userprofile_form,"userinfo_form":userinfo_form,"userinfo_img":userinfo.photo})


@login_required(login_url = "/account/new-login")
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user = request.user.id)
        userinfo.photo = img
        userinfo.save()
        # print("hello")
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',)