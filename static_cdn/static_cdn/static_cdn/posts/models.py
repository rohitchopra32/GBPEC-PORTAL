import os
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


from classroom.models import Classroom
from comments.models import Comment

# Create your models here.


def upload_location(instance, filename):
    return "Post/%s/%s" %(instance.Post, filename)


class classPost(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True, blank = True)
	content = models.TextField()
	choice = (
		('post','post'),
		('anouncement','anouncement'),
		('question', 'question')
		)
	post_type = models.CharField(choices = choice, default = 'post', max_length = 12)
	classroom = models.ForeignKey(Classroom)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	

	def __unicode__(self):
	    return self.title

	def __str__(self):
	    return self.title

	@property
	def comments(self):
	    instance = self
	    qs = Comment.objects.filter_by_instance(instance)
	    return qs

	@property
	def get_content_type(self):
	    instance = self
	    content_type = ContentType.objects.get_for_model(instance.__class__)
	    return content_type.model

	def get_absolute_url(self):
	    return reverse("posts:detail", kwargs={"slug": self.slug})
        
class file(models.Model):
	file = models.FileField(upload_to = upload_location, blank = True, null = True)
	Post = models.ForeignKey(classPost, blank = True, null = True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, blank = True, null = True)

	def filename(self):
		f = self.file.name
		f1 = f.split('/', 3)[-1]
		return f1

	def __unicode__(self):
		return self.file.name

	def __str__(self):
		return self.file.name






def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
	    slug = new_slug
	qs = classPost.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
	    new_slug = "%s-%s" %(slug, qs.first().id)
	    return create_slug(instance, new_slug=new_slug)
	return slug

