from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib import messages

from Auth.admin import UserCreationForm


class LoginView(View):
    """
    Displays form to log in.
    """

    def post(self, request):
        """
        When submitting informations via the form, this method is called
         and handles the login process.
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username}!")
                return redirect(reverse('Nutella:index',))
            else:
                form = AuthenticationForm()
        else:
            form = AuthenticationForm()
        messages.info(request, 'Une erreur est survenue. Veuillez réessayer!')
        return render(request, 'Auth/login.html', {'form': form})

    def get(self, request):
        """
        Simply displays the form when calling the webpage.
        """
        form = AuthenticationForm()
        return render(request, 'Auth/login.html', {'form': form})


class RegisterView(View):
    """
    A view that handle the creation of a new user.
    """

    def post(self, request):
        """
        Handles the case information is passed through the form to the
         webserver.
        """
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"Bienvenue {name}!")
            login(request, user)
            return redirect('Nutella:index',)
        else:
            for elt in form.errors.as_data():
                messages.info(request, f"{elt}: {form.errors.as_data()[elt]}")
            return redirect('Auth:register',)

    def get(self, request):
        """
        Displays the webpage with the form when trying to access the page
         for the first time.
        """
        template_name = 'Auth/register.html'
        form = UserCreationForm()
        return render(request, template_name, {'form': form})


class LogoutView(View):
    """
    Class based view to simply log out the user. Displays also a message.
    """

    def get(self, request):
        logout(request)
        messages.info(request, "Vous avez été déconnecté!")
        return redirect(reverse('Nutella:index',))


class AccountView(LoginRequiredMixin, TemplateView):
    """
    This view displays informantions for an account:
    if you're registered and logged in, you can access this page.
    """
    login_url = '/login/'
    template_name = 'Auth/account.html'
