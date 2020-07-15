from django.test import LiveServerTestCase
from selenium import webdriver
from django.conf import settings


class ContactViewTest(LiveServerTestCase):
    """
    A test class working with selenium. Chrome should be installed as well
     as the chromedriver.
    """
    
    homepage_url = None
	email = settings.EMAIL_USER
	message = 'This is a test message for the ContactView'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(20)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def going_to_contact_page(self):
        self.selenium.get('http://127.0.0.1:8000')
        self.homepage_url = self.selenium.current_url
        self.selenium.get('http://127.0.0.1:8000/contact/')

    def test_can_send_mail_with_selenium(self):
        # Testing contact page with selenium
        self.going_to_contact_page()
        email_form = self.selenium.find_element_by_name('email')
        email_form.send_keys(self.email)
        message_form = self.selenium.find_element_by_name('message')
        message_form.send_keys(self.message)
        message_form.submit()

        # Check that we are now on homepage
        self.assertEquals(self.homepage_url+'#', self.selenium.current_url)
