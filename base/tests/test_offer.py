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


class OfferViewTestNoData(TestCase):
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

    def testOffers(self):
        name_url = 'offers'
        test_accessibility_non_logged_user(self, name_url)
        test_accessibility_logged_user(self, name_url)

    def testOffersSearch(self):
        name_url = 'offers_search'
        test_accessibility_non_logged_user(self, name_url, data={'entity_acronym': '', 'academic_year': '1',
                                                             'code': ''})
        test_accessibility_logged_user(self, name_url, data={'entity_acronym': '', 'academic_year': '1',
                                                             'code': ''})

    def testOfferRead(self):
        name_url = 'offer_read'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testScoreEncoding(self):
        name_url = 'offer_score_encoding'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testOfferYearCalendarRead(self):
        name_url = 'offer_year_calendar_read'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testOfferYearCalendarSave(self):
        name_url = 'offer_year_calendar_save'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])

    def testOfferYearCalendarEdit(self):
        name_url = 'offer_year_calendar_edit'
        test_accessibility_non_logged_user(self, name_url, args=[1])
        test_accessibility_logged_user(self, name_url, args=[1])


def test_accessibility_non_logged_user(instance, request_url, data=None, args=None):
    """
    Routine to check accessibility to non logged user.
    A non logged user should be redirected to the login page.
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url to request
    :param data: key-value pair for get request
    :param args: arguments to pass to the url (a list)
    :return:
    """
    c = instance.client

    response = c.get(reverse(request_url, args=args), data=data)
    expected_url = get_login_url(instance, reverse(request_url, args=args))  # TODO check if data is comprised

    instance.assertRedirects(response, expected_url)  # check redirection to login url


def test_accessibility_logged_user(instance, request_url, data=None, has_perm=True, args=None):
    """
    Routine to check accessibility to logged user.
    :param instance: a CommonViewTestNoData class instance
    :param request_url: url to request
    :param data: key-value pair for get request
    :param has_perm: boolean to know if the user has the right to access the url
    :param args: arguments to pass to the url (a list)
    :return:
    """
    c = instance.logged_client

    response = c.get(reverse(request_url, args=args), data=data)

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
