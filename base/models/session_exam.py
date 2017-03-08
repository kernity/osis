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
import datetime
from django.contrib import admin
from django.db.models import Max
from base.models import offer_year_calendar, academic_calendar
from django.utils import timezone


class SessionExamAdmin(admin.ModelAdmin):
    list_display = ('learning_unit_year', 'offer_year_calendar', 'number_session', 'changed', 'deadline')
    list_filter = ('learning_unit_year__academic_year', 'number_session',)
    raw_id_fields = ('learning_unit_year', 'offer_year_calendar')
    fieldsets = ((None, {'fields': ('learning_unit_year', 'number_session', 'offer_year_calendar', 'deadline')}),)
    search_fields = ['learning_unit_year__acronym', 'offer_year_calendar__offer_year__acronym']


class SessionExam(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed = models.DateTimeField(null=True)
    number_session = models.IntegerField()
    learning_unit_year = models.ForeignKey('LearningUnitYear')
    offer_year_calendar = models.ForeignKey('OfferYearCalendar')
    progress = None
    deadline = models.DateField(null=True)

    def __str__(self):
        return u"%s - %s - %d" % (self.learning_unit_year, self.offer_year_calendar.offer_year, self.number_session)


def current_session_exam():
    offer_calendar = offer_year_calendar.find_by_current_session_exam()
    session_exam = SessionExam.objects.filter(offer_year_calendar=offer_calendar).first()
    return session_exam


def find_session_by_id(session_exam_id):
    return SessionExam.objects.get(pk=session_exam_id)


def find_session_exam_number():
    """
    :return: The current sessionExam number (based on the datetime.now() in offerYearCalendar).
    """
    sess_exam_number = SessionExam.objects.filter(offer_year_calendar__start_date__lte=timezone.now())\
                                          .filter(offer_year_calendar__end_date__gte=timezone.now())\
                                          .distinct('number_session')\
                                          .values('number_session')
    sess_exam_number = list(sess_exam_number) # Force evaluation of the queryset
    if len(sess_exam_number) > 1:
        raise Exception("There are multiple exam sessions opened at this moment !")
    elif len(sess_exam_number) == 1:
        return sess_exam_number[0].get('number_session')
    return None


def get_scores_encoding_calendars():
    academic_calendars_id = SessionExam.objects.values_list('offer_year_calendar__academic_calendar', flat=True)\
                                                            .distinct('offer_year_calendar__academic_calendar')
    return academic_calendar.find_by_ids(academic_calendars_id)

def is_inside_score_encoding(date=datetime.datetime.now().date()):
    is_inside = SessionExam.objects.exclude(offer_year_calendar__isnull=True,
                                            offer_year_calendar__academic_calendar__isnull=True,
                                            offer_year_calendar__academic_calendar__start_date__isnull=True,
                                            offer_year_calendar__academic_calendar__end_date__isnull=True)\
                                    .filter(offer_year_calendar__academic_calendar__start_date__lte=date,
                                            offer_year_calendar__academic_calendar__end_date__gte=date) \
                                    .distinct('offer_year_calendar__academic_calendar')\
                                    .count()
    return bool(is_inside)

# Return the latest session exam finised [end_date <= ARGS] according to the date passed in args.
def get_latest_session_exam(date=datetime.datetime.now().date()):
    latest_session_exam = SessionExam.objects.exclude(offer_year_calendar__isnull=True,
                                                     offer_year_calendar__academic_calendar__isnull=True,
                                                     offer_year_calendar__academic_calendar__end_date__isnull=True)\
                                              .filter(offer_year_calendar__academic_calendar__end_date__lte=date) \
                                              .order_by('-offer_year_calendar__academic_calendar__end_date')\
                                              .first()
    return latest_session_exam