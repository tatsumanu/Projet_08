from django import forms
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    email = forms.EmailField(label='Votre adresse mail ')
    message = forms.CharField(widget=forms.Textarea, label='Dites nous tout! ')


class SearchForm(forms.Form):
    search = forms.CharField(initial='Produit', label='')


class LoginForm(forms.Form):
    name = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(label='Adresse mail')
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label='Mot de passe')
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Confirmation du mot de passe')
