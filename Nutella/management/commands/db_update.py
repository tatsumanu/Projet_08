# -*-coding:'utf8'-*-

import requests
from Nutella.models import Product, Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = """ The command used to update the database associated
     with this project. Designed to be launched from cron table. """

    def handle(self, *args, **options):
        update_db = UpdateDb()

        # Update db products
        update_db.run()


class UpdateDb:

    """ Class that manages to update the food products previously
     collected with the 'populate' command. """

    db_products = {}

    # Some needed data
    data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
            'image_small_url', 'image_front_url', 'stores',
            'ingredients_text', 'last_modified_t']

    url = "https://fr.openfoodfacts.org/cgi/search.pl?"

    def run(self):

        """ Main loop iterating through the categories of food given
         to the command. """

        # starting point
        self.get_data_from_db()
        for category in Category.objects.all():

            payload = {
                'tag_0': category.name,
                'tag_contains_0': 'contains',
                'tagtype_0': 'categories',
                'tag_1': 'fr',
                'tag_contains_1': 'contains',
                'tagtype_1': 'lang',
                'sort_by': 'unique_scans_n',
                'page_size': 100,
                'action': 'process',
                'json': True
            }

            response = requests.get(self.url, params=payload)

            products = response.json()['products']

            for product in products:
                if self.check_fields(product):
                    if self.check_product_code(product['code']):
                        product = self.cleaned_data(product)
                        self.update_product(product)

    def check_fields(self, product):
        """
        Return True if the data contains all the fields required for
         each product.
        """
        if all(product.get(i, None) for i in self.data):
            return True
        else:
            return False

    def get_data_from_db(self):
        """
        Filling a dictionnary with barcode as key and product object
         as value for each product in database.
        """
        for product in Product.objects.all():
            self.db_products[product.code] = product
        return self.db_products

    def check_product_code(self, code):
        """
        Check if the product's code is inside our database food.
        """
        if code in self.db_products:
            return True
        else:
            return False

    def cleaned_data(self, product):
        """
        Check field 'ingredients_text' of the product and remove all
         the undesired stuff.
        """
        a = product['ingredients_text']
        a = a.replace('_', '').strip()
        product['ingredients_text'] = a
        return product

    def update_product(self, product):
        """
        Update fields of our products with new informations.
        """
        product_to_update = self.db_products[product['code']]
        for field in self.data:
            setattr(product_to_update, field, product[field])
            product_to_update.save()

