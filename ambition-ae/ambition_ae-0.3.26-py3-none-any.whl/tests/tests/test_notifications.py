from ambition_rando.tests import AmbitionTestCaseMixin
from django.contrib.auth.models import User, Permission
from django.core import mail
from django.core.management.color import color_style
from django.test import TestCase, tag
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_list_data.site_list_data import site_list_data
from edc_notification import site_notifications
from edc_registration.models import RegisteredSubject
from model_mommy import mommy

style = color_style()


class TestNotifications(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    def setUp(self):

        self.user = User.objects.create(
            username="erikvw", is_staff=True, is_active=True
        )
        self.subject_identifier = "1234"
        permissions = Permission.objects.filter(
            content_type__app_label="ambition_ae",
            content_type__model__in=["aeinitial", "aetmg"],
        )
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.subject_identifier = "12345"
        RegisteredSubject.objects.create(subject_identifier=self.subject_identifier)

        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(site_notifications.loaded)

    @tag("1")
    def test_susar(self):

        mommy.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            susar=YES,
            susar_reported=NO,
            user_created="erikvw",
        )
        self.assertEqual(len(mail.outbox), 5)

    @tag("1")
    def test_susar_updates(self):

        ae_initial = mommy.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            susar=YES,
            susar_reported=NO,
            user_created="erikvw",
        )

        subject = "".join([msg.subject for msg in mail.outbox])
        self.assertEqual(1, subject.count("AE SUSAR Report"))

        ae_initial.save()

        subject = "".join([msg.subject for msg in mail.outbox])
        self.assertEqual(1, subject.count("AE SUSAR Report"))

        ae_initial.susar_reported = YES
        ae_initial.save()

        subject = "".join([msg.subject for msg in mail.outbox])
        self.assertEqual(1, subject.count("AE SUSAR Report"))

        ae_initial.susar = NO
        ae_initial.susar_reported = NOT_APPLICABLE
        ae_initial.save()

        subject = "".join([msg.subject for msg in mail.outbox])
        self.assertEqual(2, subject.count("AE SUSAR Report"))

        ae_initial.susar = YES
        ae_initial.susar_reported = NO
        ae_initial.save()

        subject = "".join([msg.subject for msg in mail.outbox])
        self.assertEqual(2, subject.count("AE SUSAR Report"))

    @tag("1")
    def test_susar_text(self):
        mommy.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            susar=YES,
            susar_reported=NO,
            user_created="erikvw",
        )
        subject = "".join([msg.subject for msg in mail.outbox])
        self.assertEqual(1, subject.count("AE SUSAR Report"))
