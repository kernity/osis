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
from django.contrib.auth.models import User


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
        # Logged a professor
        user_to_log = User.objects.get(pk=4)  # user philippe
        self.logged_client = Client()
        self.logged_client.force_login(user=user_to_log)

    def testHome(self):
        name_url = 'home'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testStudies(self):
        name_url = 'studies'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testAssessments(self):
        name_url = 'assessments'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testCatalog(self):
        name_url = 'catalog'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testData(self):
        name_url = 'data'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url, has_perm=False)

    def testDataMaintenance(self):
        name_url = 'data_maintenance'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url, has_perm=False)

    def testAcademicYear(self):
        name_url = 'academic_year'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testStorage(self):
        name_url = 'storage'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url, has_perm=False)

    def testFiles(self):
        name_url = 'files'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url, has_perm=False)

    def testFilesSearch(self):
        name_url = 'files_search'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url, has_perm=False)

    def testDocumentFileRead(self):
        name_url = 'document_file_read'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1], has_perm=False)


def test_accessibility_non_logged_user(instance, request_url, args=None):
    """
    Routine to check accessibility to non logged user.
    A non logged user should be redirected to the login page.
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url to request
    :param args: arguments to pass to the url (a list)
    :return:
    """
    c = instance.client

    response = c.get(reverse(request_url, args=args))
    expected_url = get_login_url(instance, reverse(request_url, args=args))

    instance.assertRedirects(response, expected_url)  # check redirection to login url


def test_accessibility_logged_user(instance, request_url, has_perm=True, args=None):
    """
    Routine to check accessibility to logged user.
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url to request
    :param has_perm: boolean to know if the user has the right to access the url
    :param args: arguments to pass to the url (a list)
    :return:
    """
    c = instance.logged_client

    response = c.get(reverse(request_url, args=args))

    if not has_perm:    # an access denied should be showed and use of http error code 403 (forbidden)
        instance.assertTemplateUsed(response, "access_denied.html")
        instance.assertEquals(403, response.status_code)
    else:
        instance.assertEquals(200, response.status_code)


def get_login_url(instance, request_url):
    """
    Return the login url which is of the form:
    /login/?next=request_url
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url requested
    :return: the login url corresponding to the requested url
    """
    return "".join([instance.prefix_login_url, request_url])
