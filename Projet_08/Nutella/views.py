from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView, ListView, View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .admin import UserCreationForm
from .models import Product
from .forms import ContactForm, SearchForm


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


class ProductView(DetailView):
    template_name = 'Nutella/product.html'
    model = Product


class AccountView(LoginRequiredMixin, TemplateView):
    redirect_field_name = "/account/"
    login_url = '/login/'
    template_name = 'Nutella/account.html'


class SavedFoodView(ListView):
    template_name = 'Nutella/saved_food.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(users=self.request.user)


class AddToFavoriteView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        try:
            product.users.set((request.user,))
        except:
            messages.info(request, "Une erreur s'est produite!")
            return render(request, 'Nutella/results.html')
        else:
            product.save()
            messages.success(request,
                             "Cet aliment a été ajouté à votre liste!")
            return HttpResponseRedirect(reverse('Nutella:results'))


def results(request):
    template_name = 'Nutella/results.html'
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            search_terms = form.cleaned_data.get('search')
            result = Product.objects.filter(
                category__name__icontains=search_terms)
            if not result:
                result = Product.objects.filter(name__icontains=search_terms)
            request.session['last_search'] = {'search_terms': search_terms}
            return render(request,
                          template_name,
                          {'result': result, 'search_terms': search_terms})
    else:
        if 'last_search' in request.session:
            context = request.session['last_search']
            search_terms = context['search_terms']
            result = Product.objects.filter(
                category__name__icontains=search_terms)
            if not result:
                result = Product.objects.filter(name__icontains=search_terms)
            context['result'] = result
        else:
            return HttpResponseRedirect(reverse('Nutella:index'))
        return render(request,
                      template_name,
                      context)


class LoginView(View):

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username}!")
                return redirect(reverse('Nutella:index',))

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'Nutella/login.html', {'form': form})


def register(request):
    template_name = 'Nutella/register.html'
    if request.method == 'POST':
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
            return redirect('Nutella:register',)
    else:
        form = UserCreationForm()
        return render(request, template_name, {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.info(request, "Vous avez été déconnecté!")
        return redirect(reverse('Nutella:index',))
