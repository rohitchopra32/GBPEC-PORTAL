from django.db import models

# Create your models here.
class student(models.Model):
	name = models.CharField(max_length=120)
	password = models.CharField(max_length=512)
	roll_no = models.BigIntegerField()
	b1=2013
	b2=2014
	b3=2015
	b4=2016
	batch_CHOICES = (
		(b1, '2013'),
		(b2, '2014'),
		(b3, '2015'),
		(b4, '2016'),
	)
	batch = models.IntegerField(choices=batch_CHOICES, default=None)
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
	branch = models.CharField(max_length=3,choices=branch_CHOICES,default=None)

	email = models.EmailField(max_length = 100, null= True)
	contact = models.BigIntegerField()
	address = models.TextField(max_length = 300)
	first = False


	def __str__(self):
		return self.name