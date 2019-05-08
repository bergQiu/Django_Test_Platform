from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list-images/$',views.list_images,name = 'list_images'),
    url(r'^upload-image/$',views.upload_image,name = 'upload_image'),
    url(r'^delete-image/$',views.del_image,name='delete_image'),
    url(r'^images/$',views.falls_images,name='falls_images')
]