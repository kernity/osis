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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.db import models
from django.utils import timezone
from django.contrib import admin
from base.models import person
from django.utils.translation import ugettext_lazy as _


class Adviser(models.Model):
    TYPES_CHOICES = (
        ('MGR', _('Manager')),
        ('PRF', _('Professor')),
        )

    person = models.OneToOneField('base.Person',on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPES_CHOICES, default='PRF')
    email_accept = models.BooleanField(default=False)
    phone_accept = models.BooleanField(default=False)
    office_accept = models.BooleanField(default=False)
    comment=models.TextField(default='')

    def __str__(self):
        # We retrieve related person's informations (adaptation of __str__ method of base.Person)
        first_name = ""
        middle_name = ""
        last_name = ""
        if self.person.first_name :
            first_name = self.person.first_name
        if self.person.middle_name :
            middle_name = self.person.middle_name
        if self.person.last_name :
            last_name = self.person.last_name + ","

        return u"%s %s %s" % (last_name.upper(), first_name, middle_name)

    def find_by_person(a_person):
        adviser = Adviser.objects.get(person=a_person)
        return adviser
