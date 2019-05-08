# coding:utf-8

from  . import views
from django.conf.urls import url

urlpatterns = [
    # url(r'^$',views.mytest_jquery,name = 'mytest_jquery')
    url(r'^jquery/$',views.mytest_jquery),
    url(r'^table/$',views.mytest_table),
    url(r'^sel/$',views.mytest_table_select),
    url(r'^ht-select/$',views.mytest_ht_select,name = "ht_select"),
    url(r'^a/$',views.a,name = "a"),
    url(r'^keps-time/$',views.kepserver_time,name = "keps_time"),
    url(r'^keps-time-find-modify/$',views.kepserver_time_find_modify,name = "keps_time_find_modify"),
    url(r'^ht-view/$',views.ht_view,name = 'ht_view'),
    url(r'^test/$',views.test,name = 'test'),
    url(r'^new-keps-time/$',views.new_kepserver_time,name = "new_keps_time"),
    url(r'^modify-tpmis-kep-control',views.modify_tpmis_kep_control,name = "modify_tpmis_kep_control"),
    url(r'^del-tpmis-kep-control/$',views.del_tpmis_kep_control,name = 'del_tpmis_kep_control'),
    url(r'^pressure/$',views.pressure,name = 'pressure'),
    url(r'^pressure_get_info',views.pressure_get_info,name='pressure_get_info'),
    url(r'^vote/$',views.vote,name='vote'),
    url(r'^vote_chart/$',views.vote_chart,name='vote_chart'),
    url(r'^translate/$',views.translate,name='translate'),
    url(r'^model_test/$',views.model_test,name='model_test'),
    url(r'^translate_char/$',views.translate_char,name='translate_char'),
    url(r'^translate/chat/$',views.chat,name='chat')

    # url(r'^keps')
    # url(r'^show-data/$',views.show_data,name="show_data")


]