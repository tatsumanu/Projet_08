from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


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
