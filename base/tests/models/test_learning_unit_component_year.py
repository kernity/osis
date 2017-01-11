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
import datetime
from django.test import TestCase
from base.models.learning_unit_container import LearningContainer
from base.models.learning_unit_container_year import LearningContainerYear
from base.models.learning_component import LearningComponent
from base.models.learning_unit_component_year import LearningComponentYear
from base.models.academic_year import AcademicYear
from base.enums import learning_component_year_type

now = datetime.datetime.now()


class LearningComponentYearTest(TestCase):

    current_academic_year = None

    def setUp(self):
        self.current_academic_year = AcademicYear(year=(now.year),
                                     start_date=datetime.datetime(now.year, now.month, 15),
                                     end_date=datetime.datetime(now.year + 1, now.month, 28))
        self.current_academic_year.save()

    #def test_creation_learning_component_year(self):
    #   learning_container = LearningContainer(title="Biology")
    #  learning_container_different = LearningContainer(title="Chimie")
    # learning_component = LearningComponent(learning_container=learning_container,
        #                                       title="Cours magistral")
        #learning_container_year = LearningContainerYear(title="Biology 1",
        #                                               acronym="LBIO1212",
        #                                              academic_year=self.current_academic_year,
        #                                             learning_container=learning_container_different)
        #
        #learning_component_year = LearningComponentYear(learning_container_year=learning_container_year,
            #                                                     title="Cours magistral",
            #                                                    acronym="/C",
            #                                                   type=learning_component_year_type.COURS_MAGISTRAL)
            #self.assertRaises(AttributeError, learning_component_year.save)

    def test_creation_learning_component_year(self):
        learning_container = LearningContainer()
        learning_container_different = LearningContainer()

        #Composant associé à son conteneur
        learning_component = LearningComponent(learning_container=learning_container)

        #Conteneur annualisé est associé à un contenur différent du composant
        learning_container_year = LearningContainerYear(title="Biology",
                                                        acronym="LBIO1212",
                                                        academic_year=self.current_academic_year,
                                                        learning_container=learning_container_different)

        #Composant annualisé est associé à son composant
        learning_component_year = LearningComponentYear(learning_container_year=learning_container_year,
                                                        learning_component=learning_component,
                                                        title="Cours magistral",
                                                        acronym="/C",
                                                        type=learning_component_year_type.COURS_MAGISTRAL)


        self.assertRaises(AttributeError, learning_component_year.save)