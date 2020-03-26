from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(label='Votre adresse mail ')
    message = forms.CharField(widget=forms.Textarea, label='Dites nous tout! ')


class SearchForm(forms.Form):
    search = forms.CharField(initial='Produit', label='')
