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

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from base.models.person import *
import re

def search_person_with_last_name(last_name):
    return Person.objects.filter(last_name__icontains=last_name)

@login_required
def get_persones(request,search_string=''):
    persones_json = []
    persones_list=None
    if re.match(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", search_string):
        persones_list = search_by_email(search_string)
    else:
        persones_list = search_person_with_last_name(search_string)
    if persones_list:
        for person in persones_list:
            persones_json.append({'person_id': person.id,
                             'first_name': person.first_name,
                             'last_name': person.last_name,
                                  'email': person.email
                                  })
    else:
        persones_json = []

    return JsonResponse({'persones_json': persones_json})