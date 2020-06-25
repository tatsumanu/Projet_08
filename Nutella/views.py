from django.shortcuts import reverse, redirect, get_object_or_404
from django.views.generic.edit import FormView, BaseFormView
from django.views.generic import TemplateView, DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Product
from .forms import ContactForm, SearchForm
from django.conf import settings


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
    success_url = '/'
    
    def post(self, request):
        user = request.POST['email']
        message = "This is an automated reply sent from Pur Beurre Website.\
    \nWe will soon answer you! Thank you for supporting 'Pur Beurre!'\n"
        message += request.POST['message']
        email_from = settings.EMAIL_HOST_USER
        if user and message:
            send_mail(
            'Reply from Pur Beurre',
            message,
            email_from,
            [user, email_from],
            fail_silently=True,
            )
            messages.success(request, f"Merci pour votre message {user}!")
            return redirect(reverse('Nutella:index',))
        else:
            form = ContactForm()
        messages.info(request, 'Une erreur est survenue. Veuillez réessayer!')
        return render(request, template_name, {'form': form})


class ProductView(DetailView):
    """
    Displays details about a product.
    Needs a product_id to be sent in request.
    """
    template_name = 'Nutella/product.html'
    model = Product


class SavedFoodView(LoginRequiredMixin, ListView):
    """
    Displays all the food products already saved by the logged in
     user. If not any, displays an alternative page.
    """
    login_url = '/login/'
    paginate_by = 6
    template_name = 'Nutella/saved_food.html'
    context_object_name = 'products'

    def get_queryset(self):
        "This is where we try to retrieve already saved products."
        return Product.objects.filter(users=self.request.user).order_by('pk')


class AddToFavoriteView(LoginRequiredMixin, View):
    """
    Creates a relation between an existing product and an
     identified user.
    """
    
    login_url = '/login/'

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
    Look for better food products in our database. Also save the
    results of it by saving search_term's informations and results
    in the session object.
    """

    template_name = 'Nutella/results.html'
    context_object_name = 'products'
    paginate_by = 6
    form_class = SearchForm

    def get_queryset(self):

        context = self.request.session['last_search']
        search_terms = context['search_terms']
        result = self.search_product(search_terms)
        return result

    def search_product(self, search):

        products = Product.objects.filter(name__icontains=search)
        if products:
            product = products.first()
            return product.get_better_food(product).all()
        else:
            return []

    def form_valid(self, form):

        search_terms = form.cleaned_data.get('search')
        self.request.session['last_search'] = {'search_terms': search_terms}
        return self.get(self.request)
