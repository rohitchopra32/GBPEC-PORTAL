from django import forms
from django.shortcuts import get_object_or_404
from pagedown.widgets import PagedownWidget
from .models import Fourms, forumPost, category
def choice():
	c = category.objects.all()
	choice=[]
	for c1 in c:
		choice.append((get_object_or_404(category, name=c1.name),c1))
	return tuple(choice)

class createform(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'mdl-textfield__input','id':'title'}))
	description = forms.CharField(widget=PagedownWidget)
	file = forms.FileField(widget=forms.ClearableFileInput, required=False)
	class Meta:
		model = Fourms
		fields = [
			"title",
			"description",
			"file",
		]


class createpostform(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget)
	file = forms.FileField(widget=forms.ClearableFileInput, required=False)
	class Meta:
		model = forumPost
		fields = [
			"content",
			"file",
		]