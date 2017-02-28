
import selenium
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

url = "http://localhost:8000/"
justification='AT?'
class ScoreOrJustificationTest(StaticLiveServerTestCase):
    fixtures = ['academic_year.json', 'academic_calendar.json', 'session_exam.json',
                'offer_year_calendar.json', 'attribution.json', 'offer_year.json',
                'offer_enrollment.json', 'learning_unit_enrollment.json', 'exam_enrollment.json']

    # main_fixture = ['exam_enrollment.json','learning_unit_enrollment.json']  # pour cours evec note décimale perilise ou pas

    @classmethod
    def setUpClass(self):
        super(ScoreOrJustificationTest, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(15)
        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(self):
        self.selenium.quit()
        super(ScoreOrJustificationTest, cls).tearDownClass()



    def test_score_or_justification(self):
        self.selenium.get(url + "assessments/scores_encoding/search/?offer_year_id=2359")
        self.assertIn('OSIS', self.selenium.title)
        self.selenium.find_element_by_id("lnk_LCHM1111").click()
        self.selenium.implicitly_wait(10)  # seconds
        #score
        self.selenium.find_element_by_id("num_score_1374085").clear()
        self.selenium.find_element_by_id("num_score_1374085").send_keys("14")
        #and than justification
        self.selenium.find_element_by_id("slt_justification_score_1374085").select_by_visible_text("Absent")
        #justification
        self.selenium.find_element_by_id("slt_justification_score_1374160").select_by_visible_text("Tricherie")
        # and than score
        self.selenium.find_element_by_id("num_score_1374160").clear()
        self.selenium.find_element_by_id("num_score_1374160").send_keys("14.5")
        #justifications
        self.selenium.find_element_by_id("slt_justification_score_1374002").select_by_visible_text("Tricherie")
        self.selenium.find_element_by_id("slt_justification_score_1374107").select_by_visible_text("Note manquante")
        self.selenium.find_element_by_id("slt_justification_score_1373933").select_by_visible_text("Absent")
        self.selenium.find_element_by_id("slt_justification_score_1373885").select_by_visible_text("Tricherie")
        self.selenium.find_element_by_id("bt_save_online_encoding_up").click()
        self.selenium.find_element_by_id("bt_save_online_encoding_up").click()
        #cls.alert_and_close_alert()

        #cours acceptant une note décimale: credits >=15
        self.selenium.get(url + "studies/assessments/scores_encoding/")
        self.selenium.find_element_by_id("lnk_LENVI2199").click()
        self.selenium.find_element_by_id("lnk_encode").click()
        self.selenium.find_element_by_id("num_score_1418428").clear()
        self.selenium.find_element_by_id("num_score_1418428").send_keys("20.0")
        self.selenium.find_element_by_id("num_score_1418453").clear()
        self.selenium.find_element_by_id("num_score_1418453").send_keys("14.22")
        self.selenium.find_element_by_id("num_score_1418504").clear()
        self.selenium.find_element_by_id("num_score_1418504").send_keys("10.99999")
        self.selenium.find_element_by_id("num_score_1418474").clear()
        self.selenium.find_element_by_id("num_score_1418474").send_keys("-1.02")
        self.selenium.find_element_by_id("bt_save_online_encoding_down").click()
        self.selenium.find_element_by_id("num_score_1418474").clear()
        self.selenium.find_element_by_id("num_score_1418474").send_keys("6")
        self.selenium.find_element_by_id("bt_save_online_encoding_down").click()



    def alert_and_close_alert(self):
        alert = self.selenium .switch_to_alert()
        alert_text = alert.text
        self.selenium.execute_script(alert_text)
        time.sleep(5)
        alert.accept()
