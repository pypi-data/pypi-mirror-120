from copy import deepcopy

from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from edc_list_data.site_list_data import site_list_data
from edc_randomization.site_randomizers import site_randomizers
from edc_sites import add_or_update_django_sites, get_sites_by_country
from edc_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_utils.date import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version
from meta_rando.randomizers import RandomizerPhaseThree, RandomizerPhaseTwo
from meta_sites import fqdn
from meta_subject.models import SubjectVisit
from meta_visit_schedule.constants import DAY1

from ..models import (
    ScreeningPartOne,
    ScreeningPartThree,
    ScreeningPartTwo,
    SubjectScreening,
)
from .options import (
    get_part_one_eligible_options,
    get_part_three_eligible_options,
    get_part_two_eligible_options,
)


class MetaTestCaseMixin(SiteTestCaseMixin):

    fqdn = fqdn

    default_sites = get_sites_by_country("tanzania")

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count = 10

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        add_or_update_django_sites(sites=get_sites_by_country("tanzania"))
        site_randomizers._registry = {}
        if cls.import_randomization_list:
            if get_meta_version() == PHASE_TWO:
                site_randomizers.register(RandomizerPhaseTwo)
                RandomizerPhaseTwo.import_list(
                    verbose=False, sid_count_for_tests=cls.sid_count
                )
            elif get_meta_version() == PHASE_THREE:
                site_randomizers.register(RandomizerPhaseThree)
                RandomizerPhaseThree.import_list(
                    verbose=False, sid_count_for_tests=cls.sid_count
                )
        import_holidays(test=True)
        site_list_data.initialize()
        site_list_data.autodiscover()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if get_meta_version() == PHASE_TWO:
            RandomizerPhaseTwo.model_cls().objects.all().delete()
        elif get_meta_version() == PHASE_THREE:
            RandomizerPhaseThree.model_cls().objects.all().delete()
        Holiday.objects.all().delete()

    def get_subject_screening(
        self,
        report_datetime=None,
        eligibility_datetime=None,
        gender=None,
    ):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_three_eligible_options = deepcopy(get_part_three_eligible_options())
        if report_datetime:
            part_one_eligible_options.update(report_datetime=report_datetime)
        part_one_eligible_options["gender"] = (
            gender or part_one_eligible_options["gender"]
        )
        part_one = ScreeningPartOne.objects.create(
            user_created="erikvw", user_modified="erikvw", **part_one_eligible_options
        )
        screening_identifier = part_one.screening_identifier
        self.assertEqual(part_one.eligible_part_one, YES)

        screening_part_two = ScreeningPartTwo.objects.get(
            screening_identifier=screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(screening_part_two, k, v)
        screening_part_two.save()
        print(screening_part_two.reasons_ineligible_part_two)
        self.assertEqual(screening_part_two.reasons_ineligible_part_two, "")
        self.assertEqual(screening_part_two.eligible_part_two, YES)

        screening_part_three = ScreeningPartThree.objects.get(
            screening_identifier=screening_identifier
        )
        for k, v in part_three_eligible_options.items():
            setattr(screening_part_three, k, v)
        screening_part_three.save()
        self.assertEqual(screening_part_three.reasons_ineligible_part_three, "")
        self.assertEqual(screening_part_three.eligible_part_three, YES)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )

        self.assertTrue(subject_screening.eligible)

        if eligibility_datetime:
            screening_part_three.eligibility_datetime = eligibility_datetime
            screening_part_three.save()
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
        return subject_screening

    @staticmethod
    def get_subject_consent(subject_screening):
        return baker.make_recipe(
            "meta_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            gender=subject_screening.gender,
            dob=(
                get_utcnow().date()
                - relativedelta(years=subject_screening.age_in_years)
            ),
            site=Site.objects.get(name="hindu_mandal"),
        )

    def get_subject_visit(self, gender=None):
        subject_screening = self.get_subject_screening(gender=gender)
        subject_consent = self.get_subject_consent(subject_screening)
        subject_identifier = subject_consent.subject_identifier

        appointment = Appointment.objects.get(
            subject_identifier=subject_identifier, visit_code=DAY1
        )
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()
        return SubjectVisit.objects.create(appointment=appointment, reason=SCHEDULED)

    @staticmethod
    def get_next_subject_visit(subject_visit):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        return SubjectVisit.objects.create(
            appointment=next_appointment, reason=SCHEDULED
        )
