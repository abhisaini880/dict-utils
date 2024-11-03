class BaseNestDict:
    """
    Base class for nested dictionary-like structures.

    This class provides the core functionality for flattening and accessing
    nested dictionaries and lists.

    Attributes:
        data (Union[Dict, List]): The nested data structure.
        flatten_dict (Dict[str, Any]): A flattened representation of the data.

    Methods:
        get(key_path: str, default: Any = None) -> Any:
            Retrieve a value from the nested structure using a dot-notation key path.

        __getitem__(key_path: str) -> Any:
            Access a value using square bracket notation.

        __setitem__(key_path: str, value: Any) -> None:
            Set a value in the nested structure using a dot-notation key path.

        delete(key_path: str) -> None:
            Remove a key-value pair from the nested structure.

        to_dict() -> Union[Dict, List]:
            Convert the nested structure back to a regular dictionary or list.
    """

    class __FlattenHelper:
        """Private helper class to handle flattening of data."""

        @staticmethod
        def flatten(data):
            """
            Flatten the data of dict for easy access
            """

            def _flatten_dict(data, parent_key=""):
                items = {}
                for key, value in data.items():
                    new_key = f"{parent_key}.{key}" if parent_key else key
                    items[new_key] = value
                    if isinstance(value, dict):
                        items.update(_flatten_dict(value, new_key))

                    elif isinstance(value, list):
                        items.update(_flatten_list(value, new_key))

                return items

            def _flatten_list(data, parent_key=""):
                items = {}

                for index, value in enumerate(data):
                    new_key = (
                        f"{parent_key}.[{index}]"
                        if parent_key
                        else f"[{index}]"
                    )
                    items[new_key] = value
                    if isinstance(value, dict):
                        items.update(_flatten_dict(value, new_key))

                    elif isinstance(value, list):
                        items.update(_flatten_list(value, new_key))

                return items

            if isinstance(data, dict):
                return _flatten_dict(data)

            elif isinstance(data, list):
                return _flatten_list(data)

            else:
                raise ValueError(
                    f"Expected data is list or dict got {type(data)}"
                )

    def __init__(self, data=None) -> None:
        self._data = data or {}
        self._flatten_dict = self.__FlattenHelper.flatten(self._data)

    def get(self, key_path, default=None):
        if "[]" in key_path:
            length = len(
                self._flatten_dict.get(key_path.split("[]")[0][:-1], [])
            )
            res = []
            for i in range(length):
                res.append(
                    self._flatten_dict.get(key_path.replace("[]", f"[{i}]"))
                )
            return res
        return self._flatten_dict.get(key_path, default)

    def __getitem__(self, key_path):
        if "[]" in key_path:
            length = len(self._flatten_dict[key_path.split("[]")[0][:-1]])
            res = []
            for i in range(length):
                res.append(
                    self._flatten_dict[key_path.replace("[]", f"[{i}]")]
                )
            return res

        if key_path not in self._flatten_dict:
            raise KeyError(
                f"`{key_path}` keypath not found, please check again!"
            )

        return self._flatten_dict[key_path]

    def __setitem__(self, key_path, value):

        # Update the flattened dictionary
        if isinstance(value, dict):
            for k, v in self.__FlattenHelper.flatten(value).items():
                self._flatten_dict[f"{key_path}.{k}"] = v
        elif isinstance(value, list):
            for i, item in enumerate(value):
                for k, v in self.__FlattenHelper.flatten(item).items():
                    self._flatten_dict[f"{key_path}.[{i}].{k}"] = v

        self._flatten_dict[key_path] = value

        keys = key_path.split(".")
        data = self._flatten_dict
        for index in range(len(keys[:-1])):
            if keys[index] not in data:
                data[keys[index]] = (
                    [{}] if keys[index + 1].startswith("[") else {}
                )
            data = data[keys[index]]

            if isinstance(data, list):
                data = data[0]

        data[keys[-1]] = value

    def delete(self, key_path):

        value_on_key_path = self._flatten_dict.get(key_path)
        if isinstance(value_on_key_path, dict):
            for k, _ in self.__FlattenHelper.flatten(
                value_on_key_path
            ).items():
                del self._flatten_dict[f"{key_path}.{k}"]
        elif isinstance(value_on_key_path, list):
            for i, item in enumerate(value_on_key_path):
                for k, _ in self.__FlattenHelper.flatten(item).items():
                    del self._flatten_dict[f"{key_path}.[{i}].{k}"]

        del self._flatten_dict[key_path]

        keys = key_path.split(".")
        data = self._flatten_dict
        for index in range(len(keys[:-1])):
            data = data[keys[index]]

        del data[keys[-1]]

    def to_dict(self):
        res_dict, res_list = {}, []
        for key, value in self._flatten_dict.items():
            key_list = key.split(".")
            if len(key_list) > 1:
                continue
            parent_key = key_list[0]
            if parent_key.startswith("["):
                res_list.append(value)
            else:
                res_dict[parent_key] = value

        return res_list or res_dict

    def __str__(self) -> str:
        return str(self.to_dict())
