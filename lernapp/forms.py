from django import forms
from django.contrib.auth import get_user_model
class ContactForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
    message=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Your Message'}))


    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError("Enter gmail.com email address")
        return email

class LoginForm(forms.Form):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username '}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))

user=get_user_model()
class RegistrationForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username '}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password '}))
    password2=forms.CharField(label='confirm pasword',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password '}))
    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        if password !=password2:
            raise forms.ValidationError('Enter both password same')
        return data

    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=user.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username {} is already taken".format(username))
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=user.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("{} is already registerd ".format(email))
        return email
