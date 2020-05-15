from django.test import TestCase, RequestFactory
from django.urls import reverse
from Auth.views import RegisterView, LoginView, AccountView, LogoutView
from Auth.models import MyUser


# Create your tests here.
class AccountViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_account_view_is_tested(self):
        response = self.client.get(reverse('Auth:account'))
        self.assertEqual(response.resolver_match.func.__name__,
                         AccountView.as_view().__name__)

    def test_cant_access_account_view_if_not_logged_in(self):
        response = self.client.get(reverse('Auth:account'))
        self.assertEqual(response.status_code, 302)

    def test_can_access_account_view_if_logged_in(self):
        request = self.factory.get('/account/')
        request.user = self.user
        response = AccountView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Voici les informations que l'on a sur vous...")


class LoginViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_login_view_is_tested(self):
        response = self.client.get(reverse('Auth:login'))
        self.assertEqual(response.resolver_match.func.__name__,
                         LoginView.as_view().__name__)

    def test_can_access_login_view_with_get_method(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_log_in_with_correct_values_and_get_redirected(self):
        response = self.client.post(
            '/login/',
            {'username': 'john@doe.com', 'password': 'johndoe'})
        self.assertEqual(response.status_code, 302)

    def test_cannot_log_in_with_incorrect_data_and_post_method(self):
        response = self.client.post(
            '/login/',
            {'username': 'joe_test', 'password': ''}
        )
        self.assertEqual(response.status_code, 200)


class RegisterViewTest(TestCase):

    def test_register_view_is_tested(self):
        response = self.client.get(reverse('Auth:register'))
        self.assertEqual(response.resolver_match.func.__name__,
                         RegisterView.as_view().__name__)

    def test_can_access_register_view(self):
        response = self.client.get(reverse('Auth:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créer un compte")

    def can_register_with_post_method(self):
        self.client.post(
            '/register/',
            {'name': 'john@doe.com', 'password': 'johndoe'}
        )
        new_user = MyUser.objects.last()
        self.assertEquals(new_user.name, 'john@doe.com')

    def test_cannot_register_with_incorrect_data(self):
        self.client.post(
            '/register/',
            {'name': 'joe_test', 'password': ''}
        )
        new_user = MyUser.objects.last()
        self.assertEqual(new_user, None)


class LogoutViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.client.post(
            '/login/',
            {'name': 'john@doe.com', 'password': 'johndoe'})

    def test_logout_view_is_tested(self):
        response = self.client.get(reverse('Auth:logout'))
        self.assertEqual(response.resolver_match.func.__name__,
                         LogoutView.as_view().__name__)

    def test_logout_when_logged_in(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_get_redirected_to_home_page_when_logged_out(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.url, '/')
