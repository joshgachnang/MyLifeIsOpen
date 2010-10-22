# -*- coding: utf-8 -*-z
from webwork.models import Post
def getTopLikes(num):
    return Post.objects.order_by('-likes')[0:num]
def getTopDislikes(num):
    return Post.objects.all().order_by('-dislikes')[0:num]
  

def mlio_settings(request):
    from django.conf import settings
    import time, datetime
    year = str(time.localtime().tm_year)
    stardate = year + '.' + str(time.localtime().tm_yday)
    return { 'media_url': settings.MEDIA_URL, 'like': settings.RENAME_LIKE_DISLIKE[0], \
    'dislike': settings.RENAME_LIKE_DISLIKE[1], 'google_analytics_key': \
    settings.GOOGLE_ANALYTICS_KEY, 'site_title': settings.SITE_TITLE, 'site_url': settings.SITE_URL, 'year': year, \
    'stardate': stardate, 'top_likes': getTopLikes(settings.TOP_LIKES), 'top_dislikes': getTopDislikes(settings.TOP_DISLIKES), }
    
