import unittest
from nestdict import Schema
from nestdict import Field


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.simple_schema = Schema(
            type=dict,
            items={
                "name": Field(str),
                "age": Field(int),
                "email": Field(str, required=True),
            },
        )

        self.complex_schema = Schema(
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
                        "zipcode": Field(str),
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

    def test_simple_schema_valid(self):
        data = {
            "name": "John Doe",
            "age": 30,
            "email": "john.doe@example.com",
        }
        self.assertTrue(self.simple_schema.validate(data))

    def test_simple_schema_missing_optional_field(self):
        data = {"name": "John Doe", "email": "test@gmail.com"}
        self.assertTrue(self.simple_schema.validate(data))

    def test_simple_schema_missing_required_field(self):
        data = {"name": "John Doe", "age": 50}
        with self.assertRaises(ValueError):
            self.simple_schema.validate(data)

    def test_complex_schema_valid(self):
        data = [
            {
                "id": 1,
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zipcode": "12345",
                },
                "posts": [
                    {
                        "title": "First Post",
                        "content": "This is the first post.",
                        "tag": "welcome",
                    }
                ],
            },
            {
                "id": 2,
                "name": "Jane Doe",
                "age": 25,
                "address": {
                    "street": "456 Elm St",
                    "city": "Othertown",
                    "zipcode": "54321",
                },
                "posts": [
                    {
                        "title": "Second Post",
                        "content": "This is the second post.",
                        "tag": "news",
                    }
                ],
            },
        ]
        self.assertTrue(self.complex_schema.validate(data))

    def test_complex_schema_missing_required_field(self):
        data = [
            {
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zipcode": "12345",
                },
                "posts": [
                    {
                        "title": "First Post",
                        "content": "This is the first post.",
                        "tag": "welcome",
                    }
                ],
            }
        ]
        with self.assertRaises(ValueError):
            self.complex_schema.validate(data)

    def test_complex_schema_duplicate_unique_field(self):
        data = [
            {
                "id": 1,
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zipcode": "12345",
                },
                "posts": [
                    {
                        "title": "First Post",
                        "content": "This is the first post.",
                        "tag": "welcome",
                    }
                ],
            },
            {
                "id": 1,
                "name": "Jane Doe",
                "age": 25,
                "address": {
                    "street": "456 Elm St",
                    "city": "Othertown",
                    "zipcode": "54321",
                },
                "posts": [
                    {
                        "title": "Second Post",
                        "content": "This is the second post.",
                        "tag": "news",
                    }
                ],
            },
        ]
        with self.assertRaises(ValueError):
            self.complex_schema.validate(data)

    def test_complex_schema_invalid_nested_schema(self):
        data = [
            {
                "id": 1,
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zipcode": 12345,  # Invalid type for zipcode
                },
                "posts": [
                    {
                        "title": "First Post",
                        "content": "This is the first post.",
                        "tag": "welcome",
                    }
                ],
            }
        ]
        with self.assertRaises(ValueError):
            self.complex_schema.validate(data)

    def test_complex_schema_invalid_list_item(self):
        data = [
            {
                "id": 1,
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zipcode": "12345",
                },
                "posts": [
                    {
                        "title": "First Post",
                        "content": "This is the first post.",
                        "tag": ["intro"],  # Invalid type for tags
                    }
                ],
            }
        ]
        with self.assertRaises(ValueError):
            self.complex_schema.validate(data)


if __name__ == "__main__":
    unittest.main()
