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
from django.contrib import admin
from django.db import models
from base import models as mdl
from base.models.serializable_model import SerializableModel
from dissertation.models.adviser import search_by_person
from dissertation.models.dissertation import Dissertation, STATUS_CHOICES

JUSTIFICATION_LINK = "_set_to_"


class DissertationUpdateAdmin(admin.ModelAdmin):
    list_display = ('dissertation', 'get_dissertation_author', 'status_from', 'status_to', 'person', 'created')
    raw_id_fields = ('person', 'dissertation')


class DissertationUpdate(SerializableModel):

    status_from = models.CharField(max_length=12, choices=STATUS_CHOICES, default='DRAFT')
    status_to = models.CharField(max_length=12, choices=STATUS_CHOICES, default='DRAFT')
    created = models.DateTimeField(auto_now_add=True)
    justification = models.TextField(default='')
    person = models.ForeignKey('base.Person')
    dissertation = models.ForeignKey(Dissertation)

    def __str__(self):
        desc = "%s / %s >> %s / %s" % (self.dissertation.title, self.status_from, self.status_to, str(self.created))
        return desc

    def get_dissertation_author(self):
        return self.dissertation.author


def search_by_dissertation(dissert):
    return DissertationUpdate.objects.filter(dissertation=dissert).order_by('created')


def add(request, new_dissertation, old_status, justification=None):
    person = mdl.person.find_by_user(request.user)
    adviser = search_by_person(person)
    update = DissertationUpdate()
    update.status_from = old_status
    update.status_to = new_dissertation.status
    if justification:
        update.justification = justification
    else:
        update.justification = "%s%s%s" % (adviser.type, JUSTIFICATION_LINK, new_dissertation.status)
    update.person = person
    update.dissertation = new_dissertation
    update.save()
