# -*- coding: utf-8 -*-
def mlio_settings(request):
    from django.conf import settings
    import time, datetime
    year = str(time.localtime().tm_year)
    stardate = year + '.' + str(time.localtime().tm_yday)
    return { 'media_url': settings.MEDIA_URL, 'like': settings.RENAME_LIKE_DISLIKE[0], \
    'dislike': settings.RENAME_LIKE_DISLIKE[1], 'google_analytics_key': \
    settings.GOOGLE_ANALYTICS_KEY, 'site_title': settings.SITE_TITLE, 'year': year, \
    'stardate': stardate }