from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class RegisterLogoutThenLoginLogoutTest(LiveServerTestCase):
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

    def test_can_register_with_selenium(self):
        # Trying to register as a new user from homepage
        self.selenium.get('http://127.0.0.1:8000')
        register = self.selenium.find_element_by_id('create')
        ActionChains(self.selenium).move_to_element(register).click().perform()

        # Test that we are on register page
        self.assertTrue('Créer un compte' in self.selenium.page_source)

        email_form = self.selenium.find_element_by_name('email')
        email_form.send_keys('testname@test.fr')
        name_form = self.selenium.find_element_by_name('name')
        name_form.send_keys('testname')
        pass1_form = self.selenium.find_element_by_name('password1')
        pass1_form.send_keys('testname_pass')
        pass2_form = self.selenium.find_element_by_name('password2')
        pass2_form.send_keys('testname_pass')
        pass2_form.submit()

        # Checking that we are logged in with the correct informations
        account = self.selenium.find_element_by_id('account')
        ActionChains(self.selenium).move_to_element(account).click().perform()
        self.assertTrue('testname@test.fr' in self.selenium.page_source)

        # Finally loging out
        logout_btn = self.selenium.find_element_by_id('logout')
        ActionChains(self.selenium).move_to_element(logout_btn).click().perform()

    def test_login_with_selenium(self):
        # Now login again with informations provided when registering
        self.selenium.get('http://127.0.0.1:8000')
        login_btn = self.selenium.find_element_by_id('login')
        ActionChains(self.selenium).move_to_element(login_btn).click().perform()
        username_form = self.selenium.find_element_by_name('username')
        username_form.send_keys('testname@test.fr')
        pass_form = self.selenium.find_element_by_name('password')
        pass_form.send_keys('testname_pass')
        pass_form.submit()

        # Checking that we are logged in with the correct informations
        account = self.selenium.find_element_by_id('account')
        ActionChains(self.selenium).move_to_element(account).click().perform()
        self.assertTrue('testname@test.fr' in self.selenium.page_source)

        # If all works we can now logout again and quit!
        logout_btn = self.selenium.find_element_by_id('logout')
        ActionChains(self.selenium).move_to_element(logout_btn).click().perform()
