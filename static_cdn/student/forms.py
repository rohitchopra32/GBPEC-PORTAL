from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import Group, User

from .models import student



User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input',}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'mdl-textfield__input'}),required = True)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
       
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        p = False
        if username and password:
            try:
                user1 = User.objects.get(username = username)
                if not user1.check_password(password):
                    p = True
                
            except:
                pass

            user = authenticate(username=username, password=password)
            if p:
                raise forms.ValidationError("Incorrect passsword")
            if not user:
                raise forms.ValidationError("This user does not exist")
            
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)



class StudentProfileForm(forms.ModelForm):
    profile_pic = forms.FileField(widget = forms.FileInput(attrs = {'onchange':"upload_img(this);",'class':'none','id':'file_input_file,required:False'} ), required = False)
    first_name = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input'}))
    middle_name = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input'}), required = False)
    last_name = forms.CharField(widget = forms.TextInput(attrs={'class':'mdl-textfield__input'}))
    email = forms.CharField(widget = forms.EmailInput(attrs={'class':'mdl-textfield__input'}))
    contact = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'mdl-textfield__input','type':'text', 'pattern':'-?[0-9]*(\.[0-9]+)?','id':'sample2'}))
    address = forms.CharField(widget = forms.Textarea(attrs={'class':'mdl-textfield__input', 'type':'text','rows':'3'}))
    class Meta:
    	model = student
    	fields = {
            "profile_pic",
    		"first_name",
            "middle_name",
            "last_name",
    		"email",
    		"contact",
    		"address"

    	}