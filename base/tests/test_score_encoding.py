##############################################################################
#
# OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

# Test for accessibility of the view.


from django.test import TestCase, Client
from base.tests.utils import test_accessibility_logged_user, test_accessibility_non_logged_user
from django.contrib.auth.models import User


class OrganizationViewTestNoData(TestCase):  # TODO ensure that we're in a scores encoding period
    fixtures = [
        'user.json',
        'person.json',
        'tutor.json',
        'student.json',
        'academic_year.json',
        'academic_calendar.json',
        'learning_unit.json',
        'learning_unit_year.json',
        'messages_templates.json',
        'offer.json',
        'organization.json',
        'structure.json',
        'attribution.json',
        'continent.json',
        'currency.json',
        'country.json',
        'decree.json',
        'domain.json',
        'education_institution.json',
        'language.json',
        'continent.json',
        'person_address.json',
        'organization_address.json',
        'offer_year.json',
        'offer_year_calendar.json',
        'session_exam.json',
        'program_manager.json',
        'offer_enrollment.json',
        'learning_unit_enrollment.json',
        'exam_enrollment.json'
    ]

    def setUp(self):
        # Logged a professor
        user_to_log = User.objects.get(pk=4)  # user philippe
        self.logged_client = Client()
        self.logged_client.force_login(user=user_to_log)

    def testOutsideScoresEncodingsPeriod(self):
        name_url = 'outside_scores_encodings_period'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testScoresEncoding(self):
        name_url = 'scores_encoding'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testOnlineEncoding(self):
        name_url = 'online_encoding'
        args=[1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testOnlineEncodingForm(self):   # TODO ADD FORM
        name_url = 'online_encoding_form'
        args = [1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testOnlineDoubleEncodingForm(self):   # TODO ADD FORM
        name_url = 'online_double_encoding_form'
        args = [1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testOnlineDoubleEncodingValidation(self):   # TODO ADD FORM
        name_url = 'online_double_encoding_validation'
        args = [1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testOnlineEncodingSubmission(self):   # TODO ADD FORM
        name_url = 'online_encoding_submission'
        args = [1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testNotesPrinting(self):  # TODO check arguments
        name_url = 'notes_printing'
        args = [1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testNotesPrintingAll(self):  # TODO check arguments
        name_url = 'notes_printing_all'
        args = [1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)

    def testExportXls(self):
        name_url = 'scores_encoding_download'
        args = [1, 1]
        test_accessibility_non_logged_user(self, name_url, args=args)
        test_accessibility_logged_user(self, name_url, args=args)
