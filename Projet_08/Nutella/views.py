from django.shortcuts import render
from .forms import ContactForm, SearchForm
from django.views.generic.edit import FormView


# Create your views here.
def index(request):
    form = SearchForm()
    return render(request, 'Nutella/index.html', {'form': form})


def legals(request):
    return render(request, 'Nutella/legals.html')


"""
def contact(request):
    contact = ContactForm()
    return render(request, 'Nutella/contact.html', {'contact': contact})
"""


class ContactView(FormView):
    template_name = 'Nutella/contact.html'
    form_class = ContactForm
    success_url = 'Nutella/thanks/'
