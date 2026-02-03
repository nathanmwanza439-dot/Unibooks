from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User, Book, MissingRequest


class StudentCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'matricule', 'first_name', 'last_name', 'faculty')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'category', 'description', 'total_copies', 'image']


class MissingRequestForm(forms.ModelForm):
    class Meta:
        model = MissingRequest
        fields = ['title', 'authors', 'justification']


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label='Matricule ou email')


class ForcePasswordChangeForm(PasswordChangeForm):
    pass
