from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


url = "https:// dev.osis.uclouvain.be/studies /"

class ProgresBarScoresTest(StaticLiveServerTestCase):
    fixtures = ['academic_year.json', 'academic_calendar.json', 'session_exam.json',
                'offer_year_calendar.json', 'attribution.json', 'offer_year.json',
                'offer_enrollment.json', 'learning_unit_enrollment.json', 'exam_enrollment.json']

    @classmethod
    def setUpClass(cls):
        super(ProgresBarScoresTest, cls).setUpClass()
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(15)
        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(cls):
        cls.driver.quit()
        super(ProgresBarScoresTest, cls).tearDownClass()


    def test_encoding_home_page_title(cls):

        #Tests that Home is loading properly
        cls.driver.get(cls.driver.get(url+" assessments /"))
        cls.assertIn('OSIS', cls.driver.title)

    def test_is_present_progres_bar(cls):
        # self.driver.get("https: // dev.osis.uclouvain.be / studies / assessments /")
        cls.test_encoding_home_page_title()
        present = cls.driver.find_element_by_class_name('progress')
        cls.assertIsNotNone(present)
        cls.driver.implicitly_wait(30)
