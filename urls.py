# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_reset, password_reset_done, password_change, password_change_done, logout
from django.http import HttpResponsePermanentRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^MyLifeIsOpen/', include('MyLifeIsOpen.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/profile/$', lambda request: HttpResponsePermanentRedirect('/home/1')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next': '/home/1/'}, name="auth_logout"),
    url(r'^logout/(?P<next_page>.*)/$', 'django.contrib.auth.views.logout', name='auth_logout_next'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
	  {'document_root': settings.STATIC_DOC_ROOT}),
)
urlpatterns += patterns('webwork.views',
    (r'^$', lambda request: HttpResponsePermanentRedirect('/home/1')),
    (r'^home/(?P<page>\d+)/$', 'posts_page'),
    (r'^about/$', 'about'),
    (r'^new_post/$', 'new_post'),
    (r'^post/(?P<post_id>\d+)/$', 'individual_post'),
    (r'^like/(?P<post_id>\d+)/$', 'like_dislike_post', {'like': True}),
    (r'^dislike/(?P<post_id>\d+)/$', 'like_dislike_post', {'like': False}),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^comments/(?P<post_id>\d+)/$', 'show_comments'),
    # Sort by likes, geekiest, etc etc
)