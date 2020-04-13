# -*-coding:'utf8'-*-

import time
import requests
from Nutella.models import Product, Category
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):

    help = """ The basic command used to populate the database associated
     with this project. You can choose the categories of products that
     will be collected and the numer of them, or let the program do it
     with default data. Use '--category' (requires a string or a list of
     strings) and '--nb_products' (requires an integer). """

    categories = ['biscuits et gateaux', 'pizzas tartes salées et quiches',
                  'boissons', 'pates a tartiner', 'produits laitiers',
                  'charcuteries', 'conserves']

    def add_arguments(self, parser):
        parser.add_argument(
            '--category', action='append', default=[], dest='categories'
        )
        parser.add_argument(
            '--nb_products', type=int, dest='nb_products', default=100
        )

    def handle(self, *args, **options):
        if not options['categories']:
            options['categories'] = self.categories
        if not options['nb_products']:
            options['nb_products'] = 100
        populate_db = PopulateDb(
            options['categories'], options['nb_products']
        )
        # Launch the collection!
        populate_db.run()


class PopulateDb:

    help = """ Class that manages to collect food products from the API and
     then populate the database with it. """

    # Some needed data
    data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
            'image_small_url', 'image_front_url', 'stores', 'ingredients_text']

    url = "https://fr.openfoodfacts.org/cgi/search.pl?"

    def __init__(self, categories, nb_products):
        self.categories = categories
        self.nb_products = nb_products
        self.double = None

    def run(self):

        """ Main loop iterating through the categories of food given
         to the command or from the default list. """

        # starting point
        t1 = time.time()
        print("Starting collection!")

        for category in self.categories:
            # inserting categories in category table
            cat = self.add_category(category)
            self.double = []

            payload = {
                'tag_0': category,
                'tag_contains_0': 'contains',
                'tagtype_0': 'categories',
                'tag_1': 'fr',
                'tag_contains_1': 'contains',
                'tagtype_1': 'lang',
                'sort_by': 'unique_scans_n',
                'page_size': self.nb_products,
                'action': 'process',
                'json': True
            }

            print(f'Collecting products from category {category}')

            response = requests.get(self.url, params=payload)

            products = response.json()['products']

            for product in products:
                if self.check_fields(product):
                    product = self.cleaned_data(product)
                    Product.objects.create(
                        name=product['product_name'],
                        category=cat,
                        brand=product['brands'],
                        nutri_grade=product['nutrition_grade_fr'],
                        url=product['url'],
                        stores=product['stores'],
                        ingredients=product['ingredients_text'],
                        image_small=product['image_small_url'],
                        image_xl=product['image_front_url']
                    )

        print(""" Operations completed successfully in {:02f}\
 seconds!""".format((time.time() - t1)))

    def check_fields(self, product):
        if all(product.get(i, None) for i in self.data):
            return True
        else:
            return False

    def cleaned_data(self, product):
        a = product['ingredients_text']
        a = a.replace('_', '').strip()
        product['ingredients_text'] = a
        return product

    """ def check_double(self, product):
        if product['product_name'] not in self.double:
            self.double.append(product['product_name'])
        else:
            return False """

    def add_category(self, name):
        try:
            c = Category.objects.create(name=name)
        except IntegrityError:
            print("Category already existing! Will add new products to it!")
            c = Category.objects.get(name=name)
        return c
