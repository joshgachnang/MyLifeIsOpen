# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.signals import comment_was_posted
from django.forms import ModelForm, Textarea


class Post(models.Model):
    content = models.CharField("How geeky is your life?", max_length=256)
    owner = models.ForeignKey(User, blank=True, null=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    created = models.DateTimeField()
    
    def __unicode__(self):
      if self.owner == None:
	  return 'Anon' + self.content[:15]
      else:
	  return self.owner.username + self.content[:15]
      
    class Meta:
        ordering = ['-created']
        
class PostForm(ModelForm):
    content = models.TextField(max_length=1000)
    
    class Meta:
	model = Post
	exclude = ('owner', 'likes', 'dislikes', 'created')
	widgets = { 'content': Textarea(attrs={'rows': 5})}
    
class Access(models.Model):
    ip = models.IPAddressField()
    post_access = models.ForeignKey(Post)
    
    def __unicode__(self):
      return self.ip

class ExtendedUser(models.Model):
    first_name = models.CharField(blank=True, max_length=60)
    last_name = models.CharField(blank=True, max_length=60)
    bio = models.CharField(blank=True, max_length=1000)
    total_likes = models.IntegerField(blank=True)
    total_dislikes = models.IntegerField(blank=True)
    avatar = models.URLField(blank=True)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
	return user.username
    
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    site_title = models.CharField(blank=True, max_length=100)
    site_short_title = models.CharField(blank=True, max_length=100)
    num_top_likes = models.IntegerField()
    num_top_dislikes = models.IntegerField()
    rename_like = models.CharField(max_length=20)
    rename_dislike = models.CharField(max_length=20)
    author = models.CharField(max_length=100)

    #Registration settings
    account_activation_days = models.IntegerField()
    email_host = models.CharField(max_length=100)
    email_host_user = models.CharField(max_length=100)
    email_host_password = models.CharField(max_length=128)
    email_port = models.IntegerField()
    
    google_analytic_key = models.CharField(blank=True, max_length=64)
    askismet_api_key = models.CharField(blank=True, max_length=64)
    
    #Amazon S3 settings
    aws_access_key_id = models.CharField(blank=True, max_length=32)
    aws_secret_access_key = models.CharField(blank=True, max_length=256)
    aws_bucket_name = models.CharField(blank=True, max_length=256)

    #Google Storage for Developers settings
    google_storage_secret = models.CharField(blank=True, max_length=40)
    google_storage_access_key = models.CharField(blank=True, max_length=20)
    google_storage_bucket_name = models.CharField(blank=True, max_length=256)

def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    # spam checking can be enabled/disabled per the comment's target Model
    # if comment.content_type.model_class() != Entry:
    #    return

    from django.contrib.sites.models import Site
    from django.conf import settings

    try:
        from akismet import Akismet
    except:
        return

    ak = Akismet(
        key=settings.AKISMET_API_KEY,
        blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
    )

    if ak.verify_key():
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'comment_type': 'comment',
            'comment_author': comment.user_name.encode('utf-8'),
        }

        if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
            comment.flags.create(
                user=comment.content_object.author,
                flag='spam'
            )
            comment.is_public = False
            comment.save()

comment_was_posted.connect(on_comment_was_posted)