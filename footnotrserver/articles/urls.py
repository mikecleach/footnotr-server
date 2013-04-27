from django.conf.urls import patterns, include, url
from articles import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'footnotrserver.views.home', name='home'),
    # url(r'^footnotrserver/', include('footnotrserver.foo.urls')),
    url(r'^(?P<article_id>\d+)/$', views.article, name='article'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)