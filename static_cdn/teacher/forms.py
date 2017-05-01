from django import forms
from .models import teacher


class TeacherProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget = forms.FileInput(attrs = {'onchange':"upload_img(this);",'class':'none','id':'file_input_file,required:False'} ), required = False )
    first_name = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input'}))
    middle_name = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input'}),required = False)
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input'}))
    email = forms.CharField(widget = forms.EmailInput(attrs={'class':'mdl-textfield__input'}))
    contact = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'mdl-textfield__input','type':'text', 'pattern':'-?[0-9]*(\.[0-9]+)?','id':'sample2'}))
    address = forms.CharField(widget = forms.Textarea(attrs={'class':'mdl-textfield__input', 'type':'text','rows':'3'}))
    class Meta:
    	model = teacher
    	fields = [
    		"profile_pic",
    		"first_name",
            "middle_name",
            "last_name",
    		"email",
    		"contact",
    		"address"
    	]