# -*-coding:'utf8'-*-

import os
import time
import django
import requests
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet_08.settings')

django.setup()

from Nutella.models import Product, Category


def main():

    # Some needed data
    category = ''
    nb_page = 1
    page_size = 100

    categories = ['biscuits_et_gateaux', 'pizzas_tartes_salées_et_quiches',
                  'boissons', 'pates_a_tartiner', 'produits_laitiers',
                  'charcuteries', 'conserves']

    data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
            'image_small_url', 'image_front_url', 'stores', 'ingredients_text']

    url = "https://fr.openfoodfacts.org/cgi/search.pl?"

    payload = {
        'tag_0': category,
        'tag_contains_0': 'contains',
        'tagtype_0': 'categories',
        'tag_1': 'fr',
        'tag_contains_1': 'contains',
        'tagtype_1': 'lang',
        'sort_by': 'unique_scans_n',
        'page_size': page_size,
        'action': 'process',
        'json': True
    }

    # starting point
    t1 = time.time()

    # main loop iterating through the categories of food given to the script
    for category in tqdm(categories):

        # inserting categories in category table
        cat = add_category(category)

        print('Collecting products from {} category'.format(category))

        response = requests.get(url, params=payload)

        products = response.json()['products']

        for elt in products:
            if all(elt.get(i, None) for i in data):
                add_product(name=elt['product_name'],
                            category=cat,
                            brand=elt['brands'],
                            nutri_grade=elt['nutrition_grade_fr'],
                            url=elt['url'],
                            stores=elt['stores'],
                            ingredients=elt['ingredients_text'],
                            image_small=elt['image_small_url'],
                            image_xl=elt['image_front_url']
                            )

    print("Operations completed successfully in {:02f}\
 seconds!".format((time.time() - t1)))


def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


def add_product(name, brand, nutri_grade, url, stores,
                ingredients, image_small, image_xl, category):
    p = Product.objects.get_or_create(name=name, category=category)[0]
    p.brand = brand
    p.nutri_grade = nutri_grade
    p.url = url
    p.stores = stores
    p.ingredients = ingredients
    p.image_small = image_small
    p.image_xl = image_xl
    p.save()
    return p


if __name__ == "__main__":
    print("Starting collection!")
    main()
