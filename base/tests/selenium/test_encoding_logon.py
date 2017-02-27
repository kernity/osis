import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

loginEmpty =''
passwordEmpty=''
loginWrong='evase'
passwordWrong='evase'
loginCorrect='enizeyimana'
passwordCorrect = 'fffffbrrrrrrrrelfffzzddafmifdf'

class TestLogonScoreEnconding(StaticLiveServerTestCase):
    def setUp(self):
        super(TestLogonScoreEnconding, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)



    def open_login_page(self):
        url = 'https://dev.osis.uclouvain.be/'
        self.selenium.get(url)
        self.selenium.implicitly_wait(10) # seconds

        login_id = self.selenium.find_element_by_id('username')
        self.assertIsNotNone(login_id)
        pass_id = self.selenium.find_element_by_id('password')
        self.assertIsNotNone(pass_id)

        username_field = self.selenium.find_element_by_id('username')
        username_field.send_keys(loginEmpty)
        password_field = self.selenium.find_element_by_id('password')
        password_field.send_keys(passwordEmpty)
        submit = 'input[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('cannot be identified', body.text)
        time.sleep(5)


        username_field = self.selenium.find_element_by_id('username')
        username_field.send_keys(loginWrong)
        password_field = self.selenium.find_element_by_id('password')
        password_field.send_keys(passwordWrong)
        submit = 'input[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('cannot be identified', body.text)
        time.sleep(5)

        username_field = self.selenium.find_element_by_id('username')
        username_field.send_keys(loginWrong)
        password_field = self.selenium.find_element_by_id('password')
        password_field.send_keys(passwordCorrect)
        submit = 'input[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('cannot be identified', body.text)
        time.sleep(5)

        username_field = self.selenium.find_element_by_id('username')
        username_field.send_keys(loginCorrect)
        password_field = self.selenium.find_element_by_id('password')
        password_field.send_keys(passwordWrong)
        submit = 'input[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('cannot be identified', body.text)
        time.sleep(5)

        username_field = self.selenium.find_element_by_id('username')
        username_field.send_keys(loginCorrect)
        password_field = self.selenium.find_element_by_id('password')
        password_field.send_keys(passwordCorrect)
        submit = 'input[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Evase', body.text)
        time.sleep(5)

    def tearDown(self):
        super(TestLogonScoreEnconding, self).tearDown()
        self.selenium.quit()


#if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestLogonScoreEnconding)
    #runner = unittest.TextTestRunner()
    #runner.run(suite)




