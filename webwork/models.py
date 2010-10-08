# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.signals import comment_was_posted
from django.forms import ModelForm, Textarea


class Post(models.Model):
    content = models.CharField("How geeky is your life?", max_length=1000)
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
        ordering = ['created']
        
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