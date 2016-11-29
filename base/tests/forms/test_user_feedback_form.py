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
from django.test import TestCase
from base.forms.user_feedback_form import UserFeebackForm


class UserFeedbackFormValidationTest(TestCase):

    def get_valid_data(self):
        return {
            'sentry_message_id': 'fc6d8c0c43fc4630ad850ee518f1b9d0',
            'user_name': 'Valid Name',
            'email': 'valid_email@test.org',
            'message': 'This is a Valid Message'
        }

    def test_valid_data(self):
        form = UserFeebackForm(self.get_valid_data())
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = self.__get_invalid_data('email', 'invalid_Email')
        self.__assert_false_field(form, 'email')

    def test_email_is_none(self):
        form = self.__get_invalid_data('email', None)
        self.__assert_false_field(form, 'email')

    def test_user_name_is_none(self):
        form = self.__get_invalid_data('user_name', None)
        self.__assert_false_field(form, 'user_name')

    def test_message_is_none(self):
        form = self.__get_invalid_data('message', None)
        self.__assert_false_field(form, 'message')

    def test_sentry_message_id_is_none(self):
        form = self.__get_invalid_data('sentry_message_id', None)
        self.__assert_false_field(form, 'sentry_message_id')

    def test_sentry_message_too_short(self):
        form = self.__get_invalid_data('sentry_message_id', '123')
        self.__assert_false_field(form, 'sentry_message_id')

    def test_sentry_message_too_long(self):
        form = self.__get_invalid_data('sentry_message_id', 'fc6d8c0c43fc4630ad850ee518f1b9d0fc6d8c0c43fc4630ad850ee')
        self.__assert_false_field(form, 'sentry_message_id')

    def __assert_false_field(self, form, field_name):
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors.get(field_name) is not None)

    def __get_invalid_data(self, invalid_field_name, field_invalid_data):
        invalid_data = self.get_valid_data()
        invalid_data[invalid_field_name] = field_invalid_data
        form = UserFeebackForm(invalid_data)
        return form