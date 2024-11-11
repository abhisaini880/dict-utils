import timeit

from nestdict import NestDict
from copy import deepcopy

# Sample data with more complex nested structures
sample_data = {
    "user": {
        "name": "Alice",
        "age": 30,
        "address": {
            "city": "Wonderland",
            "zip": 12345,
            "coordinates": {"lat": 52.52, "long": 13.405},
        },
        "contacts": [
            {"type": "email", "value": "alice@example.com"},
            {"type": "phone", "value": "123-456"},
        ],
    },
    "preferences": {
        "language": ["English", "French"],
        "timezone": "UTC",
        "notifications": {
            "email": True,
            "sms": False,
            "push": {"enabled": True, "sound": "default"},
        },
    },
}

nest_dict = NestDict(data=deepcopy(sample_data))
regular_dict = deepcopy(sample_data)


# Function to test NestDict operations
def test_nestdict_operations():
    nest_dict = NestDict(data=deepcopy(sample_data))
    nest_dict["user.phone"] = "123-456"
    _ = nest_dict["user.name"]
    _ = nest_dict.get("user.contacts.[].value")
    del nest_dict["user.address.city"]
    nest_dict["preferences.notifications.push.sound"] = "silent"
    _ = nest_dict["preferences.notifications.push.sound"]


# Function to test regular dict operations
def test_dict_operations():
    regular_dict = deepcopy(sample_data)
    regular_dict["user"]["phone"] = "123-456"
    _ = regular_dict["user"]["name"]
    _ = [val["value"] for val in regular_dict["user"]["contacts"]]
    del regular_dict["user"]["address"]["city"]
    regular_dict["preferences"]["notifications"]["push"]["sound"] = "silent"
    _ = regular_dict["preferences"]["notifications"]["push"]["sound"]


# Measure time
nestdict_time = timeit.timeit(test_nestdict_operations, number=1)
dict_time = timeit.timeit(test_dict_operations, number=1)


print(f"NestDict time: {nestdict_time:.6f} seconds")
print(f"Regular dict time: {dict_time:.6f} seconds")
