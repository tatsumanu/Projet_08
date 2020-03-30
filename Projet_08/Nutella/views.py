from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .forms import ContactForm, SearchForm, LoginForm, RegisterForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView


# context_processors functions
def navbar_search_form(request):
    search_form = SearchForm()
    return {'search_form': search_form}


# Create your views here.
class IndexView(FormView):
    form_class = SearchForm
    template_name = 'Nutella/index.html'


class LegalView(TemplateView):
    template_name = 'Nutella/legals.html'


class ContactView(FormView):
    template_name = 'Nutella/contact.html'
    form_class = ContactForm
    success_url = 'Nutella/thanks/'


def results(request):
    template_name = 'Nutella/results.html'
    return render(request, template_name)


class LoginView(FormView):
    template_name = 'Nutella/login.html'
    form_class = LoginForm
    success_url = '/'


def register(request):
    template_name = 'Nutella/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Bienvenue {username}!")
            login(request, user)
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            print(messages.error)
        return HttpResponseRedirect(reverse('Nutella:index'))
    else:
        form = RegisterForm()
        return render(request, template_name, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('Nutella:index',))


class AccountView(TemplateView):
    template_name = 'Nutella/account.html'


def saved_food_view(request):
    pass
