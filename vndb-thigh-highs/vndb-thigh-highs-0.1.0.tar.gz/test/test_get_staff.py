from vndb_thigh_highs.models import Flag, Staff
from test_case import VNDBTestCase

class GetStaffTest(VNDBTestCase):
    def test_staff_basic(self):
        staffs = self.vndb.get_staff(Staff.id == 1, Flag.BASIC)
        self.assertEqual(len(staffs), 1)
        staff = staffs[0]
        self.assertEqual(staff.name, "Urobuchi Gen")
        self.assertEqual(staff.id, 1)

    def test_staff_all_flags(self):
        staffs = self.vndb.get_staff(Staff.id == 1)
        self.assertEqual(len(staffs), 1)
        staff = staffs[0]
        self.assertIn("scenario writer", staff.description)
        self.assertIn("Nitro+", staff.description)
