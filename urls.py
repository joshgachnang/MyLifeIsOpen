# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^MyLifeIsOpen/', include('MyLifeIsOpen.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('webwork.views',
    (r'^$', 'home'),
    (r'^home/(?P<page>\d+)/$', 'posts_page'),
    (r'^about/$', 'about'),
    (r'^new_post/$', 'new_post'),
    (r'^post/(?P<id>\d+)/$', 'single_post'),
    (r'^like/(?P<id>\d+)/$', 'like_post'),
    (r'^dislike/(?P<id>\d+)/$', 'dislike_post'),
    (r'^comment/(?P<id>\d+)/$', 'comment_post'),
)