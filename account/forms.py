# coding:utf-8
from django import forms
#引入Django默认的用户模型User
from django.contrib.auth.models import User 
from .models import UserProfile,UserInfo

# 各種與表單有關的類
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

# 继承ModelForm和数据库有关，修改数据库
class RegistrationForm(forms.ModelForm):
    # 自帶username\password\email
    password = forms.CharField(label = "Password",widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Cofirm Password",widget = forms.PasswordInput)

    class Meta:
        # 決定將表單寫入到那個數據庫表中的那些記錄
        model = User
        # 說明選用的屬性（數據庫表中的字段）
        fields = ("username","email")

    def clean_password2(self):
        cd =self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("password do not match")
        return cd["password2"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone","birth")

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
