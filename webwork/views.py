# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpRequest
from django.conf import settings
from models import Post, PostForm, Access
from datetime import datetime
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponseRedirect('/home/1')
    
def about(request):
    return render_to_response('about.html', {'user': get_user(request)})
    
def posts_page(request, page):
    minimum = (int(page) - 1) * settings.POSTS_PER_PAGE
    posts = Post.objects.order_by('created')[minimum:minimum + settings.POSTS_PER_PAGE]
    if len(posts) == 0:
        return HttpResponse("No posts..")
    if settings.RENAME_LIKE:
	print settings.RENAME_LIKE
	like = settings.RENAME_LIKE
    else:
	like = 'like'
    if settings.RENAME_DISLIKE:
	dislike = settings.RENAME_DISLIKE
    else:
	dislike = 'dislike'
    return render_to_response('post.html', {'posts': posts, 'like': like, 'dislike': dislike, 'user': get_user(request)})
    
def new_post(request):
    #Return form for new Post
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.created = datetime.now()
        post.likes = 0
        post.dislikes = 0
        post.owner = get_user(request)
	if form.is_valid():
	    form.save()
	# Need to pass a message like "Thanks for making the world a geekier place!"
	return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render_to_response('new_post.html', {'form': form, 'user': get_user(request)})

@login_required
def new_comment(request, post_id):
    #Return new comment form, pass Post object
    post = Post.objects.get(id=post_id)
    return render_to_response('new_comment.html', {'post': post})
    
def show_comments(request, post_id):
    #Return list of comments, pass Post object
    post = Post.objects.get(id=post_id)
    return render_to_response('comment_list.html', {'post': post})
    
def like_post(request, post_id):
    like_dislike(request, post_id, True)
    return HttpResponseRedirect('/') #Will use return value soon..
    
def dislike_post(request, post_id):
    like_dislike(request, post_id, False)
    return HttpResponseRedirect('/') #Will use return value soon..
    
def like_comment(request, comment_id):
    pass
def dislike_comment(request, comment_id):
    pass
  
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

def like_dislike_comment(comment_id, like):
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

def get_user(request):
    if request.user.is_authenticated:
	return request.user
    else:
	return None
  
def single_post(request):
    pass