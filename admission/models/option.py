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
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from osis_common.models.serializable_model import SerializableModel


class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'label', 'description')
    fieldsets = ((None, {'fields': ('label', 'value', 'order', 'description', 'question')}),)


class Option(SerializableModel):
    question = models.ForeignKey('Question')
    label = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return u"%s" % self.label


def find_by_question_id(question):
    try:
        return Option.objects.filter(question=question).order_by('label', 'description')
    except ObjectDoesNotExist:
        return None
