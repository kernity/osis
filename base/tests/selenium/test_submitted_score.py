import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

url = "https:// dev.osis.uclouvain.be/studies/"

class SubmitScoreTest(StaticLiveServerTestCase):
    fixtures = ['tutor.json','attribution.json']

    @classmethod
    def setUpClass(self):
        super(SubmitScoreTest, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(15)
        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(self):
        self.selenium.quit()
        super(SubmitScoreTest, self).tearDownClass()


    def test_encoding_home_page_title(self):
        #Tests that Home is loading properly
        self.selenium.get(self.selenium.get(url+" assessments/online/62504"))
        self.assertIn('OSIS', self.selenium.title)


    def test_submit_scores(self):
        self.selenium.get(url + "assessments/scores_encoding/search/?offer_year_id=2359")
        self.selenium.find_element_by_id("lnk_score_encoding").click()
        self.selenium.find_element_by_id("lnk_LCHM1111").click()
        self.assertIn('pas encore été soumises', self.selenium.find_element_by_tag_name('body'))
        time.sleep(5)
        self.selenium.find_element_by_id ("bt_score_submission_modal").click()
        self.selenium.find_element_by_id("lnk_post_scores_submission_btn").click()
        self.selenium.find_element_by_id("lnk_post_scores_submission_btn").click()
        self.selenium.implicitly_wait(3)
        self.assertNotIn('pas encore été soumises', cls.driver.find_element_by_tag_name('body'))
        self.alert_and_close_alert()


    def alert_and_close_alert(self):
        alert =self.selenium.switch_to_alert()
        alert_text = alert.text
        self.selenium.execute_script(alert_text)
        time.sleep(5)
        alert.accept()
