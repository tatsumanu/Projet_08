# -*-coding:'utf8'-*-

import requests
import time
from tqdm import tqdm


def main():

    nb_page = 20
    page_size = 20
    categories = 5

    fill_db(nb_page, page_size, categories)


def fill_db(nb_page, page_size, categories):

    # starting point
    t1 = time.time()

    # inserting categories in category table
    add_category = "INSERT INTO category (category) VALUES (%s)"
    for cat in categories:
        cursor.execute(add_category, (cat,))


    # main loop iterating through the categories of food given to the script
    cpt = 1
    while cpt <= nb_page:
        print('Collecting products from {} categories \
    in page: {}/{}'.format(len(categories), cpt, nb_page))
        for cat in tqdm(categories):

            url = "https://fr.openfoodfacts.org/cgi/search.pl?"

            data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
                    'stores', 'ingredients_text']

            payload = {
                'tag_0': cat,
                'tag_contains_0': 'contains',
                'tagtype_0': 'categories',
                'tag_1': 'fr',
                'tag_contains_1': 'contains',
                'tagtype_1': 'lang',
                'sort_by': 'unique_scans_n',
                'page_size': page_size,
                'page': cpt,
                'action': 'process',
                'json': 1
            }

            response = requests.get(url, params=payload)

            products = response.json()['products']

            p = (tuple(elt.get(i, None) for i in data) for elt in products)

            for elt in p:
                elt += (categories.index(cat)+1),
                cursor.execute(add_product, elt)
        cpt += 1

    print("Operations completed successfully in {:02f}\
    seconds!".format((time.time() - t1)))

if __name__ == "__main__":

    main()
