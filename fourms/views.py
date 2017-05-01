from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Fourms, category, forumPost, create_forum_slug, create_post_slug
from .forms import createform, createpostform
# Create your views here.


def forumView(request,username, sortby=None):
	forum = Fourms.objects.all().order_by("-created")
	all_category = category.objects.all()
	paginator = Paginator(forum, 10)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		'forums':queryset,
		'category':all_category,

	}
	if request.POST:
		title = request.POST['title']
		description = request.POST['description']
		cat = request.POST['category']
		c = category.objects.get(name = cat)
		f = Fourms.objects.create(title=title, description = description,category = c, slug=slugify(title))
		f.slug = create_forum_slug(f)
		file=request.POST['file']
		f.file= file
		f.subscriber.add(request.user)
		f.save()
		messages.success(request, 'Forum Created Succesfully successfully', extra_tags='html_safe')
		return HttpResponseRedirect('/%s/forum/'%request.user.username)


	if sortby is not None:
		sort = Fourms.objects.filter(category = category.objects.get(name=sortby)) 
		print(sort)
		context.update({'forums':sort,'sort':sortby})
	
	return render(request, "forum_view.html", context)


def editForum(request, username, slug=None):
	instance = Fourms.objects.get(slug=slug)
	form = createform(request.POST or None, instance = instance)
	context = {'form':form}
	if form.is_valid():
		instance = form.save(commit=False)
		instance.slug = create_forum_slug(instance)
		if request.POST['file']:
			instance.file=request.POST['file']
		instance.save()
		return HttpResponseRedirect('/%s/forumfull/%s'%(request.user.username,instance.slug))

	return render(request, "forum_edit.html", context)

def deleteForum(request, username, slug):
	forum = Fourms.objects.get(slug=slug)
	forum.delete()


	return HttpResponseRedirect('/%s/forum/'%(request.user.username))

def fullForum(request, username, slug):
	forum = Fourms.objects.get(slug=slug)
	posts = forumPost.objects.filter(forum = forum).order_by("-timestamp")
	paginator = Paginator(posts, 5)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	form = createpostform(request.POST or None)
	sub = forum.subscriber.all()
	l=[]
	for s in sub:
		l.append(s.username)
	print(l)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user = request.user
		instance.slug= create_post_slug(instance)
		instance.forum = forum
		if request.POST['file']:
			instance.file = request.POST['file']

		instance.save()
		return HttpResponseRedirect('/%s/forumfull/%s'%(request.user.username,forum.slug))

	context = {
		'forum':forum,
		'posts':queryset,
		'form':form,
		'list':l,

	}
	if str(request.user.username).strip() == str(forum.creator).strip():
		context.update({'author':True})
	

	return render(request, "forum_full.html", context)

def viewPost(request, username, slug):
	post = forumPost.objects.get(slug=slug)
	context = {'post':post}
	if str(request.user.username).strip() == str(post.user).strip():
		context.update({'author':True})
	return render(request, "post_full.html", context)

def editPost(request, username, slug):
	instance = forumPost.objects.get(slug=slug)
	form = createpostform(request.POST or None, instance= instance)
	context = {'form':form}
	if form.is_valid():
		instance=form.save(commit=False)
		instance.slug = create_post_slug(instance)
		if request.POST['file']:
			instance.file = request.POST['file']

		instance.save()
		return HttpResponseRedirect('/%s/forum/post/%s'%(request.user.username,instance.slug))



	return render(request,"forum_post_edit.html", context)

def deletePost(request, username, slug):
	f = forumPost.objects.filter(slug=slug).values('forum')
	print(f)
	forum = Fourms.objects.get(id=f)
	print(forum.slug)
	post = forumPost.objects.get(slug=slug)
	post.delete()

	return HttpResponseRedirect('/%s/forumfull/%s/'%(request.user.username, forum.slug))


def subForum(request, username, slug):
	forum = Fourms.objects.get(slug=slug)
	forum.subscriber.add(request.user)

	return HttpResponseRedirect('/%s/forumfull/%s'%(request.user.username,forum.slug))

def unsubForum(request, username, slug):
	forum = Fourms.objects.get(slug=slug)
	forum.subscriber.remove(request.user)

	return HttpResponseRedirect('/%s/forumfull/%s'%(request.user.username,forum.slug))