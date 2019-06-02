from vndb_thigh_highs.models import Flag, Character
from vndb_thigh_highs import GetCommandOptions
from test_case import VNDBTestCase

class GetCharacterTest(VNDBTestCase):
    def test_basic(self):
        characters = self.vndb.get_character(Character.id == 3885, Flag.BASIC)
        self.assertEqual(len(characters), 1)
        character = characters[0]
        self.assertEqual(character.name, "Naoe Yamato")
        self.assertEqual(character.id, 3885)

    def test_all_flags(self):
        characters = self.vndb.get_character(Character.id == 4052)
        self.assertEqual(len(characters), 1)
        character = characters[0]
        self.assertEqual(character.name, "Yukimura Anzu")
        self.assertEqual(character.bust, 69)
        self.assertEqual(character.waist, 46)
        self.assertEqual(character.hip, 73)

    def test_multiple_pages(self):
        sengoku_rance_characters_ids = [
            735, 2855, 2872, 2856, 740, 736, 2859, 2862, 2897, 2904,
            2864, 2959, 2861, 2887, 5833, 2877, 2880, 2863, 2956, 2871,
            2958,
        ]
        characters = self.vndb.get_all_character(
            Character.id == sengoku_rance_characters_ids, Flag.BASIC)
        self.assertEqual(len(characters), len(sengoku_rance_characters_ids))
        unique_ids = set([
            character.id for character in characters
        ])
        self.assertEqual(len(unique_ids), len(sengoku_rance_characters_ids))

    def test_limit(self):
        options = GetCommandOptions()
        options.limit = 15
        characters = self.vndb.get_all_character(
            Character.id != 1, Flag.BASIC, options)
        self.assertTrue(len(characters) >= 15)
        self.assertTrue(len(characters) < 50)
        unique_ids = set([
            character.id for character in characters
        ])
        self.assertTrue(len(unique_ids) >= 15)
        self.assertTrue(len(unique_ids) < 50)
