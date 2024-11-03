""" Implements the dict and list schema classes """

from .field import Field
from typing import Union


class Schema:
    """
    A class to represent a schema for nested dictionaries or lists.
    Attributes:
    -----------
    items : dict[str, Field]
        A dictionary where keys are strings and values are Field objects.
    type : list | dict
        The type of the schema, which can be either a list or a dictionary.
    unique_fields : list, optional
        A list of fields that must be unique within the schema (default is an empty list).
    min_length : int, optional
        The minimum length of the schema (default is None).
    max_length : int, optional
        The maximum length of the schema (default is None).
    """

    def __init__(
        self,
        items: dict[str, Union[Field, "Schema"]],
        type: type[list] | type[dict],
        unique_fields: list = [],
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> None:
        self.items = items
        self.type = type
        self.unique_fields = unique_fields
        self.min_length = min_length
        self.max_length = max_length
        self._validate_schema()

    def _validate_schema(self):
        self._validate_items()
        self._validate_type()
        self._validate_unique_fields()
        self._validate_length()

    def _validate_items(self):
        """
        Validates the items attribute of the schema.

        This method checks if the items attribute is a dictionary and if each
        item in the dictionary is an instance of the Field class. If either
        condition is not met, a ValueError is raised.

        Raises:
            ValueError: If items is not a dictionary or if any item in the
                        dictionary is not an instance of the Field class.
        """
        if not isinstance(self.items, dict):
            raise ValueError("Schema items must be a dictionary")

        for _, field in self.items.items():
            if not isinstance(field, Field | Schema):
                raise ValueError("Schema items must be of type Field")

    def _validate_type(self):
        """
        Validates the type attribute of the schema.

        This method checks if the type attribute is a list or a dictionary. If
        the type attribute is not a list or a dictionary, a ValueError is
        raised.

        Raises:
            ValueError: If the type attribute is not a list or a dictionary.
        """
        if not self.type in [list, dict]:
            raise ValueError("Schema type must be a list or dict")

    def _validate_unique_fields(self):
        """
        Validates the unique_fields attribute of the schema.

        This method checks if the unique_fields attribute is a list. If the
        unique_fields attribute is not a list, a ValueError is raised.

        Raises:
            ValueError: If the unique_fields attribute is not a list.
        """
        if not isinstance(self.unique_fields, list):
            raise ValueError("Schema unique fields must be a list")

    def _validate_length(self):
        """
        Validate the min_length and max_length attributes.

        This method checks if the min_length and max_length attributes are
        integers and if the min_length is less than the max_length. If either
        condition is not met, a ValueError is raised.

        Raises:
            ValueError: If min_length is greater than max_length.
            ValueError: If min_length or max_length are not integers.

        """

        if (
            self.min_length is not None
            and not isinstance(self.min_length, int)
            and self.min_length < 0
        ):
            raise ValueError(
                "Schema min length must be an integer and greater than 0"
            )

        if (
            self.max_length is not None
            and not isinstance(self.max_length, int)
            and self.max_length < 0
        ):
            raise ValueError(
                "Schema max length must be an integer and greater than 0"
            )

    def validate(self, value) -> bool:
        """
        Validate the value against the schema.

        Args:
            value (_type_): _description_

        Returns:
            bool: _description_
        """

        if not isinstance(value, self.type):
            raise ValueError(
                f"Expected type {self.type} but got {type(value)}"
            )

        if self.type == list:
            if self.min_length is not None and len(value) < self.min_length:
                raise ValueError(
                    f"Length {len(value)} is less than minimum limit {self.min_length}"
                )

            if self.max_length is not None and len(value) > self.max_length:
                raise ValueError(
                    f"Length {len(value)} is greater than maximum limit {self.max_length}"
                )

            if self.unique_fields:
                unique_field_values = {
                    key: set() for key in self.unique_fields
                }
                for item in value:
                    for key in self.unique_fields:
                        if key in item:
                            unique_field_values[key].add(item[key])

                for key, unique_values in unique_field_values.items():
                    if len(unique_values) != len(value):
                        raise ValueError(
                            f"Field {key} must have unique values"
                        )

            # check if value is not another schema
            # add check for value too
            for item in value:
                for key, field in self.items.items():
                    field.validate(item.get(key))

        elif self.type == dict:
            for key, field in self.items.items():
                field.validate(value.get(key))

        return True


if __name__ == "__main__":
    schema_obj = Schema(
        items={
            "name": Field(str, min_length=1, max_length=50),
            "age": Field(int, min=0, max=100),
            "jobs": Schema(
                type=list,
                items={"title": Field(str), "company": Field(str)},
                min_length=1,
                unique_fields=["company"],
            ),
        },
        type=dict,
        unique_fields=["name"],
        min_length=1,
        max_length=2,
    )

    data = {
        "name": "John Doe",
        "age": 30,
        "jobs": [],
    }

    schema_obj.validate(data)
