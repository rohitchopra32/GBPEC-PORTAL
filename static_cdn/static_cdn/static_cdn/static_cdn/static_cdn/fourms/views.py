from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils.text import slugify


from .models import Fourms, category, forumPost, create_forum_slug, create_post_slug
from .forms import createform, createpostform
# Create your views here.


def forumView(request,username, sortby=None):
	forum = Fourms.objects.all().order_by("-created")
	all_category = category.objects.all()
	context = {
		'forums':forum,
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
		if request.FILES:
			for f in request.FILES.getlist('file'):
				file=f	
			print(file)
		f.file= file
		f.save()
		messages.success(request, 'Forum Created Succesfully successfully', extra_tags='html_safe')
		return HttpResponseRedirect('/%s/forum/'%request.user.username)


	if sortby is not None:
		sort = Fourms.objects.filter(category = category.objects.get(name=sortby)) 
		print(sort)
		context.update({'forums':sort,'sort':sortby})
	
	return render(request, "forum_view.html", context)


def editForum(request, username, slug=None):

	return render(request, "forum_edit.html", context)

def deleteForum(request, username, slug):

	return HttpResponseRedirect('/%s/forum/%s'%(request.user.username, f.slug))

def fullForum(request, username, slug):
	forum = Fourms.objects.get(slug=slug)
	posts = forumPost.objects.filter(forum = forum).order_by("-timestamp")
	context = {
		'forum':forum,
		'posts':posts,

	}
	if str(request.user.username).strip() == str(forum.creator).strip():
		context.update({'author':True})
	

	return render(request, "forum_full.html", context)

def editPost(request, username, slug):

	return render(request,"forum_post_edit.html", context)

def deletePost(request, username, slug):

	return HttpResponseRedirect('/%s/forum/post/%s/'%(request.user.username, p.slug))


