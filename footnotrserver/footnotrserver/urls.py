from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from articles import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
    

urlpatterns = patterns('articles.views',
    url(r'^articles/$', views.ArticleList.as_view(), name='article-list'),
    url(r'^articles/new$', views.ArticleAdd.as_view(), name='article-add'),
    url(r'^articles/(?P<guid>[A-Za-z0-9]+)/$', views.ArticleDetail.as_view(), name='article-detail'),
    url(r'^annotations/$', views.AnnotationList.as_view(), name='annotation-list'),
    url(r'^annotations/new$', views.AnnotationAdd.as_view(), name='annotation-add'),
    url(r'^annotations/(?P<pk>[0-9]+)/$', views.AnnotationDetail.as_view(), name='annotation-detail'),
    url(r'^comments/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^comments/new$', views.CommentAdd.as_view(), name='comment-add'),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^votes/$', views.VoteList.as_view(), name='vote-list'),
    url(r'^votes/new$', views.VoteAdd.as_view(), name='vote-add'),
    url(r'^votes/(?P<pk>[0-9]+)/$', views.VoteDetail.as_view(), name='vote-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),name='user-detail'),
    #this is for access to old api, until new one is completed
    url(r'^oldarticles/(?P<article_id>\d+)/$', views.article, name='article'),

    url(r'^user-comments/(?P<pk>[0-9]+)/$', views.user_comment_list, name='user-comment-list'),
    url(r'^user-comments/(?P<username>[A-Za-z0-9]+)/$', views.user_comment_list_by_name, name='user-comment-list'),
    url(r'^latest-users/$', views.latest_comment_list, name='latest-comment-list'),

    #url(r'^articles/$', views.ArticleList.as_view(), name='articlelist'),
    #url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view(), name='article-detail'),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)