# ------------------------------------------------------------------------------
# Test Cancellation Page
# ------------------------------------------------------------------------------
import sys
import datetime as dt
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from wagtail.core.models import Page, PageViewRestriction
from ls.joyous.models.calendar import CalendarPage
from ls.joyous.models.events import RecurringEventPage
from ls.joyous.models.events import CancellationPage
from ls.joyous.utils.recurrence import Recurrence, WEEKLY, MO, WE, FR

# ------------------------------------------------------------------------------
class Test(TestCase):
    def setUp(self):
        self.home = Page.objects.get(slug='home')
        self.user = User.objects.create_user('i', 'i@joy.test', 's3(r3t')
        self.calendar = CalendarPage(owner = self.user,
                                     slug  = "events",
                                     title = "Events")
        self.home.add_child(instance=self.calendar)
        self.calendar.save_revision().publish()
        self.event = RecurringEventPage(slug      = "test-meeting",
                                        title     = "Test Meeting",
                                        repeat    = Recurrence(dtstart=dt.date(1989,1,1),
                                                               freq=WEEKLY,
                                                               byweekday=[MO,WE,FR]),
                                        time_from = dt.time(13),
                                        time_to   = dt.time(15,30))
        self.calendar.add_child(instance=self.event)
        self.cancellation = CancellationPage(owner = self.user,
                                             overrides = self.event,
                                             except_date = dt.date(1989,2,1),
                                             cancellation_title   = "Meeting Cancelled",
                                             cancellation_details =
                                                 "Cancelled due to lack of interest")
        self.event.add_child(instance=self.cancellation)
        self.cancellation.save_revision().publish()

    def testGetEventsByDay(self):
        hiddenCancellation = CancellationPage(owner = self.user,
                                              overrides = self.event,
                                              except_date = dt.date(1989,2,13))
        self.event.add_child(instance=hiddenCancellation)
        events = RecurringEventPage.events.byDay(dt.date(1989,2,1),
                                                 dt.date(1989,2,28))
        self.assertEqual(len(events), 28)
        evod1 = events[0]
        self.assertEqual(evod1.date, dt.date(1989,2,1))
        self.assertEqual(len(evod1.days_events), 1)
        self.assertEqual(len(evod1.continuing_events), 0)
        title, page, url = evod1.days_events[0]
        self.assertEqual(title, "Meeting Cancelled")
        self.assertIs(type(page), CancellationPage)
        evod2 = events[12]
        self.assertEqual(evod2.date, dt.date(1989,2,13))
        self.assertEqual(len(evod2.days_events), 0)
        self.assertEqual(len(evod2.continuing_events), 0)

    def testOccursOn(self):
        self.assertIs(self.event._occursOn(dt.date(1989, 2, 1)), False)
        self.assertIs(self.event._occursOn(dt.date(1989, 2, 3)), True)

    def testUnexplainedCancellation(self):
        self._cancel_1999_02_08()

        events = RecurringEventPage.events.byDay(dt.date(1999,2,1),
                                                dt.date(1999,2,28))
        self.assertEqual(len(events), 28)
        evod = events[7]
        self.assertEqual(evod.date, dt.date(1999,2,8))
        self.assertEqual(len(evod.days_events), 0)
        self.assertEqual(len(evod.continuing_events), 0)

    def testUnexplainedCancellationExplained(self):
        restriction = self._cancel_1999_02_08()

        request = RequestFactory().get("/test")
        request.user = self.user
        KEY = PageViewRestriction.passed_view_restrictions_session_key
        request.session = {KEY: [restriction.id]}
        events = RecurringEventPage.events(request).byDay(dt.date(1999,2,1),
                                                          dt.date(1999,2,28))
        self.assertEqual(len(events), 28)
        evod = events[7]
        self.assertEqual(evod.date, dt.date(1999,2,8))
        self.assertEqual(len(evod.days_events), 1)
        self.assertEqual(len(evod.continuing_events), 0)
        title, page, url = evod.days_events[0]
        self.assertEqual(title, "Restructure Pending")
        self.assertIs(type(page), CancellationPage)

    def _cancel_1999_02_08(self):
        cancellation = CancellationPage(owner = self.user,
                                        overrides = self.event,
                                        except_date = dt.date(1999, 2, 8),
                                        cancellation_title   = "Restructure Pending",
                                        cancellation_details = "Keep it quiet")
        self.event.add_child(instance=cancellation)
        PASSWORD = PageViewRestriction.PASSWORD
        restriction = PageViewRestriction.objects.create(restriction_type = PASSWORD,
                                                         password = "s3cr3t",
                                                         page = cancellation)
        restriction.save()
        return restriction

    def testStatus(self):
        self.assertEqual(self.cancellation.status, "cancelled")
        self.assertEqual(self.cancellation.status_text, "This event has been cancelled.")
        now = dt.datetime.now()
        myday = now.date() + dt.timedelta(1)
        friday = myday + dt.timedelta(days=(4-myday.weekday())%7)
        futureCan = CancellationPage(owner = self.user,
                                     overrides = self.event,
                                     except_date = friday,
                                     cancellation_title   = "",
                                     cancellation_details = "")
        self.event.add_child(instance=futureCan)
        self.assertEqual(futureCan.status, "cancelled")
        self.assertEqual(futureCan.status_text, "This event has been cancelled.")

    def testWhen(self):
        self.assertEqual(self.cancellation.when, "Wednesday 1st of February 1989 at 1pm to 3:30pm")

    def testWhenEver(self):
        event = RecurringEventPage(slug      = "XYZ",
                                   title     = "Xylophone yacht zombies",
                                   repeat    = Recurrence(dtstart=dt.date(1989,1,1),
                                                          freq=WEEKLY,
                                                          byweekday=[FR]),
                                   time_from = dt.time(19))
        self.calendar.add_child(instance=event)
        cancellation = CancellationPage(owner = self.user,
                                        overrides = event,
                                        except_date = dt.date(1989,3,10),
                                        cancellation_title = "Cancelled")
        event.add_child(instance=cancellation)
        cancellation.save_revision().publish()
        self.assertEqual(cancellation.when, "Friday 10th of March 1989 at 7pm")

    def testAt(self):
        self.assertEqual(self.cancellation.at.strip(), "1pm")

    def testGroup(self):
        self.assertIsNone(self.cancellation.group)

    def testOverridesRepeat(self):
        self.assertEqual(self.cancellation.overrides_repeat, self.event.repeat)

    def testGetContext(self):
        request = RequestFactory().get("/test")
        context = self.cancellation.get_context(request)
        self.assertIn('overrides', context)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
