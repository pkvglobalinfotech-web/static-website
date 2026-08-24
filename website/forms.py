from django import forms

from .models import Contact,User

from django.contrib.auth.forms import UserCreationForm



class RegisterForm(UserCreationForm):


    class Meta:

        model=User

        fields=[
            "username",
            "email",
            "password1",
            "password2"
        ]
class ContactForm(forms.ModelForm):


    class Meta:

        model=Contact

        fields=[
            "name",
            "email",
            "phone",
            "message"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555 123 4567'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Tell us about your project...'}),
        }