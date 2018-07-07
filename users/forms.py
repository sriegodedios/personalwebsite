from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from localflavor.us.models import USStateField
from users.models import ContactInformation, Profile
from django.forms import ModelForm



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2', )

class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1')


class AddressForm(ModelForm):
    class Meta:
        model = ContactInformation
        fields = ('username', 'address_1', 'address_2','city','state','zip_code')



class ChangePasswordForm:
    model = User
    fields = ('new_password1','new_password2','old_password')

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        
class ImageUploadForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("picture",)

#class PictureUploadForm(ModelForm):
#    class Meta:
#        model = forms.ImageFields()
