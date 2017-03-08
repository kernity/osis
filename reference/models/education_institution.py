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
from django.db import models
from reference.enums import education_institution_type, education_institution_national_comunity as nat_community
from django.core import serializers
from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin


class EducationInstitutionAdmin(SerializableModelAdmin):
    list_display = ('name', 'institution_type', 'country', 'adhoc')
    search_fields = ['name']
    list_filter = ('institution_type',)


class EducationInstitution(SerializableModel):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    institution_type = models.CharField(max_length=25, choices=education_institution_type.INSTITUTION_TYPE)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    country = models.ForeignKey('reference.Country', blank=True, null=True)
    national_community = models.CharField(max_length=20, choices=nat_community.NATIONAL_COMMUNITY_TYPES, blank=True, null=True)
    adhoc = models.BooleanField(default=True)
    address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


def serialize_list(list_education_institutions):
    """
    Serialize a list of student objects using the json format.
    Use to send data to osis-portal.
    :param list_education_institutions: a list of "EducationInstitution" objects
    :return: the serialized list (a json)
    """
    fields = ('id', 'name', 'institution_type', 'postal_code', 'city', 'country',
              'national_community', 'adhoc')
    return serializers.serialize("json", list_education_institutions, fields=fields)
