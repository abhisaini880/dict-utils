from .base import BaseNestDict
from .field import Field
from .schema import Schema


class NestDict(BaseNestDict):
    def __init__(self, data=None, schema={}):
        self.schema = schema
        if not schema or (schema and schema.validate(data)):
            super().__init__(data)

    def __setitem__(self, key_path, value):
        if self.schema:
            keys = key_path.split(".")
            schema = self.schema
            for key in keys:

                # if schema is of type list, then we need to check if the key is an index
                if isinstance(schema, Schema) and schema.type == list:
                    if key.startswith("[") and key.endswith("]"):
                        schema = schema.items
                    else:
                        raise ValueError(f"Invalid schema for key {key_path}")
                # if schema is of type dict, then we need to check if the key is a key in the dict
                elif isinstance(schema, Schema) and schema.type == dict:
                    schema = schema.items.get(key)

                # if schema is of type Schema, then we need to check if the key is a key in the items dict
                elif isinstance(schema, dict):
                    schema = schema.get(key)

            if schema and isinstance(schema, Field):
                schema.validate(value)

        return super().__setitem__(key_path, value)

    def __delitem__(self, key_path):

        if self.schema:
            keys = key_path.split(".")
            schema = self.schema
            for key in keys:

                # if schema is of type list, then we need to check if the key is an index
                if isinstance(schema, Schema) and schema.type == list:
                    if key.startswith("[") and key.endswith("]"):
                        schema = schema.items
                    else:
                        raise ValueError(f"Invalid schema for key {key_path}")
                # if schema is of type dict, then we need to check if the key is a key in the dict
                elif isinstance(schema, Schema) and schema.type == dict:
                    schema = schema.items.get(key)

                # if schema is of type Schema, then we need to check if the key is a key in the items dict
                elif isinstance(schema, dict):
                    schema = schema.get(key)

            if schema and isinstance(schema, Field):
                schema.validate(None)

        return super().__delitem__(key_path)


__all__ = ["NestDict", "Field", "Schema"]
