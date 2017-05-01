from django.db import models
import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from classroom.models import Classroom
from fourms.models import Fourms
# Create your models here.
def download_location(instance, filename):
	return "%s/%s"%(instance.id, filename)

def choices():
	now = datetime.datetime.now()
	choices = ((i, str(i)) for i in range(2013, now.year+1))
	return choices




class student(models.Model):
	profile_pic = models.FileField(upload_to = download_location, null = True, blank = True)
	username = models.OneToOneField(settings.AUTH_USER_MODEL, default= None)
	first_name = models.CharField(max_length=120, null = True, blank=False)
	middle_name = models.CharField(max_length=120, null = True, blank=True)
	last_name = models.CharField(max_length=120, null=True, blank=True)
	roll_no = models.CharField(max_length = 20, unique = True)
	# b1=2013
	# b2=2014
	# b3=2015
	# b4=2016
	batch_CHOICES = choices()
	batch = models.IntegerField(choices=batch_CHOICES, default=None, null = True)
	br=''
	cse= 'cse'
	ece= 'ece'
	mae= 'mae'
	branch_CHOICES = (
		(br, 'branch'),
		(cse, 'CSE'),
		(ece, 'ECE'),
		(mae, 'MAE'),
	)
	branch = models.CharField(max_length=3,choices=branch_CHOICES,default=None, null = True)
	fourms = models.ManyToManyField(Fourms, related_name = "studentforum")
	email = models.EmailField(max_length = 100, null= True)
	contact = models.BigIntegerField(null = True)
	address = models.TextField(max_length = 300, null = True)
	classroom = models.ManyToManyField(Classroom, related_name = "students")
	first = models.BooleanField(default = True)


	def __str__(self):
		return self.roll_no


	def get_status(self):
		if self.first == True:
			return true
		return False

