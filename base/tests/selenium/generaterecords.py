from pickle import load

from django.core.management.base import BaseCommand, CommandError

from base.models import offer
from base.models.person import Person
from django.contrib.auth.models import User
from base import models as mdl_base
from reference import models as mdl_reference
from attribution import models as mdl_attribution
from faker import Faker
import datetime


fake = Faker()

def create_academic_year(self):
    start_date = datetime.datetime(2016, 9, 15)
    end_date = datetime.datetime(2017, 9, 14)
    year = start_date.year+'-'+end_date.year
    academic_year = mdl_base.academic_year.AcademicYear.objects.create(year=year, start_date= start_date,
                                                                       end_date=end_date)
    return academic_year


def create_organization(self):
    organisation = mdl_base.organization.Organization.objects.create(name='Université catholique de Louvain',
                                                                     acronym='UCL', reference='-',
                                                                     website='http://uclouvain.be', type='Main')
    return organisation

def create_organization_adress(self, organisation,localisation,cp,city,country ):
    organisation_adres = mdl_base.organization_address.OrganizationAddress.objects.create(organization=organisation,
                                                                                          label='-',
                                                                                          location=localisation,
                                                                                          postal_code=cp,
                                                                                          city=city,country=country)
    return organisation_adres



def create_sector(self, acronym,title,organisation,type):
    structure_sector = mdl_base.structure.Structure.objects.create(acronym=acronym,
                                                                   title=title, organization=organisation, type=type)
    return structure_sector

def create_structure(self,acronym,titre,structure_part_of,organisation,type):
    structure = mdl_base.structure.Structure.objects.create(acronym=acronym, title=titre,
                                                                part_of=structure_part_of, organization=organisation,
                                                                type=type)
    return structure


def create_campus(self,name,organisation):
    campus = mdl_base.campus.Campus.objects.create(name=name, organization=organisation)
    return campus


def create_offer(self,title):
    offer = mdl_base.offer.Offer.objects.create(title=title)
    return offer

def create_offer_year(self,offer,academic_year,structure_sector,structure_fac,structure_pgm,acronym,title,title_short,grade,
                       recipient,location, postal_code,city, phone, fax,country,campus):
    offer_year = mdl_base.offer_year.OfferYear.objects.create(offer=offer, academic_year=academic_year,
                                                              entity_administration=structure_sector,
                                                              entity_administration_fac=structure_fac,
                                                              entity_management=structure_pgm,
                                                              ntity_management_fac=structure_fac,
                                                              acronym=acronym,
                                                              title=title,
                                                              title_short=title_short,
                                                              grade=grade, recipient=recipient,
                                                              location=location,
                                                              postal_code= postal_code,
                                                              city=city, country=country,
                                                              phone=phone, fax=fax, campus=campus)

def create_leaning_unit(self,acronym,title,start_year, end_year):
    leaning_unit = mdl_base.learning_unit.LearningUnit.objects.create(acronym=acronym,title=title,start_year=start_year,end_year=end_year)
    return leaning_unit

def create_leaning_unit_year(self,academic_year,leaning_unit,acronym,title,credits):
    decimal_scores=False
    if (credits >=15):
        decimal_scores =True
    leaning_unit_year = mdl_base.learning_unit_year.LearningUnitYear.objects.create(
        academic_year=academic_year, learning_unit=leaning_unit,
        acronym=acronym, title=title, credits=credits, decimal_scores=decimal_scores)
    return leaning_unit_year


def create_user(self,username, password, email):
    user = User.objects.create(username=username, password=password, email=email)
    return user


def create_person(self,user):
    person = Person.objects.create(user=user, first_name=fake.first_name(),
                                               last_name=fake.last_name())
    return person

def create_program_manager(self,person,offer_year):
    program_manager = mdl_base.program_manager.ProgramManager.objects.create(person=person,offer_year=offer_year)
    return program_manager

def create_tutor(self,person):
    tutor = mdl_base.tutor.Tutor.objects.create(person=person)
    return tutor

def create_attribution(self,learning_unit_year,tutor):
    attribution = mdl_attribution.attribution.Attribution.objects.create(learning_unit_year = learning_unit_year,tutor=tutor)
    return attribution

def create_student(self,person):
    student = mdl_base.student.Student.objects.create(person=person, registration_id=fake.ean(length=8))
    return student

def create_offer_enrollement(self,student,offer_year):
    offer_enrollment = mdl_base.offer_enrollment.OfferEnrollment.objects.create( student=student,offer_year=offer_year)
    return offer_enrollment

def create_learning_unit_enrollement(self,learning_unit_year,offer_enrollment):
    learning_unit_enrollement = mdl_base.learning_unit_enrollment.LearningUnitEnrollment.objects.create( learning_unit_year=learning_unit_year,offer_enrollment=offer_enrollment)
    return learning_unit_enrollement


