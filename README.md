# NestDict: Advanced data structures for complex data

![PyPI](https://img.shields.io/pypi/v/nestdict) ![Python Versions](https://img.shields.io/badge/python-3.6%2B-yellow) ![PyPI Downloads](https://img.shields.io/pypi/dm/nestdict) ![License](https://img.shields.io/pypi/l/nestdict
)


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Overview

`NestDict` is a powerful Python library that extends the standard dictionary functionality to handle nested dictionaries, providing advanced features such as validation and support for frozen dictionaries. This library simplifies the manipulation of complex data structures, making it an ideal choice for applications that require dynamic data management.

## Features

- **Nested Dictionary Handling**: Seamlessly access and manipulate deeply nested dictionaries.
- **Validation**: Validate data types based on predefined mappings, including support for complex data structures.
- **Advanced Validation**: Supports additional validation rules such as value ranges, required fields, and uniqueness constraints.
- **Dynamic Type Checking**: Automatically validate data types whenever a value is updated.


## Installation

You can install `NestDict` using pip:

``` bash
pip install nestdict
```

## Usage
Here’s a quick example of how to use NestDict:
``` python
from nestdict import NestDict, Field, Schema

# Create a nested dictionary
data = [
    {
        "id": 1001,
        "name": "John Doe",
        "age": 30,
        "address": {"city": "New York", "zip": "10001"},
    },
    {
        "id": 1002,
        "name": "Mira",
        "age": 25,
        "address": {"city": "Chicago", "zip": "40002"},
    },
]

# Define schema
user_schema = Schema(
    type=list,
    items={
        "id": Field(int, required=True),
        "name": Field(str, required=True),
        "age": Field(int, required=True, min=0, max=120),
        "address": Schema(
            type=dict,
            items={
                "city": Field(str, required=True),
                "zip": Field(str, required=True)
            }
        )
    },
    min_length=1,
    max_length=1000,
    unique_fields=["id"],
)

# Initialize NestDict
nested_dict = NestDict(data=data, schema=user_schema)

# Access nested data
print(nested_dict.get("[0].name"))  # Output: "John Doe"
print(nested_dict.get("[].name"))  # Output: ["John Doe", "Mira"]

# Set new values
nested_dict["[0].age"] =  31

# This will raise a ValueError because the age must be an integer
try:
    nested_dict["[0].age"] = "thirty-five"
except ValueError as e:
    print(e)  # Output: user.age must be of type <class 'int'>

# Delete nested data
del nested_dict["[0].address.city"]
print(nested_dict.get("[0].address.city"))  # Output: None

# print out dict
print(nested_dict)

# save final dict object
final_dict = nested_dict.to_dict()

```
## API Reference

### NestDict

- `get(key_path, default=None)`
Retrieves the value at the specified key path in the nested dictionary. If the key path does not exist, it returns the specified default value (or `None` if not provided).

- `__getitem__(key_path)`
Allows access to the value at the specified key path using bracket notation (e.g., `nested_dict[key_path]`). Raises a `KeyError` if the key path is not found.

- `__setitem__(key_path, value)`
Sets the value at the specified key path using bracket notation (e.g., `nested_dict[key_path] = value`). It validates the value's type according to the validation rules if provided during initialization.

- `__delitem__(key_path)`
Deletes the value at the specified key path. If the key path does not exist, it raises a `KeyError`.

- `to_dict()`
Returns the nested structure as a standard dictionary, representing the current state of the data.

### Schema

- `Schema(type, items, unique_fields=[], min_length=None, max_length=None)`
Define a schema for nested data structures.
- `validate(data)`
Validate data against the schema.

### Field

- `Field(field_type, required=False, default=None, immutable=False, min=None, max=None, min_length=None, max_length=None, pattern=None, choices=None, dependencies=None, name="Field")`
Define a field with validation rules.
- `validate_value(value)`
Validate a value against the field constraints.

### Data Parameter

The **data** parameter is the initial nested dictionary structure that you want to manage using the `NestDict` class. It can be any valid Python dictionary (or list of dictionaries) that you need to work with.

#### Key Points:
- **Type**: Accepts a `dict` or `list`.
- **Nested Structure**: You can create deeply nested dictionaries. For example, `{"a": {"b": {"c": 1}}}` is a valid input.
- **Mutable**: The data is mutable, meaning you can modify it using the available methods like `set`, `delete`, or through direct item access.


## Contributing Guidelines

Contributions to NestDict are welcome! To maintain a high standard for our project, please follow these guidelines when contributing:

1. **Fork the Repository**: Start by forking the repository to your account.

2. **Create a New Branch**: Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/YourFeatureName
    ```
3. **Make Changes**: Implement your changes and ensure that your code adheres to our coding standards.

4. **Write Tests**: If applicable, add unit tests to cover your changes. Ensure that all tests pass before submitting your changes.

5. **Commit Your Changes**: Use clear and concise commit messages that explain the purpose of the changes. Refer to the COMMIT_GUIDELINES.md for detailed commit message conventions.

6. **Push Your Branch**: Push your changes to your fork:

    ```bash
    git push origin feature/YourFeatureName
    ```
7. **Submit a Pull Request**: Navigate to the original repository and submit a pull request, explaining your changes and the motivation behind them.

8. **Respect the License**: Ensure that any contributions you make do not violate the existing license terms. Contributions should not be commercialized without explicit permission.

*Thank you for contributing to NestDict!*

## Commit Guidelines
We follow specific conventions for our commit messages to maintain clarity and consistency. Please refer to the [COMMIT_GUIDELINES.md](COMMIT_GUIDELINES.md) file for detailed commit message conventions.

## License
This project is licensed under the MIT License. See the [License](LICENSE) file for more details.
