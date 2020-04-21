from django import forms


# Models for the forms of website
class ContactForm(forms.Form):
    """
    A basic contact form. Not implemented on the first version of the app.
    """
    email = forms.EmailField(label='Votre adresse mail ')
    message = forms.CharField(widget=forms.Textarea, label='Dites nous tout! ')


class SearchForm(forms.Form):
    """
    The form designed to look for an healthier product as the user enters
    his search in.
    """
    search = forms.CharField(initial='Produit', label='')
