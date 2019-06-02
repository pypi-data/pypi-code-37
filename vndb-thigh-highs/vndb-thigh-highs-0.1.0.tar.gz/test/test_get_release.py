from vndb_thigh_highs.models import Flag, Release, AnimationType
from test_case import VNDBTestCase

class GetReleaseTest(VNDBTestCase):
    def test_release_basic(self):
        releases = self.vndb.get_release(Release.id == 350, Flag.BASIC)
        self.assertEqual(len(releases), 1)
        release = releases[0]
        self.assertEqual(release.title, "Fate/Stay Night - First Press Limited Edition")
        self.assertEqual(release.id, 350)

    def test_release_all_flags(self):
        releases = self.vndb.get_release(Release.id == 350)
        self.assertEqual(len(releases), 1)
        release = releases[0]
        self.assertEqual(release.gtin, '4560158370012')
        self.assertEqual(release.animation.ero, AnimationType.NO_ANIMATION)
