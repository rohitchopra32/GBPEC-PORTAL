from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.contrib import messages
from .models import post
from .forms import postform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm

def post_create(request, username=None):
	
	form = postform(request.POST or None, request.FILES or None);
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request,"save!!", extra_tags='some-tag')
		return HttpResponseRedirect('/%s/post/'%username)

	context = {
		"form": form,
		"username": username,

	}
	return render(request, "post_form.html", context)


def post_home(request, username=None):
	queryset_list= post.objects.all().order_by("-timestamp")
	paginator = Paginator(queryset_list, 5)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	
	context = {
		"object_list":queryset,
		"title": "list",
		"page_request_var":page_request_var,
		"username": username,
	}
	return render(request, "index.html", context)



def post_detail(request, id=None,username=None):
	instance = get_object_or_404(post, id=id)
	comments = Comment.objects.filter_by_instance(instance)
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_data = form.cleaned_data.get('content')
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		new_comment, created = Comment.objects.get_or_create(
								user = request.user,
								content_type = content_type,
								object_id = obj_id,
								content = content_data

								)
	context={
		"title": instance.title,
		"instance": instance,
		"comments": comments,
		"form": form,
		"username": username,

		

	}
	return render(request, "post_detail.html", context)


def post_update(request, id = None, username=None):
	instance = get_object_or_404(post, id= id)
	form = postform(request.POST or None,  request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request,"save!!", extra_tags='some-tag')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": instance.title,
			"instance": instance,
			"form": form,
			"username": username,


		}
	return render(request, "post_form.html",context)

def post_delete(request, id=None, username=None):
	instance = get_object_or_404(post, id= id)
	instance.delete()
	messages.success(request,"save!!", extra_tags='some-tag')
	return redirect("post:home")