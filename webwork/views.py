# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpRequest, HttpResponseBadRequest
from django.conf import settings
from django.utils import simplejson
from models import Post, PostForm, Access
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime

def short_render(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    template = args[0]
    template = 'mobile_' + template
    if req.is_mobile: 
      if len(args) > 1:
	return render_to_response(template, args[1], **kwargs)
      else:
	return render_to_response(template, **kwargs)
    else:
      return render_to_response(*args, **kwargs)

def about(request):
    return short_render(request, 'about.html')
    #return render_to_response('about.html', {}, RequestContext(request))
    
def posts_page(request, page):

    intpage = int(page)
    minimum = (intpage - 1) * settings.POSTS_PER_PAGE
    t = Post.objects.all().count()
    if t <= settings.POSTS_PER_PAGE:
	total_pages = 1
    else:
	total_pages = (t / settings.POSTS_PER_PAGE) + 1
    posts = Post.objects.order_by('-created')[minimum:minimum + settings.POSTS_PER_PAGE - 1]
    if len(posts) == 0:
	if total_pages != 0:
	  return HttpResponseRedirect('/home/1')
	else:
	  return HttpResponseRedirect('/new_post/')
    if intpage > total_pages:
	return HttpResponseRedirect('/home/1')
    prev = intpage - 1
    if intpage == total_pages:
	next_page = 0
    else:
	next_page = intpage + 1
	
    if total_pages == 1:
	page_list = [1]
    elif total_pages == 2:
	page_list = [1,2]
    elif total_pages == 3:
	page_list = [1,2,3]
    elif total_pages == 4:
	page_list = [1,2,3,4]
    elif intpage == 1 :
	page_list = [1,2,3,4,5]
    elif intpage == total_pages:
	page_list = (intpage - 4, intpage - 3, intpage - 2, intpage - 1, intpage)
    elif total_pages - 1 == intpage:
	page_list = (intpage - 3, intpage - 2, intpage - 1, intpage, intpage + 1)
    else:
	page_list = (intpage - 2, intpage - 1, intpage, intpage + 1, intpage + 2)
    
    return short_render(request, 'post.html', {'posts': posts, 'prev': prev, 'next': next_page, 'last_page': total_pages, 'page_list': page_list, 'twitter_template': 'templates: { twitter: "{{url}}" }'})
    
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
    return short_render(request, 'new_post.html', {'form': form})
    
def show_comments(request, post_id):
    #Return list of comments, pass Post object
    post = Post.objects.get(id=post_id)
    return short_render(request, 'comment_list.html', {'post': post, 'next': '/comments/' + str(post.id)})
    #return render_to_response('comment_list.html', {'post': post, 'next': '/comments/' + str(post.id)}, RequestContext(request))
    
def individual_post(request, post_id):
    #Return list of comments, pass Post object
    post = Post.objects.get(id=post_id)
    return short_render(request, 'individual_post.html', {'post': post})
    #return render_to_response('individual_post.html', {'post': post}, RequestContext(request))

def best(request):
    posts = Post.objects.order_by('-likes')[0:24]
    return short_render(request, 'best_worst.html', {'posts': posts})
    #return render_to_response('best_worst.html', {'posts': posts}, RequestContext(request))
    
def worst(request):
    posts = Post.objects.order_by('-dislikes')[0:24]
    return short_render(request, 'best_worst.html', {'posts': posts})
    #return render_to_response('best_worst.html', {'posts': posts}, RequestContext(request))

def like_dislike_post(request, post_id, like):
    accesses = Access.objects.filter(ip=request.META.get('REMOTE_ADDR'))
    if len(accesses) != 0:
        for access in accesses:
	    if access.post_access.id == int(post_id):
	      return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/home/1')) #Need to modify to anchor
    post = Post.objects.get(id=post_id)
    if like == True:
      post.likes = post.likes + 1
    else:
      post.dislikes = post.dislikes + 1
    post.save()
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    a = Access(ip=ip, post_access=post)
    a.save()
    return HttpResponseRedirect('/#' + str(post.id))
    
#Ajax update like/dislike. Right now only works through Ajax and via GET. Returns JSON.
def post_like(request):
    
    #Make sure request is following our Ajax and GET rules.
    if not request.is_ajax():
	return HttpResponseBadRequest
    if not request.method == u'GET':
	return HttpResponseBadRequest
    
    results = {'success':False}
    GET = request.GET
    if GET.has_key(u'post_id') and GET.has_key(u'like_dis'):
	post_id = int(GET[u'post_id'])
	
	like = GET[u'like_dis']
	post = Post.objects.get(id=post_id)
	accesses = Access.objects.filter(ip=request.META.get('REMOTE_ADDR'))
	#This should be handled via cookie..
	if len(accesses) != 0:
	    for access in accesses:
		if access.post_access.id == int(post_id):
		  #Change to return blank JSON, or same?
		  json = simplejson.dumps(results)
		  return HttpResponse(json, mimetype="application/json") #Need to modify to anchor
	
	if like == u"like":
	    post.likes = post.likes + 1
	elif like == u"dislike":
	    post.dislikes = post.dislikes + 1
	post.save()
	results = {'success':True, 'likes':post.likes, 'dislikes':post.dislikes}
	
	#Save access
	ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
	a = Access(ip=ip, post_access=post)
	a.save()
	
    
    json = simplejson.dumps(results)
    
    return HttpResponse(json, mimetype="application/json")