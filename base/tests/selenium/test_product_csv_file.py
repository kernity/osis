
import csv
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


url = "https:// dev.osis.uclouvain.be/studies /"
justification_code = 'AT?'

class ScoreOrJustificationTest(StaticLiveServerTestCase):
    fixtures = ['academic_year.json', 'academic_calendar.json', 'session_exam.json',
                'offer_year_calendar.json', 'attribution.json', 'offer_year.json',
                'offer_enrollment.json', 'learning_unit_enrollment.json', 'exam_enrollment.json']

    # main_fixture = ['exam_enrolment.json']  # pour cours evec note décimale perilise ou pas

    def setUpClass(self):
        super(ScoreOrJustificationTest, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(15)

        # Add records to test DB, to replace this code by django command
        # populate_test_db()


    def tearDownClass(self):
        self.selenium.quit()
        super(ScoreOrJustificationTest, self).tearDownClass()



    def test_is_invalid_score(self):
        self.selenium.get(self.selenium.get(url + "assessments/scores_encoding/"))
        self.assertIn('OSIS', self.selenium.title)
        self.selenium.implicitly_wait(10)  # seconds
        self.selenium.find_element_by_id("lnk_highlight_studies/assessments/scores_encoding/").click()
        self.selenium.implicitly_wait(5)
        self.assertIn("https://dev.osis.uclouvain.be/studies/assessments/scores_encoding/online/65418/", self.selenium.current_url)
        self.selenium.find_element_by_id("lnk_LENVI2199").click()
        self.selenium.implicitly_wait(5)
        self.selenium.find_element_by_id("lnk_scores_excel").click()
        self.selenium.implicitly_wait(3000)   #le temps de sauvegarde
        csvFile = "session_2016_1_LCHM1111.csv"
        delimiter = '\t'
        f = open(csvFile, 'r')
        reader = csv.reader(f, delimiter)
        ncol = len(next(reader))  # Read first line and count columns
        self.assertEqual(ncol,10) #nb column Année académique,	Session,	Unité d'enseignement,	Programme,	Noma,	Nom,	Prénom,	Note chiffrée,	Justification,	Date de fin
        f.seek(0)  # go back to beginning of file
        reader = csv.reader(f)
        i = 0
        while i < 9:
            next(reader, None)  # l'entête et les 8 lignes : session, anac, date de production, ..... (au total 9 lignes à sauter)
        row_count = sum(1 for row in reader)  # commencer à compter
        self.assertEqual(row_count,453)

        f.seek(0)  # go back to beginning of file
        i = 0
        while i < 9:
            next(reader,
                 None)  # l'entete et les 8 lignes : session, anac, date de production, ..... (au total 9 lignes à sauter)
        for row in reader:
            score = row[7]
            justification = row[8]
            if score:
              self.assertGreaterEqual(score,0)
              self.assertLessEqual(score, 20)
            elif justification:
                self.assertIn(justification, justification_code)
     
        self.alert_and_close_alert()


    def alert_and_close_alert(self):
        alert = self.selenium.switch_to_alert()
        alert_text = alert.text
        self.selenium.execute_script(alert_text)
        time.sleep(5)
        alert.accept()


