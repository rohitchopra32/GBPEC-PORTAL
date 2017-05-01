from django import forms
from django.contrib.admin import widgets                                       


from .models import file, classPost as Post


class PostForm(forms.ModelForm):
    choice = (
        ('post','post'),
        ('anouncement','anouncement'),
        ('question', 'question')
        )
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'mdl-textfield__input','id':'s1'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'mdl-textfield__input','id':'sample5','rows':'3'}))
    post_type = forms.ChoiceField(choices = choice, widget = forms.Select(attrs={'class':'mdl-selectfield__select', 'id':'post_type'}))
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "post_type",
            
        ]

class FileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'class':'none','id':'file_input_file','required':'False'}), required = False )
    class Meta:
        model = file
        fields = [
            "file"
        ]
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(FileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['file'].required = False

class StudentPostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'mdl-textfield__input','id':'sample3'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'mdl-textfield__input','id':'sample5','rows':'3'}))
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            
                       
        ]
