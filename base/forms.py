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
from django import forms
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet

from base import models as mdl
from base.models.exam_enrollment import JUSTIFICATION_TYPES


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ScoreFileForm(forms.Form):
    file = forms.FileField()


class OrganizationForm(ModelForm):
    class Meta:
        model = mdl.organization.Organization
        fields = ['acronym', 'name', 'website', 'reference']


class AcademicCalendarForm(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',),
                                 required=True)
    end_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),
                               input_formats=('%d/%m/%Y',),
                               required=True)

    class Meta:
        model = mdl.academic_calendar.AcademicCalendar
        fields = ['start_date', 'end_date', 'title', 'highlight_title', 'highlight_description', 'highlight_shortcut']


class OfferYearCalendarForm(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',),
                                 required=True)
    end_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),
                               input_formats=('%d/%m/%Y',),
                               required=True)

    class Meta:
        model = mdl.offer_year_calendar.OfferYearCalendar
        fields = ['offer_year', 'start_date', 'end_date', 'customized']


class BaseScoreFrom(forms.Form):
    JUSTIFICATION_CHOICES = JUSTIFICATION_TYPES

    def __init__(self,enrollment_id,student,offer_year_acronym, encoder_is_pgm_manager):
        super().__init__()
        self.enrollment_id = enrollment_id
        self.student_registration_id = student.registration_id
        self.student_last_name = student.last_name
        self.student_first_name = student.student_first_name
        self.offer_year_acronym = offer_year_acronym
        self.decimal_allowed = False
        if not encoder_is_pgm_manager:
            self.JUSTIFICATION_CHOICES = list(filter(lambda x,y: x not in ('ILL', 'JUSTIFIED_ABSENCE'),
                                                     JUSTIFICATION_TYPES))

    score_final = forms.IntegerField(max_value=20, min_value=0)
    score_draft = forms.IntegerField(max_value=20, min_value=0)
    justification_final = forms.ChoiceField(choices=JUSTIFICATION_CHOICES, required=False)
    justification_draft = forms.ChoiceField(choices=JUSTIFICATION_CHOICES, required=False)


class DecimalScoreForm(BaseScoreFrom):
    def __init__(self):
        super().__init__()
        self.decimal_allowed = True

    score_final = forms.DecimalField(max_value=20,min_value=0)
    score_draft = forms.DecimalField(max_value=20, min_value=0)


def get_score_form(decimal):
    if decimal:
        return DecimalScoreForm
    else:
        return BaseScoreFrom
