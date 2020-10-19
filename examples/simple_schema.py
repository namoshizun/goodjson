import uuid
from goodjson.validators import foreach, foreach_key, is_list, is_integer, gj_all, \
    is_uuid, is_float, is_number, is_null, is_between, \
    is_positive, is_negative, is_not_empty, is_categorical


"""
Example:

Check a simple homogeneous list
"""
data = [1, 2, 3, 4]

# Assert a list
print(is_list()(data))


validate_fn = gj_all(
    # Assert a list of integers
    is_list(),
    foreach(is_integer)
)
print(validate_fn(data))


"""
Example:

Check a simple dict
"""
data = {
    'year': 2020,
}

validate_fn = foreach_key(
    year=[is_integer],
)
print(validate_fn(data))


"""
Example 3.

Check various built-in validators
"""
test_set = {
    'is_integer': (10, is_integer),
    'is_float': (10.2, is_float),
    'is_uuid': (str(uuid.uuid4()), is_uuid),
    'is_between': (5, is_between(0, 10, inclusive=True)),
    'is_null': ('', is_null),
    'is_not_empty': ('', is_not_empty),
    'is_categorical': (
        'east',
        is_categorical(['east', 'west', 'north', 'south'])
    ),
    'is_positive': (-10, is_positive),
    'is_negative': (1e-4, is_negative),
    'is_number': ('10', is_number),
}


for validator_name, data_and_validator in test_set.items():
    data, validate_fn = data_and_validator
    ok, err = validate_fn(data)
    print('Validator: ', validator_name)
    print(f'Data: {data} ({type(data)} type)')
    print(f'Result: {"good" if ok else "bad"}, {err or ""}')
    print('=' * 10)
