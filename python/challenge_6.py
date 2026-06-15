import sys

class JSONValidationError(Exception):
    pass

def validate_json(data, path="root", error_list=None):
    # initialize error_list on first call - needed for recursive calls
    if error_list is None:
        error_list = []
        is_top_level = True
    else:
        is_top_level = False

    # check invalid basic values
    if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
        error_list.append(f"Invalid value type '{type(data).__name__}' at {path}")
    # value is a dictionary (needed for recursive calls)
    elif isinstance(data, dict):
        # iterate over dictionary key:value pairs
        for key, val in data.items():
            # bad key
            if not isinstance(key, str):
                error_list.append(f"Bad Key: '{key}' is a {type(key).__name__}")
            # check value - dictionary
            new_path = f"{path}[{key}]"
            validate_json(val, new_path, error_list)
            # check value - list
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            validate_json(item, new_path, error_list)
    if is_top_level:
        # no errors
        if len(error_list) == 0:
            return {"valid" : True, "Errors" : []}
        else:
            # errors
            raise JSONValidationError({"valid" : False, "Errors" : error_list})

    
            
# Test 1 - valid JSON-like dictionary
valid_data = {
    "name": "Mike",
    "age": 52,
    "active": True,
    "scores": [10, 20, 30],
    "profile": {
        "city": "Birmingham",
        "languages": ["English", "French"],
        "meta": {
            "verified": False,
            "rating": 4.8
        }
    },
    "misc": None
}

print(validate_json(valid_data))

# Test 2 - invalid key type (not a string)

invalid_key = {
    123: "number key",
    "ok": "fine"
}

print(validate_json(invalid_key))

# Test 3 - invalid value type (set not allowed)

invalid_value = {
    "name": "Mike",
    "bad": {1, 2, 3}   # set is invalid
}

print(validate_json(invalid_value))

# Test 4 - list contains invalid JSON types

invalid_list = {
    "items": ["ok", 123, None, {"x": 1}, {1, 2}]  # set inside list
}

print(validate_json(invalid_list))

# Test 5  - nested dictionary with invalid key

invalid_nested_key = {
    "outer": {
        "inner": {
            99: "bad key"   # invalid
        }
    }
}

print(validate_json(invalid_nested_key))

# Test 6 - nested dictionary with invalid value

invalid_nested_value = {
    "outer": {
        "inner": {
            "ok": lambda x: x   # function is invalid
        }
    }
}

print(validate_json(invalid_nested_value))

# Test 7 - multiple errors

multiple_errors = {
    123: "bad key",
    "list": [1, 2, {3, 4}],     # set inside list
    "nested": {
        "ok": 1,
        999: "bad nested key"
    }
}

print(validate_json(multiple_errors))