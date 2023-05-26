from django import forms
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class CreateUserForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name','phone','phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm,self).__init__(*args,**kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control px-4'


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class Update(forms.ModelForm):
    class Meta:
        model = User
        fields=('first_name','last_name','other_name','email','phone','image','bio','date_of_birth','gender')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(Update,self).__init__(*args,**kwargs)
        required = ('first_name','last_name','email','gender')
        gender = ('gender',)
        bio = ('bio',)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-lg mb-2'
            if i in required:
                self.fields[i].widget.attrs['readonly'] = True
            if i in gender:
                self.fields[i].widget.attrs['class'] = 'form-select form-select-lg mb-2'
            if i in bio:
                self.fields[i].widget.attrs['rows'] = 3         