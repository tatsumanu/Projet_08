from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import MyUser
from .views import AccountView


# Create your tests here.
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

    def test_results_view(self):
        response = self.client.get(reverse('Nutella:results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vous pouvez remplacer cet aliment par")


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
