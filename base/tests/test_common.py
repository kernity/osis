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
from django.core.urlresolvers import reverse


class CommonViewTestNoData(TestCase):
    prefix_login_url = "/login/?next="
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
        pass

    def testHome(self):
        test_accessibility_non_logged_user(self, 'home')

    def testStudies(self):
        test_accessibility_non_logged_user(self, 'studies')

    def testAssessments(self):
        test_accessibility_non_logged_user(self, 'assessments')

    def testCatalog(self):
        test_accessibility_non_logged_user(self, 'catalog')

    def testData(self):
        test_accessibility_non_logged_user(self, 'data')

    def testdataMaintenance(self):
        test_accessibility_non_logged_user(self, 'data_maintenance')

    def testAcademicYear(self):
        test_accessibility_non_logged_user(self, 'academic_year')

    def testStorage(self):
        test_accessibility_non_logged_user(self, 'storage')

    def testFiles(self):
        test_accessibility_non_logged_user(self, 'files')

    def testFilesSearch(self):
        test_accessibility_non_logged_user(self, 'files_search')

    def testDocumentFileRead(self):
        test_accessibility_non_logged_user(self, 'document_file_read', args=[1])


def test_accessibility_non_logged_user(instance, request_url, args=None):
    """
    Routine to check accessibility to non logged user.
    A non logged user should be redirected to the login page.
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url to request
    :param args: arguments to pass to the url (a list)
    :return:
    """
    c = Client()

    response = c.get(reverse(request_url, args=args))
    expected_url = get_login_url(instance, reverse(request_url, args=args))

    instance.assertRedirects(response, expected_url)  # check redirection to login url


def get_login_url(instance, request_url):
    """
    Return the login url which is of the form:
    /login/?next=request_url
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url requested
    :return: the login url corresponding to the requested url
    """
    return "".join([instance.prefix_login_url, request_url])
