from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import MyUser
from .views import AccountView, ResultsView


class BasicViewTest(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('Nutella:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui mais de qualité!")

    def test_legal_view(self):
        response = self.client.get(reverse('Nutella:legals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SARL Pur Beurre")

    def test_contact_view(self):
        response = self.client.get(reverse('Nutella:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dites nous tout!")


class AccountViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_cant_access_account_view_if_not_logged_in(self):
        response = self.client.get(reverse('Nutella:account'))
        self.assertEqual(response.status_code, 302)

    def test_can_access_account_view_if_logged_in(self):
        request = self.factory.get('/account/')
        request.user = self.user
        response = AccountView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Voici les informations que l'on a sur vous...")


class ResultsViewTest(TestCase):

    def test_get_redirected_when_no_search_entered(self):
        response = self.client.get(reverse('Nutella:results'))
        self.assertEqual(response.status_code, 302)

    def test_access_results_view_when_entering_search_terms(self):
        response = self.client.post('/results/', {'search': 'search_terms'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'search_terms')

    def test_access_results_page_with_session_context(self):
        session = self.client.session
        session['last_search'] = {'search_terms': 'search_terms'}
        session.save()
        response = self.client.get('/results/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'search_terms')

    def test_cant_save_products_if_not_logged_in(self):
        response = self.client.post('/results/', {'search': 'pizza'})
        self.assertContains(response, "Voir ce produit")

    def test_can_save_product_if_logged_in(self):
        c = self.client.force_login(user='TestUser')
        response = c.post('/results/', {'search': 'search_terms'})
        self.assertContains(response, 'Sauvegarder')
