from django import forms
from .models import UserProfile


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile

        fields = [
            'name',
            'email',
            'phone',
            'dob',
            'password'
        ]