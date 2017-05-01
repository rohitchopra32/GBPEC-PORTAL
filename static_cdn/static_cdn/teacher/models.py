from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from classroom.models import Classroom
from fourms.models import Fourms
# Create your models here.
def download_location(instance, filename):
	return "%s/%s"%(instance.id, filename)
class teacher(models.Model):
	def image_tag(self):
	    return u'<img src="%s"/>' % self.profile_pic.url

	image_tag.short_description = 'Image'
	image_tag.allow_tags = True

	profile_pic = models.FileField(upload_to = download_location, null = True, blank = True)
	username = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, limit_choices_to = {'groups':1})
	first_name = models.CharField(max_length=120, null = True, blank=False)
	middle_name = models.CharField(max_length=120, null = True, blank=True)
	last_name = models.CharField(max_length=120, null = True, blank=False)
	email = models.EmailField(max_length = 100, null= True)
	contact = models.BigIntegerField(null = True)
	position = models.CharField(max_length=120, null=True)
	address = models.TextField(max_length = 300, null = True)
	fourms = models.ManyToManyField(Fourms, related_name = "teacher_fourms")
	first = models.BooleanField(default = True)
	

	def __str__(self):
		return self.first_name

	def get_status(self):
		if self.first == True:
			return true
		return False

