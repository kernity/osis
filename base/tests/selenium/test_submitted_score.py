import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

url = "https:// dev.osis.uclouvain.be/studies/"

class SubmitScoreTest(StaticLiveServerTestCase):
    fixtures = ['tutor.json','attribution.json']

    @classmethod
    def setUpClass(cls):
        super(SubmitScoreTest, cls).setUpClass()
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(15)
        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(cls):
        cls.driver.quit()
        super(SubmitScoreTest, cls).tearDownClass()


    def test_encoding_home_page_title(cls):
        #Tests that Home is loading properly
        cls.driver.get(cls.driver.get(url+" assessments/online/62504"))
        cls.assertIn('OSIS', cls.driver.title)


    def test_submit_scores(cls):
        cls.driver.get(url + "assessments/scores_encoding/search/?offer_year_id=2359")
        cls.driver.find_element_by_id("lnk_score_encoding").click()
        cls.driver.find_element_by_id("lnk_LCHM1111").click()
        cls.assertIn('pas encore été soumises', cls.driver.find_element_by_tag_name('body'))
        time.sleep(5)
        cls.driver.find_element_by_id ("bt_score_submission_modal").click()
        cls.driver.find_element_by_id("lnk_post_scores_submission_btn").click()
        cls.driver.find_element_by_id("lnk_post_scores_submission_btn").click()
        cls.driver.implicitly_wait(3)
        cls.assertNotIn('pas encore été soumises', cls.driver.find_element_by_tag_name('body'))
        cls.alert_and_close_alert()


    def alert_and_close_alert(self):
        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        self.driver.execute_script(alert_text)
        time.sleep(5)
        alert.accept()
