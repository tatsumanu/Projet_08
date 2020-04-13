from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic.edit import FormView, BaseFormView
from django.views.generic import TemplateView, DetailView, ListView, View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from .admin import UserCreationForm
from .models import Product
from .forms import ContactForm, SearchForm


# context_processors functions
def navbar_search_form(request):
    search_form = SearchForm()
    return {'search_form': search_form}


# Create your views here.
class IndexView(FormView):
    """
    Simple homepage view for the website.
    Contains a form to search for food products.
    """
    form_class = SearchForm
    template_name = 'Nutella/index.html'


class LegalView(TemplateView):
    """
    This view displays legal content for this
     website.
    """
    template_name = 'Nutella/legals.html'


class ContactView(FormView):
    """
    A view to display contact form.
    Currently not working in this version.
    """
    template_name = 'Nutella/contact.html'
    form_class = ContactForm
    success_url = 'Nutella/thanks/'


class ProductView(DetailView):
    """
    Displays details about a product.
    Needs a product_id to be sent in request.
    """
    template_name = 'Nutella/product.html'
    model = Product


class AccountView(LoginRequiredMixin, TemplateView):
    """
    This view displays informantions for an account:
    if you're registered and logged in, you can access this page.
    """
    redirect_field_name = "/account/"
    login_url = '/login/'
    template_name = 'Nutella/account.html'


class SavedFoodView(ListView):
    """
    Displays all the food products already saved by the logged in
     user. If not any, displays an alternative page.
    """
    paginate_by = 6
    template_name = 'Nutella/saved_food.html'
    context_object_name = 'products'

    def get_queryset(self):
        "This is where we try to retrieve already saved products."
        return Product.objects.filter(users=self.request.user)


class AddToFavoriteView(View):
    """
    Creates a relation between an existing product and an
     identified user.
    """

    def post(self, request, product_id):
        """
        No GET method here. Only POST. To prevent XSS. Try to add
         a new relation in the users(favorites) product field. Display
         a message if success or not. Can also manage cases when the
         selected product is already saved.
        """
        product = get_object_or_404(Product, pk=product_id)
        if request.user in product.users.all():
            messages.info(request, "Cet aliment est déjà dans vos favoris!")
        else:
            try:
                product.users.set((request.user,))
            except KeyError:
                messages.info(request, "Une erreur s'est produite!")
            else:
                product.save()
                messages.success(
                    request,
                    "Cet aliment a été ajouté à votre liste!"
                    )
        return HttpResponseRedirect(reverse('Nutella:results'))


class DeleteView(View):
    """
    Removes selected relation between identified user and an already
     saved product.
    """

    def post(self, request, product_id):
        """
        Handles the product_id given by the request and try to remove
         existing relation between the user and this product.
        Displays message for success or not.
        """
        product = get_object_or_404(Product, pk=product_id)
        try:
            product.users.remove(request.user)
        except KeyError:
            messages.info(request, "Une erreur s'est produite!")
        else:
            product.save()
            messages.success(request, "Aliment supprimé de votre liste!")
            return redirect(reverse('Nutella:saved_food'))


class ResultsView(ListView, BaseFormView):
    """
    Displays the products found with the search terms of the user.
    """

    template_name = 'Nutella/results.html'
    context_object_name = 'products'
    paginate_by = 6
    form_class = SearchForm

    def get_queryset(self):
        """
        Look for better food products in our database. Also save the
         results of it by saving search_term's informations and results
         in the session object.
        """
        context = self.request.session['last_search']
        search_terms = context['search_terms']
        result = Product.objects.filter(
            category__name__icontains=search_terms)
        if not result:
            result = Product.objects.filter(name__icontains=search_terms)
        return result.order_by('nutri_grade')

    def form_valid(self, form):
        """
        Handles the research made by the user, through the category and
         product references.
        """
        search_terms = form.cleaned_data.get('search')
        self.request.session['last_search'] = {'search_terms': search_terms}
        self.request.session['search_terms'] = search_terms
        return self.get(self.request)


class ResultsView2(ListView):

    template_name = 'Nutella/results.html'
    context_object_name = 'products'

    def post(self, request):

        form = SearchForm(data=request.POST)
        if form.is_valid():
            search_terms = form.cleaned_data.get('search')
            result = Product.objects.filter(
                category__name__icontains=search_terms)
            if not result:
                result = Product.objects.filter(name__icontains=search_terms)
            result = result.order_by('pk')
            request.session['last_search'] = {'search_terms': search_terms}
            paginator = Paginator(result, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,
                          self.template_name,
                          {'products': result,
                           'search_terms': search_terms,
                           'page_obj': page_obj})
        else:
            return render(request, self.template_name)

    def get(self, request):

        if 'last_search' in request.session:
            context = request.session['last_search']
            search_terms = context['search_terms']
            result = Product.objects.filter(
                category__name__icontains=search_terms)
            if not result:
                result = Product.objects.filter(name__icontains=search_terms)
            context['products'] = result
        else:
            return HttpResponseRedirect(reverse('Nutella:index'))
        result = result.order_by('pk')
        paginator = Paginator(result, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return render(request,
                      self.template_name,
                      context)


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
        return render(request, 'Nutella/login.html', {'form': form})

    def get(self, request):
        """
        Simply displays the form when calling the webpage.
        """
        form = AuthenticationForm()
        return render(request, 'Nutella/login.html', {'form': form})


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
            return redirect('Nutella:register',)

    def get(self, request):
        """
        Displays the webpage with the form when trying to access the page
         for the first time.
        """
        template_name = 'Nutella/register.html'
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
