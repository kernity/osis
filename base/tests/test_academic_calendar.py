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


class AcademicCalendarViewTestNoData(TestCase):
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

    def testAcademicCalendars(self):
        name_url = 'academic_calendars'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testAcademicCalendarsSearch(self):
        name_url = 'academic_calendars_search'
        test_accessibility_non_logged_user(self, name_url, data={'academic_year': '1'})
        test_accessibility_logged_user(self, name_url, data={'academic_year': '1'})

    def testAcademicCalendarRead(self):
        name_url = 'academic_calendar_read'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testAcademicCalendarNew(self):  # TODO ADD FORMS
        name_url = 'academic_calendar_save_new'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testAcademicCalendarSave(self):     # TODO ADD FORMS
        name_url = 'academic_calendar_save'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testAcademicCalendarEdit(self):
        name_url = 'academic_calendar_edit'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testAcademicCalendarCreate(self):
        name_url = 'academic_calendar_create'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)
