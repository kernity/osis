from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

url = "https:// dev.osis.uclouvain.be/studies/"


class CoursesPgmUserTest(StaticLiveServerTestCase):
    fixtures = ['academic_year.json', 'academic_calendar.json', 'session_exam.json',
                'offer_year_calendar.json', 'attribution.json', 'offer_year.json',
                ' offer_enrollment.json', ' learning_unit_year.json',
                'learning_unit_enrollment.json', 'exam_enrollment.json']

    def setUpClass(self):
        super(CoursesPgmUserTest, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)

        # Add records to test DB, to replace this code by django command
        # populate_test_db()

    def tearDownClass(self):
        self.selenium.quit()
        super(CoursesPgmUserTest, self).tearDownClass()




    #def test_encoding_home_page_title(self):
        #Tests that Home is loading properly
        #self.selenium.get(self.selenium.get(url+"assessments/"))
        #self.assertIn('OSIS', self.selenium.title)


    def test_is_present_courses_programm(self):
        # self.driver.get("https: // dev.osis.uclouvain.be / studies / assessments /")

        pge_depart = self.selenium.get(url) #depart
        #self.assertIn('OSIS', self.selenium.title)
        if not "OSIS" in self.selenium.title:
            raise Exception("Unable to load OSIS - Encoding module!")
        self.assertEqual(pge_depart.content, b"Encodage des notes - session")

        self.selenium.implicitly_wait(5)
        self.selenium.find_element_by_id("lnk_highlight_studies/assessments/scores_encoding/").click()
        self.assertIn("https://dev.osis.uclouvain.be/studies/assessments/scores_encoding/", self.selenium.current_url)
        pge_depart = self.selenium.get(self.selenium.current_url)  # depart
        self.assertEqual(pge_depart.content, b"Encodage des notes")
        self.selenium.implicitly_wait(5)

        self.selenium.find_element_by_id('lnk_score_encoding').click()
        self.selenium.implicitly_wait(3)
        self.assertIn("https://dev.osis.uclouvain.be/studies/assessments/scores_encoding/", self.selenium.current_url)
        #select pgm; show students
        self.selenium.find_element_by_id("slt_offer_list_selection").select_by_visible_text("CHIM11BA")
        self.selenium.find_element_by_id("bt_submit_scores_by_offer").click()
        self.selenium.implicitly_wait(15)
        self.selenium.find_element_by_id("slt_offer_list_selection").select_by_visible_text("BIOL11BA")
        self.selenium.find_element_by_id("bt_submit_scores_by_offer").click()
        self.selenium.implicitly_wait(15)
        self.selenium.find_element_by_id("slt_offer_list_selection").select_by_visible_text("ENVI2MS/G")
        self.selenium.find_element_by_id("bt_submit_scores_by_offer").click()
        self.selenium.implicitly_wait(15)

        #sql request : find scores saved / all enrollments in var
        #self.assertIn(var, self.driver.find_element_by_tag_name('body'))