class Command(BaseCommand):
    #Creates the records for the database

    def handle(self, *args, **options):
        tel_sc = '010473324'
        fax_sc = '010472837'
        recipient_sc = 'SC'
        adres_sc = 'Place des Sciences, 2L6.06.01'
        localisation_lln = 'Louvain-la-Neuve'
        cp_lln = 1348
        country_be = 'Belgique'
        city = 'Ottignies'
        acronym_chim_leaning = 'LCHM1111'
        acronym_biol_leaning = 'LENVI2199'
        title_chim_leaning = 'Chimie générale 1'
        title_biol_leaning = 'Stage professionnel'
        end_leaning = 2099

        academic_year = create_academic_year(self)
        organisation = create_organization(self)
        organisation_adres =  create_organization_adress(self,organisation,localisation_lln,cp_lln,city,country_be)
        structure_sector =create_sector(self,'SST','Secteur des sciences et technologies',organisation,'SECTOR')
        structure_fac = create_structure(self,'SC','Faculté des sciences',structure_sector,organisation,'FACULTY')
        structure_pgm_chim = create_structure(self,'CHIM', 'Ecole de chimie',structure_fac,organisation,'PROGRAM_COMMISION')
        structure_pgm_biol = create_structure(self, 'BIOL', 'Ecole de biologie', structure_fac, organisation,'PROGRAM_COMMISION')
        campus = create_campus(self,'Louvain-la-Neuve', organisation)
        offer = create_offer(self,'Bachelier en sciences')
        offer_year_chim =create_offer_year(self,offer,academic_year,structure_sector,structure_fac,structure_pgm_chim,'CHIM11BA','Première année de bachelier en sciences chimiques',
                                      'I Ba en scs chimiques','Bachelier',recipient_sc,adres_sc,cp_lln,localisation_lln,tel_sc ,fax_sc,country_be,campus)
        offer_year_biol = create_offer_year(self, offer, academic_year, structure_sector, structure_fac, structure_pgm_biol,'BIOL11BA', 'Première année de bachelier en sciences biologiques',
                                       'I Ba en scs biologiques', 'Bachelier',recipient_sc,adres_sc ,cp_lln,localisation_lln, tel_sc,fax_sc,country_be,campus)
        credits = 10

        #decimal score not allowed
        leaning_unit_chim = create_leaning_unit(self,acronym_chim_leaning,title_chim_leaning,2004,end_leaning)
        leaning_unit_year_chim = create_leaning_unit_year(self, academic_year,
                                                                               leaning_unit_chim,
                                                                               acronym_chim_leaning, title_chim_leaning,
                                                                               credits)
        credits = 20
        #decimal score allowed
        leaning_unit_biol =  create_leaning_unit(self,acronym_biol_leaning,title_biol_leaning,2007,end_leaning)
        leaning_unit_year_biol = create_leaning_unit_year(self,academic_year,leaning_unit_biol,acronym_biol_leaning,title_biol_leaning,credits)


        #program manager
        user_pgm_manager = create_user(self,'evase','evase','evase@gmail.com')
        person_pgm_manager = create_person(self,user_pgm_manager)
        program_manager_chim =create_program_manager(self,person_pgm_manager,offer_year_chim)
        program_manager_biol = create_program_manager(self, person_pgm_manager, offer_year_biol)

        #prof leader
        user_chim_leaning_unit_tutor_leader =create_user(self,'evaseLchim','evaseLchim','evaseevaseChim@gmail.com')
        person_chim_leaning_unit_tutor_leader =create_person(self,user_chim_leaning_unit_tutor_leader)
        tutor_chim_leaning_unit = create_tutor(self,person_chim_leaning_unit_tutor_leader) #tutor and leader of lchm1111
        create_attribution(self, leaning_unit_chim , tutor_chim_leaning_unit)


        user_biol_leaning_unit_tutor_leader = create_user(self, 'evaseLbiol', 'evaseLbiol', 'evaseevaseBiol@gmail.com')
        person_biol_leaning_unit_tutor_leader = create_person(self, user_biol_leaning_unit_tutor_leader)
        tutor_biol_leaning_unit = create_tutor(self, person_biol_leaning_unit_tutor_leader)  # tutor and leader of LENVI2199
        create_attribution(self, leaning_unit_biol, tutor_biol_leaning_unit)
        #prof
        user_chim_leaning_unit_tutor= create_user(self, 'evaseTchim', 'evaseTchim', 'evase@gmail.com')
        person_chim_leaning_unit_tutor = create_person(self, user_chim_leaning_unit_tutor)
        tutor2_chim_leaning_unit = create_tutor(self, person_chim_leaning_unit_tutor)  # tutor  of lchm1111
        create_attribution(self, leaning_unit_chim, tutor2_chim_leaning_unit)


        user_biol_leaning_unit_tutor = create_user(self, 'evaseTbiol', 'evaseTbiol', 'evase@gmail.com')
        person_bil_leaning_unit_tutor = create_person(self, user_biol_leaning_unit_tutor)
        tutor2_biol_leaning_unit = create_tutor(self,person_bil_leaning_unit_tutor)  # tutor  of LENVI2199
        create_attribution(self, leaning_unit_biol, tutor2_biol_leaning_unit)


        #student  and offer enrollment and  leaning unity

        for i in range(0, 200):
            user = create_user(self,fake.user_name(),fake.password(),fake.email())
            person = create_person(self,user)
            student =create_student(self,person)
            if(i%20==0):
                create_learning_unit_enrollement(self, leaning_unit_year_chim,
                                                 create_offer_enrollement(self, student, offer_year_chim))
            else :
                create_learning_unit_enrollement(self, leaning_unit_year_biol,
                                                 create_offer_enrollement(self, student, offer_year_biol))

            print(student)