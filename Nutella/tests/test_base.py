from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from Auth.models import MyUser
from Nutella.models import Product, Category
from Nutella.views import ResultsView, SavedFoodView, AddToFavoriteView
from Nutella.views import LegalView, IndexView, ContactView, DeleteView


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
                         
    def test_get_redirected_after_sending_an_email(self):
        response = self.client.post(
            reverse('Nutella:contact'),
            {'email': 'test@test.fr',
             'message': 'This is a test message!'})
        self.assertEqual(response.status_code, 302)


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
        self.assertEqual(response.status_code, 302)

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
