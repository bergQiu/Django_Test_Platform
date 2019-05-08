#coding:utf-8
from django.shortcuts import render
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
# Create your views here.
# 基於類的視圖 

from django.views.generic import TemplateView,ListView
from .models import  Course

from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView,DeleteView
from django.shortcuts import redirect
from .forms import CreateCourseForm

from django.http import HttpResponse


class CourseListView(ListView):
    # queryset = Course.objects.filter(user=User.objects.filter(username='test3'))
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'


class UserMixin:
    # def get_queryset(self):
    #     qs = super(UserMixin,self).get_queryset()
    #     return qs.filter(user=self.request.user)
    def get_queryset(self):
        queryset = Course.objects.filter(user=self.request.user)
        return queryset
    # pass

class UserCourseMixin(UserMixin,LoginRequiredMixin):
    model = Course
    login_url = '/account/new-login/'

class ManageCourseListView(UserCourseMixin,ListView):
    # queryset = Course.objects.filter(user=self.requset.user)
    context_object_name = 'courses'
    template_name = 'course/manage/manage_course_list.html'


class CreateCourseView(UserCourseMixin,CreateView):
    fields = ['title','overview']
    template_name = 'course/manage/create_course.html'

    def post(self,request,*args,**kargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({'form':form})


class DeleteCourseView(UserCourseMixin,DeleteView):
    context_object_name = 'courses'
    template_name = 'course/manage/delete_course_confirm.html'#确认刪除模板的名稱
    success_url = reverse_lazy('course:manage_course')#刪除成功後的頁面URL

    # def dispatch(self,*args,**kargs):
    #     resp = super(DeleteCourseView,self).dispatch(*args,**kargs)
    #     if self.request.is_ajax():
    #         response_data = {"result":"OK"}
    #         return HttpResponse(json.dumps(response_data),content_type="application/json")
    #     else:
    #         return resp



