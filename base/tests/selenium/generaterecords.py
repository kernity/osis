from django.core.management.base import BaseCommand, CommandError

from base.models import offer
from base.models.person import Person
from django.contrib.auth.models import User
from base import models as mdl_base
from reference import models as mdl_reference
from faker import Faker

# Une fois le patch applique,
# il suffira de lancer python manage.py generaterecords pour generer les records
# et de generer un dump json avec python manage.py dumpdata
# Fixer le generateur pour que cela fonctionne


class Command(BaseCommand):
    help = 'Creates the records for the database'
    academic_year = mdl_base.academic_year.AcademicYear.objects.create(year='2016-2017', start_date ='2016-09-15', end_date='2017-09-14')
    organisation =mdl_base.organization.Organization.objects.create(name='Université catholique de Louvain',acronym='UCL',reference='-', website='http://uclouvain.be', type='Main')
    organisation_adres =mdl_base.organization_address.OrganizationAddress.objects.create(organization = organisation, label = '-', location='Louvain la Neuve', postal_code='1348', city='Ottignies', country='Belgique')

    structure_sector = mdl_base.structure.Structure.objects.create(acronym='SST', title='Secteur des sciences et technologies',organization=organisation, type='SECTOR')
    structure_fac = mdl_base.structure.Structure.objects.create(acronym='SC', title='Faculté des sciences',part_of=structure_sector, organization=organisation, type='FACULTY')
    structure_pgm = mdl_base.structure.Structure.objects.create(acronym='CHIM', title='Ecole de chimie', part_of=structure_fac , organization =organisation, type='PROGRAM_COMMISION')
    campus = mdl_base.campus.Campus.objects.create(name='Louvain-la-Neuve', organization=organisation)
    offer = mdl_base.offer.Offer.objects.create(title = "Bachelier en droit")

    offer_year = mdl_base.offer_year.OfferYear.objects.create(offer=offer, academic_year=academic_year, entity_administration=structure_sector, entity_administration_fac=structure_fac,
                                    entity_management=structure_pgm, ntity_management_fac=structure_fac, acronym='CHIM11BA', title='Première année de bachelier en sciences chimiques',
                                    title_short='I Ba en scs chimiques', grade='Bachelier', recipient='SC',location='Place des Sciences, 2L6.06.01', postal_code='1348',
                                    city='Louvain-la-Neuve', country='Belgique', phone='010473324', fax='010472837', campus=campus)


    #fieldsets_academic_year = ((None, {'fields': ('year', 'start_date', 'end_date')}),)



    #fieldsets_organisation = ((None, {'fields': ('name', 'acronym', 'reference', 'website', 'type')}),)
    #fieldsets_organisation_adres = ((None, {'fields': ('organization', 'label', 'location', 'postal_code', 'city', 'country')}),)
    #fieldsets_structure = ((None, {'fields': ('acronym', 'title', 'part_of', 'organization', 'type')}),)
    #fieldsets_campus = ((None, {'fields': ('name', 'organization')}),)

    #fieldsets_structure_adres = ((None, {'fields': ('structure', 'label', 'location', 'postal_code', 'city', 'country', 'phone', 'fax', 'email')}),)

    #fieldsets_offerYear = ((None, {'fields': ('offer', 'academic_year', 'entity_administration', 'entity_administration_fac',
    #                               'entity_management', 'entity_management_fac', 'acronym', 'title', 'parent',
    #                                'title_international', 'title_short', 'title_printable', 'grade', 'recipient',
    #                                'location', 'postal_code', 'city', 'country', 'phone', 'fax', 'email', 'campus')}),)

    #fieldsets_country = ((None, {'fields': ('iso_code', 'name', 'nationality', 'european_union', 'dialing_code', 'cref_code',
    #                                'currency', 'continent')}),)
    #fieldsets_grade_type = ((None, {'fields': ('name', 'institutional_grade_type', 'coverage', 'adhoc', 'institutional')}),)


    def handle(self, *args, **options):
        fake = Faker()

        for i in range(0, 10000):
            user = User.objects.create(username=fake.user_name(),
                                       password=fake.password(),
                                       email=fake.email())
            new_person = Person.objects.create(user=user, first_name=fake.first_name(), last_name=fake.last_name())
            student = mdl_base.student.Student.objects.create(person = new_person, registration_id =fake.ean(length=8))


            print(student)