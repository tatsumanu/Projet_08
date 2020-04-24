from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.urls import reverse
from Auth.models import MyUser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from .models import Product, Category
from .views import ResultsView, SavedFoodView, AddToFavoriteView
from.views import LegalView, IndexView, ContactView, DeleteView



class IndexViewTest(TestCase):

    def test_can_access_index_view(self):
        response = self.client.get(reverse('Nutella:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui mais de qualité!")

    def test_index_view_is_tested(self):
        response = self.client.get(reverse('Nutella:index'))
        self.assertEqual(response.resolver_match.func.__name__,
                         IndexView.as_view().__name__)


class LegalViewTest(TestCase):

    def test_can_access_legal_view(self):
        response = self.client.get(reverse('Nutella:legals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SARL Pur Beurre")

    def test_legal_view_is_tested(self):
        response = self.client.get(reverse('Nutella:legals'))
        self.assertEqual(response.resolver_match.func.__name__,
                         LegalView.as_view().__name__)


class ContactViewTest(TestCase):

    def test_can_access_contact_view(self):
        response = self.client.get(reverse('Nutella:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dites nous tout!")

    def test_contact_view_is_tested(self):
        response = self.client.get(reverse('Nutella:contact'))
        self.assertEqual(response.resolver_match.func.__name__,
                         ContactView.as_view().__name__)


class SavedFoodViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_saved_food_view_is_tested(self):
        response = self.client.get(reverse('Nutella:saved_food'))
        self.assertEqual(response.resolver_match.func.__name__,
                         SavedFoodView.as_view().__name__)

    def test_cant_access_saved_food_view_if_not_logged_in(self):
        response = self.client.get(reverse('Nutella:saved_food'))
        self.assertEqual(response.status_code, 302)

    def test_can_access_saved_food_view_if_logged_in(self):
        request = self.factory.get('/saved_food/')
        request.user = self.user
        response = SavedFoodView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Vos aliments sauvegardés!")


class AddToFavoriteViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            name='test',
            category=self.category
        )
        self.factory = RequestFactory()

    def test_add_to_favorite_view_is_tested(self):
        response = self.client.post(reverse(
            'Nutella:add_to_favorite',
            args=(10221,)
            ))
        self.assertEqual(response.resolver_match.func.__name__,
                         AddToFavoriteView.as_view().__name__)

    def test_cant_add_to_favorite_if_not_logged_in(self):
        response = self.client.post(reverse(
            'Nutella:add_to_favorite',
            args=(10221,)
        ))
        self.assertEqual(response.status_code, 404)

    def test_can_add_to_favorite_if_logged_in(self):
        request = self.factory.post(reverse(
            'Nutella:add_to_favorite',
            args=(self.product.id,)
        ))
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = AddToFavoriteView.as_view()(
            request,
            product_id=self.product.id)
        self.assertEqual(response.status_code, 302)


class ResultsViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def create_conditions_for_test(self):
        category = Category.objects.create(
            name='test_category'
        )
        product = Product.objects.create(
            name='test_name',
            brand='test_brand',
            nutri_grade='a',
            category=category
        )
        return product

    def test_can_access_results_view_with_post_method(self):
        response = self.client.post('/results/', {'search': 'search_terms'})
        self.assertEqual(response.status_code, 200)

    def test_can_access_results_view_with_get_method_and_session_data(self):
        session = self.client.session
        session['last_search'] = {'search_terms': 'test'}
        session.save()
        response = self.client.get('/results/')
        self.assertEqual(response.status_code, 200)

    def test_results_view_is_tested(self):
        session = self.client.session
        session['last_search'] = {'search_terms': 'test'}
        session.save()
        response = self.client.get(reverse('Nutella:results'))
        self.assertEqual(response.resolver_match.func.__name__,
                         ResultsView.as_view().__name__)

    def test_search_product_method_with_existing_products(self):
        product = self.create_conditions_for_test()
        result_view = ResultsView()
        result = result_view.search_product('test')
        self.assertEqual(product, [x for x in result][0])

    def test_search_product_method_with_zero_product(self):
        result_view = ResultsView()
        result = result_view.search_product('test')
        self.assertEqual([], result)


class ProductViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            name='test',
            category=self.category
        )
        self.factory = RequestFactory()

    def test_can_access_to_product_view(self):
        request = self.factory.post(reverse(
            'Nutella:product',
            args=(self.product.id,)
        ))
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = AddToFavoriteView.as_view()(
            request,
            product_id=self.product.id)
        self.assertEqual(response.status_code, 302)


class DeleteViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            name='test',
            category=self.category
        )
        self.factory = RequestFactory()

    def test_delete_view_is_tested(self):
        response = self.client.get(reverse(
            'Nutella:delete',
            args=(10221,)
        ))
        self.assertEqual(response.resolver_match.func.__name__,
                         DeleteView.as_view().__name__)

    def test_call_delete_view_without_product_id_get_404(self):
        response = self.client.post(reverse(
            'Nutella:delete',
            args=(0,)
        ))
        self.assertEqual(response.status_code, 404)

    def test_get_redirected_to_saved_food_page_when_deleting_product(self):
        request = self.factory.post(reverse(
            'Nutella:product',
            args=(self.product.id,)
        ))
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = DeleteView.as_view()(
            request,
            product_id=self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/saved_food/')


class AdminViewTest(TestCase):

    def test_get_redirected_when_accessing_admin_view(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)


class CategoryModelTest(TestCase):

    def create_conditions_for_test(self):
        category = Category.objects.create(
            name='test_category'
        )
        return category

    def test_can_create_category(self):
        category = self.create_conditions_for_test()
        last_category = Category.objects.last()
        self.assertEqual(category, last_category)

    def test_can_render_category_name_when_called(self):
        category = self.create_conditions_for_test()
        self.assertEqual(category.name, category.__str__())


class ProductModelTest(TestCase):

    def create_conditions_for_test(self):
        category = Category.objects.create(
            name='test_category'
        )
        product = Product.objects.create(
            name='test_name',
            brand='test_brand',
            nutri_grade='a',
            category=category
        )
        return product

    def test_can_create_product_models_if_category_defined(self):
        product = self.create_conditions_for_test()
        last_product = Product.objects.last()
        self.assertEqual(product, last_product)

    def test_can_render_product_name_when_called(self):
        product = self.create_conditions_for_test()
        self.assertEqual(product.name, product.__str__())

    def test_get_better_food_method(self):
        product = self.create_conditions_for_test()
        category = Product.objects.last().category
        Product.objects.create(
            name='new_test_product',
            brand='test_brand',
            nutri_grade='b',
            category=category
        )
        right_order = [elt for elt in Product.objects.all().order_by('nutri_grade')]
        order_returned = [elt for elt in product.get_better_food(product)]
        self.assertEqual(right_order, order_returned)


class RegisterSearchSaveProductTest(LiveServerTestCase):
    """
    A test class working with selenium. Chrome should be installed as well
     as the chromedriver.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login_with_selenium(self):
        # Now login again with informations provided when registering
        self.selenium.get('http://127.0.0.1:8000')
        login_btn = self.selenium.find_element_by_id('login')
        ActionChains(self.selenium).move_to_element(login_btn).click().perform()
        username_form = self.selenium.find_element_by_name('username')
        username_form.send_keys('testname@test.fr')
        pass_form = self.selenium.find_element_by_name('password')
        pass_form.send_keys('testname_pass')
        pass_form.submit()

    def test_can_search_for_products_with_selenium(self):
        # Login with informations of test_Auth
        self.login_with_selenium()
        search_form = self.selenium.find_element_by_name('search')
        search_form.clear()
        search_form.send_keys('nutella')
        search_form.submit()

        # Check that we are now on result page and there are food products
        self.assertTrue("Vous pouvez remplacer cet aliment par" in self.selenium.page_source)

        # Selecting a random product and print his informations page
        result = self.selenium.find_element_by_id('result')
        ActionChains(self.selenium).move_to_element(result).click().perform()
        self.assertTrue("Voici les informations disponibles sur ce produit" in self.selenium.page_source)

    def test_save_a_random_product_and_access_to_it_through_savedfoodpage(self):
        # Saving selected product
        save_btn = self.selenium.find_element_by_id('save_btn')
        saved_food_url = self.selenium.current_url
        ActionChains(self.selenium).move_to_element(save_btn).click().perform()
        # Now going to saved_food page to check that this product has been saved
        savedfood_page = self.selenium.find_element_by_id('savedfood')
        ActionChains(self.selenium).move_to_element(savedfood_page).click().perform()
        food_from_savedfood_page = self.selenium.find_element_by_id('to_product_info')
        ActionChains(self.selenium).move_to_element(food_from_savedfood_page).click().perform()
        self.assertEquals(saved_food_url, self.selenium.current_url)

        # If all works we can now logout and quit!
        logout_btn = self.selenium.find_element_by_id('logout')
        ActionChains(self.selenium).move_to_element(logout_btn).click().perform()
