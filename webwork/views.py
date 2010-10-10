# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpRequest
from django.conf import settings
from models import Post, PostForm, Access
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime

def home(request):
    return HttpResponseRedirect('/home/1')
    
def about(request):
    return render_to_response('about.html', {'user': get_user(request)})
    
def posts_page(request, page):
    minimum = (int(page) - 1) * settings.POSTS_PER_PAGE
    posts = Post.objects.order_by('created')[minimum:minimum + settings.POSTS_PER_PAGE - 1]
    if len(posts) == 0:
        return HttpResponseRedirect('/new_post/')
    return render_to_response('post.html', {'posts': posts}, RequestContext(request))
    
def new_post(request):
    #Return form for new Post
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.created = datetime.datetime.now()
        post.likes = 0
        post.dislikes = 0
        if request.user.is_authenticated():
	  post.owner = request.user
	else:
	  post.owner = None
	if form.is_valid():
	    form.save()
	# Need to pass a message like "Thanks for making the world a geekier place!"
	return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render_to_response('new_post.html', {'form': form}, RequestContext(request))
    
@login_required
def show_comments(request, post_id):
    #Return list of comments, pass Post object
    post = Post.objects.get(id=post_id)
    return render_to_response('comment_list.html', {'post': post}, RequestContext(request))
    
def like_post(request, post_id):
    like_dislike(request, post_id, True)
    return HttpResponseRedirect('/') #Will use return value soon..
    
def dislike_post(request, post_id):
    like_dislike(request, post_id, False)
    return HttpResponseRedirect('/') #Will use return value soon..
    
def like_dislike(request, post_id, like):
    accesses = Access.objects.filter(ip=request.META.get('REMOTE_ADDR'))
    if len(accesses) != 0:
        for access in accesses:
	    if access.post_access.id == int(post_id):
	      return 1 #Need to modify to anchor
    post = Post.objects.get(id=post_id)
    if like == True:
      post.likes = post.likes + 1
    else:
      post.dislikes = post.dislikes + 1
    post.save()
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    a = Access(ip=ip, post_access=post)
    a.save()
    return 0 #Need to modify to anchor
