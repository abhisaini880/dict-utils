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
                if key.startswith("["):
                    continue
                if isinstance(schema, Schema):
                    schema = schema.items.get(key)
                elif isinstance(schema, Field):
                    schema.validate(value)
                    break
                else:
                    raise ValueError(f"Invalid schema for key {key_path}")
        return super().__setitem__(key_path, value)


__all__ = ["NestDict", "Field", "Schema"]
