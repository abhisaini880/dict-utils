import unittest
from nestdict import NestDict, Schema, Field


class TestNestDict(unittest.TestCase):

    def setUp(self):
        self.schema = Schema(
            type=list,
            items={
                "id": Field(int, required=True),
                "name": Field(str),
                "age": Field(int),
                "address": Schema(
                    type=dict,
                    items={
                        "street": Field(str),
                        "city": Field(str),
                        "zipcode": Field(int),
                    },
                ),
                "posts": Schema(
                    type=list,
                    items={
                        "title": Field(str),
                        "content": Field(str),
                        "tag": Field(str),
                    },
                    min_length=1,
                    unique_fields=["title"],
                ),
            },
            min_length=1,
            unique_fields=["id"],
        )
        self.valid_data = [
            {
                "id": 1,
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zipcode": 12345,
                },
                "posts": [
                    {
                        "title": "First Post",
                        "content": "This is the first post",
                        "tag": "first",
                    },
                    {
                        "title": "Second Post",
                        "content": "This is the second post",
                        "tag": "second",
                    },
                ],
            }
        ]
        self.invalid_data = {
            "name": "John Doe",
            "age": "thirty",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "zipcode": "12345",
            },
        }

    def test_initial_validation_success(self):
        try:
            nest_dict = NestDict(self.valid_data, self.schema)
        except ValueError:
            self.fail("NestDict raised ValueError unexpectedly!")

        self.assertEqual(nest_dict["[0].id"], 1)

    def test_initial_validation_failure(self):
        with self.assertRaises(ValueError):
            NestDict(self.invalid_data, self.schema)

    def test_set_data_success(self):
        nest_dict = NestDict(self.valid_data, self.schema)
        try:
            nest_dict["[0].age"] = 35
            nest_dict["[0].address.zipcode"] = 54321
        except ValueError:
            self.fail(
                "NestDict raised ValueError unexpectedly when setting valid data!"
            )

        self.assertEqual(nest_dict["[0].age"], 35)
        self.assertEqual(nest_dict["[0].address.zipcode"], 54321)

        final_dict = nest_dict.to_dict()

        self.assertEqual(final_dict[0]["age"], 35)
        self.assertEqual(final_dict[0]["address"]["zipcode"], 54321)

    def test_set_data_failure(self):
        nest_dict = NestDict(self.valid_data, self.schema)
        with self.assertRaises(ValueError):
            nest_dict["[0].address.zipcode"] = "54321"
            nest_dict["[0].age"] = "thirty"

    def test_set_invalid_data_failure(self):
        nestdict = NestDict(self.valid_data, self.schema)

        with self.assertRaises(ValueError):
            nestdict["age"] = 30

    def test_delete_data_success(self):
        nest_dict = NestDict(self.valid_data, self.schema)
        try:
            del nest_dict["[0].address.zipcode"]
            del nest_dict["[0].posts.[0].title"]
        except ValueError:
            self.fail(
                "NestDict raised ValueError unexpectedly when deleting valid data!"
            )

        self.assertNotIn("zipcode", nest_dict["[0].address"])
        self.assertNotIn("title", nest_dict["[0].posts"][0])

        final_dict = nest_dict.to_dict()

        self.assertNotIn("zipcode", final_dict[0]["address"])
        self.assertNotIn("title", final_dict[0]["posts"][0])

    def test_delete_data_failure(self):
        nest_dict = NestDict(self.valid_data, self.schema)
        with self.assertRaises(ValueError):
            del nest_dict["[0].id"]


if __name__ == "__main__":
    unittest.main()
