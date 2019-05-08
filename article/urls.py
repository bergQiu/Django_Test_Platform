from django.conf.urls import url
from . import views,list_views

urlpatterns = [
    url(r'^article-column/$',views.article_column,name = 'article_column'),
    url(r'^dle-column/$',views.del_article_column,name = 'del_article_column'),
    url(r'^rename-column/$',views.rename_article_column,name = 'rename_article_column'),
    url(r'^article-post/$',views.article_post,name = "article_post"),
    url(r'^article-list/$',views.article_list,name = "article_list"),
    url(r'^article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.article_detail,name = "article_detail"),
    url(r'^article-del/$',views.article_del,name = "article_del"),
    url(r'^article-redit/(?P<article_id>\d+)/$',views.article_redit,name = "article_redit"),
    url(r'^list-article-titles/$',list_views.article_titles,name = 'list_article_titles'),
    url(r'^list-article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',list_views.article_detail,name = "list_article_detail"),
    url(r'^list-article-titles/(?P<username>[-\w]+)$',list_views.article_titles,name = 'author_articles'),
    url(r'^like-article/$',list_views.like_article,name = "like_article"),
    url(r'^list-article-titles-filter/$',list_views.article_titles_filter,name ="article_filter"),
    url(r'^list-del-comment/$',list_views.del_comment,name="article_del_comment")
]