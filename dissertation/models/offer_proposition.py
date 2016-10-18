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
from django.utils import timezone
from base.models.serializable_model import SerializableModel
from datetime import datetime


class OfferPropositionAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'offer')
    raw_id_fields = ('offer',)


class OfferProposition(SerializableModel):
    acronym = models.CharField(max_length=200)
    offer = models.ForeignKey('base.Offer')
    student_can_manage_readers = models.BooleanField(default=True)
    adviser_can_suggest_reader = models.BooleanField(default=False)
    evaluation_first_year = models.BooleanField(default=False)
    validation_commission_exists = models.BooleanField(default=False)
    start_visibility_proposition = models.DateField(default=timezone.now)
    end_visibility_proposition = models.DateField(default=timezone.now)
    start_visibility_dissertation = models.DateField(default=timezone.now)
    end_visibility_dissertation = models.DateField(default=timezone.now)
    start_jury_visibility = models.DateField(default=timezone.now)
    end_jury_visibility = models.DateField(default=timezone.now)
    start_edit_title = models.DateField(default=timezone.now)
    end_edit_title = models.DateField(default=timezone.now)

    @property
    def in_periode_visibility_proposition(self):
        now = datetime.date(datetime.now())
        start = self.start_visibility_proposition
        end = self.end_visibility_proposition
        return start <= now <= end

    @property
    def in_periode_visibility_dissertation(self):
        now = datetime.date(datetime.now())
        start = self.start_visibility_dissertation
        end = self.end_visibility_dissertation
        return start <= now <= end

    @property
    def in_periode_jury_visibility(self):
        now = datetime.date(datetime.now())
        start = self.start_jury_visibility
        end = self.end_jury_visibility
        return start <= now <= end

    @property
    def in_periode_edit_title(self):
        now = datetime.date(datetime.now())
        start = self.start_edit_title
        end = self.end_edit_title
        return start <= now <= end

    def __str__(self):
        return self.acronym


def get_by_offer(offer):
    return OfferProposition.objects.get(offer=offer)


def search_by_offer(offers):
    return OfferProposition.objects.filter(offer__in=offers).distinct().order_by('acronym')


def show_validation_commission(offer_propositions):
    # True if validation_commission_exists is True or it exist one offer_proposition
    return any([offer_proposition.validation_commission_exists for offer_proposition in offer_propositions])


def show_evaluation_first_year(offer_propositions):
    # True if validation_commission_exists is True or it exist one offer_proposition
    return any([offer_proposition.evaluation_first_year for offer_proposition in offer_propositions])


def get_by_dissertation(dissertation):
    return get_by_offer(dissertation.offer_year_start.offer)


def find_by_id(offer_proposition_id):
    return OfferProposition.objects.get(pk=offer_proposition_id)
