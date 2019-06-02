from vndb_thigh_highs.models import Flag, Producer
from test_case import VNDBTestCase

class GetProducerTest(VNDBTestCase):
    def test_producer_basic(self):
        producers = self.vndb.get_producer(Producer.id == 428, Flag.BASIC)
        self.assertEqual(len(producers), 1)
        producer = producers[0]
        self.assertEqual(producer.name, "MangaGamer")
        self.assertEqual(producer.id, 428)

    def test_producer_all_flags(self):
        producers = self.vndb.get_producer(Producer.id == 428)
        self.assertEqual(len(producers), 1)
        producer = producers[0]
        self.assertEqual(producer.links.homepage, "http://www.mangagamer.com/")
