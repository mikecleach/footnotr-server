from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from articles import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('articles.views',
    url(r'^articles/$', views.ArticleList.as_view(), name='article-list'),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^annotations/$', views.AnnotationList.as_view(), name='annotation-list'),
    url(r'^annotations/(?P<pk>[0-9]+)/$', views.AnnotationDetail.as_view(), name='annotation-detail'),
    url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    #this is for access to old api, until new one is completed
    url(r'^oldarticles/(?P<article_id>\d+)/$', views.article, name='article'),   
    #url(r'^articles/$', views.ArticleList.as_view(), name='articlelist'),
    #url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view(), name='article-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)