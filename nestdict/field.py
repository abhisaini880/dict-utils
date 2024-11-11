""" Implementation for the Field class. """

from typing import Any, List, Optional, Union
import re


class Field:
    """
    A class to represent a field with various validation and constraint options.

    Attributes:
    -----------
    field_type : Any
        The type of the field.
    required : bool, optional
        Indicates if the field is required (default is False).
    default : Any, optional
        The default value of the field (default is None).
    immutable : bool, optional
        Indicates if the field is immutable (default is False).
    min : Optional[Union[int, float]], optional
        The minimum value for the field (default is None).
    max : Optional[Union[int, float]], optional
        The maximum value for the field (default is None).
    min_length : Optional[int], optional
        The minimum length for the field (default is None).
    max_length : Optional[int], optional
        The maximum length for the field (default is None).
    pattern : Optional[str], optional
        A regex pattern that the field value must match (default is None).
    choices : Optional[List], optional
        A list of valid choices for the field value (default is None).
    dependencies : Optional[Dict[str, Any]], optional
        A dictionary of dependencies for the field (default is None).

    """

    def __init__(
        self,
        field_type: Any,
        required: bool = False,
        default: Any = None,
        immutable: bool = False,
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        choices: Optional[List] = None,
    ):
        self.field_type = field_type
        self.required = required
        self.default = default  # not implemented yet
        self.immutable = immutable  # not implemented yet
        self.min = min
        self.max = max
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        self.choices = choices

        self._validate_field()

    def _validate_field(self) -> None:
        """
        Validate all the args of Field class
        """

        self._validate_field_type()
        self._validate_required()
        self._validate_min_max()
        self._validate_length()
        self._validate_pattern()
        self._validate_choices()

    def _validate_field_type(self) -> None:
        """
        Validate the field type.

        Raises:
            TypeError: If the field type is not valid.
        """
        if not isinstance(self.field_type, type):
            raise TypeError("field_type must be a valid type")

    def _validate_required(self) -> None:
        """
        Validate the required attribute.

        Raises:
            TypeError: If the required attribute is not a boolean.
        """
        if not isinstance(self.required, bool):
            raise TypeError("required must be a boolean")

    def _validate_min_max(self) -> None:
        """
        Validate the min and max attributes.

        Raises:
            TypeError: If min or max are not numbers.
            ValueError: If min is greater than max.
        """
        if self.min is not None and not isinstance(self.min, (int, float)):
            raise TypeError("min must be an int or float")

        if self.max is not None and not isinstance(self.max, (int, float)):
            raise TypeError("max must be an int or float")

        if (
            self.min is not None
            and self.max is not None
            and self.min > self.max
        ):
            raise ValueError("min cannot be greater than max")

    def _validate_length(self) -> None:
        """
        Validate the min_length and max_length attributes.

        Raises:
            TypeError: If min_length or max_length are not integers.
            ValueError: If min_length is greater than max_length.
        """
        if self.min_length is not None and not isinstance(
            self.min_length, int
        ):
            raise TypeError("min_length must be an int")

        if self.max_length is not None and not isinstance(
            self.max_length, int
        ):
            raise TypeError("max_length must be an int")

        if (
            self.min_length is not None
            and self.max_length is not None
            and self.min_length > self.max_length
        ):
            raise ValueError("min_length cannot be greater than max_length")

    def _validate_pattern(self) -> None:
        """
        Validate the pattern attribute.

        Raises:
            ValueError: If the pattern is not a valid regex.
        """
        if self.pattern is not None:
            try:
                re.compile(self.pattern)
            except re.error:
                raise ValueError("pattern must be a valid regex")

    def _validate_choices(self) -> None:
        """
        Validate the choices attribute.

        Raises:
            TypeError: If choices is not a list.
        """
        if self.choices is not None and not isinstance(self.choices, list):
            raise TypeError("choices must be a list")

    def validate(self, value) -> bool:
        """
        Validate the value against the Field schema.

        Args:
            value (_type_): _description_

        Returns:
            bool: _description_
        """

        if self.required and value is None:
            raise ValueError("Field is required")

        if value is None:
            return True

        if not isinstance(value, self.field_type):
            raise ValueError(
                f"Expected type {self.field_type} but got {type(value)}"
            )

        if self.min is not None and value < self.min:
            raise ValueError(
                f"Value {value} is less than minimum limit {self.min}"
            )

        if self.max is not None and value > self.max:
            raise ValueError(
                f"Value {value} is greater than maximum limit {self.max}"
            )

        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(
                f"Length {len(value)} is less than minimum limit {self.min_length}"
            )

        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(
                f"Length {len(value)} is greater than maximum limit {self.max_length}"
            )

        if self.pattern is not None and not re.match(self.pattern, value):
            raise ValueError(
                f"Value {value} does not match pattern {self.pattern}"
            )

        if self.choices is not None and value not in self.choices:
            raise ValueError(
                f"Value {value} is not in choices {self.choices}"
            )

        return True


if __name__ == "__main__":
    name = Field(str, required=True, min_length=1, max_length=50)
    name.validate("john")
    name.validate("")
