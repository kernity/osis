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
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from base.models import offer_year, student
from base.models.serializable_model import SerializableModel
from dissertation.models.dissertation_role import get_promoteur_by_dissertation
from dissertation.utils.emails_dissert import send_mail_dissert_accepted_by_teacher, \
    send_mail_dissert_acknowledgement, send_mail_dissert_accepted_by_com, send_mail_dissert_refused_by_teacher, \
    send_mail_dissert_refused_by_com, send_mail_to_teacher_new_dissert
from . import proposition_dissertation, offer_proposition, dissertation_location


class DissertationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'active', 'proposition_dissertation', 'modification_date')
    raw_id_fields = ('author', 'offer_year_start', 'proposition_dissertation', 'location')


STATUS_CHOICES = (
    ('DRAFT', _('draft')),
    ('DIR_SUBMIT', _('submitted_to_director')),
    ('DIR_OK', _('accepted_by_director')),
    ('DIR_KO', _('refused_by_director')),
    ('COM_SUBMIT', _('submitted_to_commission')),
    ('COM_OK', _('accepted_by_commission')),
    ('COM_KO', _('refused_by_commission')),
    ('EVA_SUBMIT', _('submitted_to_first_year_evaluation')),
    ('EVA_OK', _('accepted_by_first_year_evaluation')),
    ('EVA_KO', _('refused_by_first_year_evaluation')),
    ('TO_RECEIVE', _('to_be_received')),
    ('TO_DEFEND', _('to_be_defended')),
    ('DEFENDED', _('defended')),
    ('ENDED', _('ended')),
    ('ENDED_WIN', _('ended_win')),
    ('ENDED_LOS', _('ended_los')),
)

DEFEND_PERIODE_CHOICES = (
    ('UNDEFINED', _('undefined')),
    ('JANUARY', _('january')),
    ('JUNE', _('june')),
    ('SEPTEMBER', _('september')),
)


class Dissertation(SerializableModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(student.Student)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='DRAFT')
    defend_periode = models.CharField(max_length=12, choices=DEFEND_PERIODE_CHOICES, blank=True, null=True)
    defend_year = models.IntegerField(blank=True, null=True)
    offer_year_start = models.ForeignKey(offer_year.OfferYear)
    proposition_dissertation = models.ForeignKey(proposition_dissertation.PropositionDissertation)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    modification_date = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(dissertation_location.DissertationLocation, blank=True, null=True)

    def __str__(self):
        return self.title

    def deactivate(self):
        self.active = False
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()

    def go_forward(self):

        next_status = get_next_status(self, "go_forward")
        if self.status == 'TO_RECEIVE' and next_status == 'TO_DEFEND':
            send_mail_dissert_acknowledgement(self.author.person)
        if self.status == 'DRAFT' and next_status == 'DIR_SUBMIT':
            send_mail_to_teacher_new_dissert(get_promoteur_by_dissertation(self))
        self.set_status(next_status)

    def accept(self):
        next_status = get_next_status(self, "accept")
        if self.status == 'DIR_SUBMIT':
            send_mail_dissert_accepted_by_teacher(self.author.person)
        if self.status == 'COM_SUBMIT':
            send_mail_dissert_accepted_by_com(self.author.person)
        self.set_status(next_status)

    def refuse(self):
        next_status = get_next_status(self, "refuse")
        if self.status == 'DIR_SUBMIT':
            send_mail_dissert_refused_by_teacher(self.author.person)
        if self.status == 'COM_SUBMIT':
            send_mail_dissert_refused_by_com(self.author.person, get_promoteur_by_dissertation(self).person)
        self.set_status(next_status)

    class Meta:
        ordering = ["author__person__last_name", "author__person__middle_name", "author__person__first_name", "title"]


def count_by_proposition(proposition):
    return Dissertation.objects.filter(active=True) \
        .filter(proposition_dissertation=proposition) \
        .exclude(status='DRAFT') \
        .count()


def find_by_id(dissertation_id):
    return Dissertation.objects.get(pk=dissertation_id)


def get_next_status(dissertation, operation):
    if operation == "go_forward":
        if dissertation.status == 'DRAFT' or dissertation.status == 'DIR_KO':
            return 'DIR_SUBMIT'
        elif dissertation.status == 'TO_RECEIVE':
            return 'TO_DEFEND'
        elif dissertation.status == 'TO_DEFEND':
            return 'DEFENDED'
        else:
            return dissertation.status
    elif operation == "accept":
        offer_prop = offer_proposition.get_by_offer(dissertation.offer_year_start.offer)
        if offer_prop.validation_commission_exists and dissertation.status == 'DIR_SUBMIT':
            return 'COM_SUBMIT'
        elif offer_prop.evaluation_first_year and (dissertation.status == 'DIR_SUBMIT' or
                                                   dissertation.status == 'COM_SUBMIT' or
                                                   dissertation.status == 'COM_KO'):
            return 'EVA_SUBMIT'
        elif dissertation.status == 'EVA_SUBMIT' or dissertation.status == 'EVA_KO':
            return 'TO_RECEIVE'
        elif dissertation.status == 'DEFENDED':
            return 'ENDED_WIN'
        else:
            return 'TO_RECEIVE'
    elif operation == "refuse":
        if dissertation.status == 'DIR_SUBMIT':
            return 'DIR_KO'
        elif dissertation.status == 'COM_SUBMIT':
            return 'COM_KO'
        elif dissertation.status == 'EVA_SUBMIT':
            return 'EVA_KO'
        elif dissertation.status == 'DEFENDED':
            return 'ENDED_LOS'
        else:
            return dissertation.status
    else:
        return dissertation.status


def search(terms=None, active=True):
    queryset = Dissertation.objects.all()
    if terms:
        queryset = queryset.filter(
            Q(author__person__first_name__icontains=terms) |
            Q(author__person__middle_name__icontains=terms) |
            Q(author__person__last_name__icontains=terms) |
            Q(description__icontains=terms) |
            Q(proposition_dissertation__title__icontains=terms) |
            Q(proposition_dissertation__author__person__first_name__icontains=terms) |
            Q(proposition_dissertation__author__person__middle_name__icontains=terms) |
            Q(proposition_dissertation__author__person__last_name__icontains=terms) |
            Q(status__icontains=terms) |
            Q(title__icontains=terms)
        ).filter(active=active).distinct()
    return queryset


def search_by_offer(offers):
    return Dissertation.objects.filter(offer_year_start__offer__in=offers)


def search_by_offer_and_status(offers, status):
    return search_by_offer(offers).filter(status=status)


def search_by_proposition_author(terms=None, active=True, proposition_author=None):
    return search(terms=terms, active=active).filter(proposition_dissertation__author=proposition_author)
