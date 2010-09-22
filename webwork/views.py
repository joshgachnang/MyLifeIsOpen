# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.conf import settings
from models import Post, PostForm
from datetime import datetime

def home(request):
    return HttpResponseRedirect('/home/1')
    
def about(request):
    return render_to_response('about.html')
    
def posts_page(request, page):
    minimum = (int(page) - 1) * settings.POSTS_PER_PAGE
    posts = Post.objects.order_by('created')[minimum:minimum + settings.POSTS_PER_PAGE]
    if len(posts) == 0:
        return HttpResponse("No posts..")
    return render_to_response('post.html', {'posts': posts})
    
def new_post(request):
    #Return form for new Post
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.created = datetime.now()
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
    return render_to_response('new_post.html', {'form': form})

def new_comment(request, post):
    #Return new comment form, pass Post object
    return render_to_response('new_comment.html', {'post': post})
def show_comments(request, post):
    #Return list of comments, pass Post object
    return render_to_response('comment_list.html', {'post': post})