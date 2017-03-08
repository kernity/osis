##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from base.tests.models import test_person, test_student
from internship.tests.models import test_internship_offer, test_internship_speciality, test_organization, \
    test_internship_choice
from internship.models import internship_choice as mdl_internship_choice
from django.core.exceptions import ValidationError


class TestModifyStudentChoices(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("username", "test@test.com", "passtest")
        self.user.first_name = "first_name"
        self.user.last_name = "last_name"
        self.user.save()
        add_permission(self.user, "is_internship_manager")
        self.person = test_person.create_person_with_user(self.user)
        self.c = Client()
        self.c.force_login(self.user)

        self.student = test_student.create_student("first", "last", "64641200")

        self.speciality_1 = test_internship_speciality.create_speciality(name="urgence")
        self.speciality_2 = test_internship_speciality.create_speciality(name="chirurgie")

        self.organization_1 = test_organization.create_organization(reference="01")
        self.organization_2 = test_organization.create_organization(reference="02")
        self.organization_3 = test_organization.create_organization(reference="03")
        self.organization_4 = test_organization.create_organization(reference="04")
        self.organization_5 = test_organization.create_organization(reference="05")

        self.offer_1 = test_internship_offer.create_specific_internship_offer(self.organization_1, self.speciality_1)
        self.offer_2 = test_internship_offer.create_specific_internship_offer(self.organization_2, self.speciality_1)
        self.offer_3 = test_internship_offer.create_specific_internship_offer(self.organization_3, self.speciality_1)
        self.offer_4 = test_internship_offer.create_specific_internship_offer(self.organization_4, self.speciality_1)

        self.offer_5 = test_internship_offer.create_specific_internship_offer(self.organization_1, self.speciality_2)
        self.offer_6 = test_internship_offer.create_specific_internship_offer(self.organization_5, self.speciality_2)

    def test_with_zero_choices(self):
        selection_url = reverse("specific_internship_student_modification", kwargs={'internship_id': 1,
                                                                        'speciality_id': self.speciality_2.id,
                                                                        'registration_id': self.student.registration_id}
                                )
        self.assertRaises(ValidationError, self.c.post, selection_url, {})

    def test_with_one_choice(self):
        selection_url = reverse("specific_internship_student_modification", kwargs={'internship_id': 1,
                                                                        'speciality_id': self.speciality_2.id,
                                                                        'registration_id': self.student.registration_id}
                                )
        self.c.post(selection_url, data={'form-TOTAL_FORMS': '2',
                                         'form-INITIAL_FORMS': '0',
                                         'form-MIN_NUM_FORMS': '2',
                                         'form-MAX_NUM_FORMS': '2',
                                         'form-0-offer': str(self.offer_5.id),
                                         'form-0-preference': '1',
                                         'form-0-priority': 'on',
                                         'form-1-offer': str(self.offer_6.id),
                                         'form-1-preference': '0',
                                         'form-1-priority': 'off'})
        choices = list(mdl_internship_choice.search_by_student_or_choice(student=self.student))

        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0].organization, self.organization_1)
        self.assertEqual(choices[0].speciality, self.speciality_2)
        self.assertEqual(choices[0].internship_choice, 1)
        self.assertEqual(choices[0].choice, 1)
        self.assertTrue(choices[0].priority)

    def test_with_multiple_choice(self):
        selection_url = reverse("specific_internship_student_modification", kwargs={'internship_id': 1,
                                                                        'speciality_id': self.speciality_1.id,
                                                                        'registration_id': self.student.registration_id}
                                )
        self.c.post(selection_url, data={'form-TOTAL_FORMS': '4',
                                         'form-INITIAL_FORMS': '0',
                                         'form-MIN_NUM_FORMS': '4',
                                         'form-MAX_NUM_FORMS': '4',
                                         'form-0-offer': str(self.offer_1.id),
                                         'form-0-preference': '1',
                                         'form-0-priority': 'off',
                                         'form-1-offer': str(self.offer_2.id),
                                         'form-1-preference': '2',
                                         'form-1-priority': 'off',
                                         'form-2-offer': str(self.offer_3.id),
                                         'form-2-preference': '3',
                                         'form-2-priority': 'off',
                                         'form-3-offer': str(self.offer_4.id),
                                         'form-3-preference': '4',
                                         'form-3-priority': 'off',
                                         })
        choices = list(mdl_internship_choice.search_by_student_or_choice(student=self.student))
        self.assertEqual(len(choices), 4)

        self.c.post(selection_url, data={'form-TOTAL_FORMS': '4',
                                         'form-INITIAL_FORMS': '0',
                                         'form-MIN_NUM_FORMS': '4',
                                         'form-MAX_NUM_FORMS': '4',
                                         'form-0-offer': str(self.offer_1.id),
                                         'form-0-preference': '1',
                                         'form-0-priority': 'off',
                                         'form-1-offer': str(self.offer_2.id),
                                         'form-1-preference': '0',
                                         'form-1-priority': 'off',
                                         'form-2-offer': str(self.offer_3.id),
                                         'form-2-preference': '2',
                                         'form-2-priority': 'off',
                                         'form-3-offer': str(self.offer_4.id),
                                         'form-3-preference': '0',
                                         'form-3-priority': 'off',
                                         })
        choices = list(mdl_internship_choice.search_by_student_or_choice(student=self.student))
        self.assertEqual(len(choices), 2)

    def test_with_incorrect_speciality(self):
        selection_url = reverse("specific_internship_student_modification", kwargs={'internship_id': 1,
                                                                        'speciality_id': self.speciality_1.id,
                                                                        'registration_id': self.student.registration_id}
                                )
        self.c.post(selection_url, data={'form-TOTAL_FORMS': '4',
                                         'form-INITIAL_FORMS': '0',
                                         'form-MIN_NUM_FORMS': '4',
                                         'form-MAX_NUM_FORMS': '4',
                                         'form-0-offer': str(self.offer_1.id),
                                         'form-0-preference': '1',
                                         'form-0-priority': 'on',
                                         'form-1-offer': str(self.offer_5.id),
                                         'form-1-preference': '2',
                                         'form-1-priority': 'on',
                                         'form-2-offer': str(self.offer_3.id),
                                         'form-2-preference': '0',
                                         'form-2-priority': 'on',
                                         'form-3-offer': str(self.offer_4.id),
                                         'form-3-preference': '0',
                                         'form-3-priority': 'on',
                                         })
        choices = list(mdl_internship_choice.search_by_student_or_choice(student=self.student))
        self.assertEqual(len(choices), 1)

    def test_replace_previous_choices(self):
        previous_choice = test_internship_choice.create_internship_choice(test_organization.create_organization(),
                                                                          self.student, self.speciality_1, 2)
        selection_url = reverse("specific_internship_student_modification", kwargs={'internship_id': 2,
                                                                        'speciality_id': self.speciality_2.id,
                                                                        'registration_id': self.student.registration_id}
                                )
        self.c.post(selection_url, data={'form-TOTAL_FORMS': '2',
                                         'form-INITIAL_FORMS': '0',
                                         'form-MIN_NUM_FORMS': '2',
                                         'form-MAX_NUM_FORMS': '2',
                                         'form-0-offer': str(self.offer_5.id),
                                         'form-0-preference': '1',
                                         'form-0-priority': 'on',
                                         'form-1-offer': str(self.offer_6.id),
                                         'form-1-preference': '0',
                                         'form-1-priority': 'off'})
        choices = list(mdl_internship_choice.search_by_student_or_choice(student=self.student))
        self.assertEqual(len(choices), 1)
        self.assertNotEqual(previous_choice, choices[0])


def add_permission(user, codename):
    perm = get_permission(codename)
    user.user_permissions.add(perm)


def get_permission(codename):
    return Permission.objects.get(codename=codename)