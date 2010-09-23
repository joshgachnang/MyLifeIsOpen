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
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/change_password/$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/change_password_done/$', 'django.contrib.auth.views.password_change'),
)
urlpatterns += patterns('webwork.views',
    (r'^$', 'home'),
    (r'^home/(?P<page>\d+)/$', 'posts_page'),
    (r'^about/$', 'about'),
    (r'^new_post/$', 'new_post'),
    (r'^post/(?P<id>\d+)/$', 'single_post'),
    (r'^like/(?P<post_id>\d+)/$', 'like_post'),
    (r'^dislike/(?P<post_id>\d+)/$', 'dislike_post'),
    (r'^comment/(?P<post_id>\d+)/$', 'comment_post'),
    (r'^comment_like/(?P<post_id>\d+)/$', 'like_comment'),
    (r'^comment_dislike/(?P<post_id>\d+)/$', 'dislike_comment'),
)