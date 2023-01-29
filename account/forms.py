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

		fields=[
			"image",
		]
