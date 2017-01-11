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
from django.contrib import admin
from base.enums.learning_unit_year_type import YEAR_TYPES


class LearningContainerYearAdmin(admin.ModelAdmin):
    list_display = ('learning_container', 'academic_year', 'language', 'acronym', 'acronym_initials', 'acronym_number',

                    'type', 'title', 'title_short', 'requirement_entity', 'allocation_entity')
    fieldsets = ((None, {'fields': ('learning_container', 'academic_year', 'language','acronym', 'acronym_initials',
                                    'acronym_number', 'type', 'title', 'title_short', 'requirement_entity',
                                    'allocation_entity' )}),)
    search_fields = ['acronym']


class LearningContainerYear(models.Model):
    academic_year = models.ForeignKey('AcademicYear')
    learning_container = models.ForeignKey('LearningContainer')
    title = models.CharField(max_length=255)
    acronym = models.CharField(max_length=10)
    #Ajoutés pour la gestion des UE
    language = models.ForeignKey('reference.Language')
    acronym_initials = models.CharField(max_length=5)
    acronym_number = models.CharField(max_length=4)
    type = models.CharField(max_length=10, blank=True, null=True, choices=YEAR_TYPES)
    title_short = models.CharField(max_length=50)
    requirement_entity = models.IntegerField(default=0)
    allocation_entity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.title != self.learning_container.title:
            raise AttributeError("The title of the learning container year is different from the learning container.")

        super(LearningContainerYear, self).save()

    def __str__(self):
        return u"%s - %s" % (self.acronym, self.title)

    class Meta:
        permissions = (
            ("can_access_learningcontaineryear", "Can access learning container year"),
        )


def find_by_academic_year(academic_year):
    return LearningContainerYear.objects.get(pk=academic_year)


def find_by_id(learning_container_year_id):
    return LearningContainerYear.objects.get(pk=learning_container_year_id)

def find_by_acronym_initials(acronym_initials=None):
    queryset = LearningContainerYear.objects

    if acronym_initials:
        queryset = queryset.filter(acronym_initials=acronym_initials)

    return queryset

def find_by_acronym_number(acronym_number=None):
    queryset = LearningContainerYear.objects

    if acronym_number:
        queryset = queryset.filter(acronym_number=acronym_number)

    return queryset

#Puis, pour le développement, il faudrait au moins pouvoir faire une recherche dans la base sur acronym_initials et acronym_number et academic_year
#(le dernier, je sais, ce sera pas facile). Et affichier toutes les learining units qui correspondent à ces critères (1, les 2 premiers ou les 3).  Afficher un tableau de résultat contenant :
#les acronyms (du learning_container_year), l’acronyme_unit_type (de learning_unit_year), le title (de la même)
#Et permettre à l’utilisateur de choisir dans la liste affichée une LU, en cliquant dessus => ça ouvrira un écran bien complexe, avec des onglets et toussa; mais ça on en aprler l’an prochain.