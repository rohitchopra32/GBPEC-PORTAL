from django import forms
from .models import post
from pagedown.widgets import PagedownWidget


class postform(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget())
	class Meta:
		model = post
		fields = [
			"title",
			"content",
			"attachment",
		]