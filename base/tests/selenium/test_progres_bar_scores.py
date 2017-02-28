from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


url = "http://localhost:8000/studies/"

class ProgresBarScoresTest(StaticLiveServerTestCase):
    fixtures = ['academic_year.json', 'academic_calendar.json', 'session_exam.json',
                'offer_year_calendar.json', 'attribution.json', 'offer_year.json',
                'offer_enrollment.json', 'learning_unit_enrollment.json', 'exam_enrollment.json']

    @classmethod
    def setUpClass(self):
        super(ProgresBarScoresTest, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(15)
        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(self):
        self.selenium.quit()
        super(ProgresBarScoresTest, self).tearDownClass()


    def test_encoding_home_page_title(self):

        #Tests that Home is loading properly
        self.selenium.get(self.selenium.get(url+"assessments /"))
        self.assertIn('OSIS', self.selenium.title)

    def test_is_present_progres_bar(self):
        # self.driver.get("https: // dev.osis.uclouvain.be / studies / assessments /")
        self.test_encoding_home_page_title()
        present = self.selenium.find_element_by_class_name('progress')
        self.assertIsNotNone(present)
        self.selenium.implicitly_wait(30)
