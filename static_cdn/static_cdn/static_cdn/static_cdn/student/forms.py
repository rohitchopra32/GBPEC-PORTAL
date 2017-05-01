from django import forms

from .models import student

class loginForm(forms.ModelForm):
	class Meta:
		model = student
		fields = [
			"name",
			"password"
		]