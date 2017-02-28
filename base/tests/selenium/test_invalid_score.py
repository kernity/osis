import selenium
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

url = "http://localhost:8000/studies/"


class InvalidScoreTest(StaticLiveServerTestCase):
    fixtures = ['academic_year.json', 'academic_calendar.json', 'session_exam.json',
                'offer_year_calendar.json', 'attribution.json', 'offer_year.json',
                'offer_enrollment.json', 'learning_unit_enrollment.json', 'exam_enrollment.json']
    #main_fixture = ['learning_unit_year.json']  # pour cours evec note décimale perilise ou pas
    @classmethod
    def setUpClass(self):
        super(InvalidScoreTest, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(15)
        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(self):
        self.selenium.quit()
        super(InvalidScoreTest,  self).tearDownClass()


    def test_encoding_home_page_title(self):
        #Tests that Home is loading properly
         self.selenium.get( self.selenium.get(url+"assessments/online/62504"))
         self.assertIn('OSIS',  self.selenium.title)


    def test_is_invalid_score(self):
         self.test_encoding_home_page_title()
         self.selenium.get(url + "assessments/scores_encoding/search/?offer_year_id=2359")
         self.selenium.find_element_by_id("lnk_LCHM1111").click()
         self.selenium.implicitly_wait(10)  # seconds
         self.selenium.find_element_by_id("num_score_1374160").clear()
         self.selenium.find_element_by_id("num_score_1374160").send_keys("14.5")   #course with ECTS < 15 ; tester aussi pour
         self.selenium.find_element_by_id("bt_save_online_encoding_up").click()
         self.alert_and_close_alert()

         self.selenium.find_element_by_id("num_score_1374107").clear()
         self.selenium.find_element_by_id("num_score_1374107").send_keys("-1")  #score < 0
         self.selenium.find_element_by_id("bt_save_online_encoding_up").click()
         self.alert_and_close_alert()

         self.selenium.find_element_by_id("num_score_1374160").clear()
         self.selenium.find_element_by_id("num_score_1374160").send_keys("22")  #score > 20
         self.selenium.find_element_by_id("bt_save_online_encoding_up").click()
         self.alert_and_close_alert()

         self.selenium.find_element_by_id("num_score_1374046").clear()
         self.selenium.find_element_by_id("num_score_1374046").send_keys("a5")    #not score
         self.selenium.find_element_by_id("bt_save_online_encoding_up").click()
        # self.alert_and_close_alert()





    def alert_and_close_alert(self):
        alert =  self.selenium.switch_to_alert()
        alert_text = alert.text
        self.selenium.execute_script(alert_text)
        time.sleep(5)
        alert.accept()
