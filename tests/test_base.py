import unittest
from nestdict import NestDict


class TestBase(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "user": {
                "name": "Alice",
                "age": 30,
                "address": {"city": "Wonderland", "zip": 12345},
            },
            "preferences": {
                "language": ["English", "French"],
                "timezone": "UTC",
            },
        }
        self.nest_dict = NestDict(data=self.sample_data)

    def test_get_existing_key(self):
        self.assertEqual(self.nest_dict.get("user.name"), "Alice")
        self.assertEqual(
            self.nest_dict.get("user.address.city"), "Wonderland"
        )

    def test_get_non_existing_key(self):
        self.assertIsNone(self.nest_dict.get("user.phone"))

    def test_get_non_existing_key_with_default(self):
        self.assertEqual(
            self.nest_dict.get("user.phone", "123-456"), "123-456"
        )

    def test_set_new_key(self):
        self.nest_dict["user.phone"] = "123-456"
        self.assertEqual(self.nest_dict.get("user.phone"), "123-456")

    def test_set_existing_key(self):
        self.nest_dict["user.name"] = "Bob"
        self.assertEqual(self.nest_dict.get("user.name"), "Bob")

        self.nest_dict["user.address"] = {"city": "test_city_1", "zip": 54321}
        self.assertEqual(
            self.nest_dict.get("user.address.city"), "test_city_1"
        )
        self.assertEqual(
            self.nest_dict.get("user.address"),
            {"city": "test_city_1", "zip": 54321},
        )

        self.nest_dict["preferences.timezone"] = "IST"
        self.assertEqual(
            self.nest_dict.get("preferences"),
            {"language": ["English", "French"], "timezone": "IST"},
        )

    def test_delete_key(self):
        self.assertEqual(self.nest_dict["user.address.city"], "Wonderland")

        self.nest_dict.delete("user.address")
        self.assertIsNone(self.nest_dict.get("user.address"))
        self.assertIsNone(self.nest_dict.get("user.address.city"))

        dict_data = self.nest_dict.to_dict()
        self.assertIsNone(dict_data["user"].get("address"))
