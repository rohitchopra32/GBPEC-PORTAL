from django import forms
from .models import Classroom

class classroomForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'mdl-textfield__input','id':'sample3'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'class':'mdl-textfield__input','rows':'3','id':'sample5'}))
	class Meta:
		model = Classroom
		fields = [
			"name",
			"description",
		]

