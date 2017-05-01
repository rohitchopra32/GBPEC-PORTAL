from django import forms
from django.shortcuts import get_object_or_404

from .models import Fourms, forumPost, category
def choice():
	c = category.objects.all()
	choice=[]
	for c1 in c:
		choice.append((get_object_or_404(category, name=c1.name),c1))
	return tuple(choice)

class createform(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'mdl-textfield__input','id':'title'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'class':'mdl-textfield__input','rows':'3','id':'description'}))
	category = forms.ModelMultipleChoiceField(queryset=category.objects.all(), widget = forms.Select(attrs={'class':'mdl-selectfield__select', 'id':'category'}))
	class Meta:
		model = Fourms
		fields = [
			"title",
			"category",
			"description",
			"file",
		]


class createpostform(forms.ModelForm):

	class Meta:
		model = forumPost
		fields = [
			"content",
			"file",
		]