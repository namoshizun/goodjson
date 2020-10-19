from datetime import datetime
from goodjson.validators import \
    foreach, foreach_key, is_between, is_categorical, is_list, is_number, \
    is_string, is_float, gj_all, is_integer


"""
Example:

Check a list of dicts by chaining `foreach` and `foreach_key` higher order validators
"""
validate_fn = foreach_key(
    users=[
        is_list(),
        foreach(foreach_key(
            name=[is_string],
            age=[is_number],
            events=[
                is_list(),
                foreach(is_string)
            ]
        ))
    ]
)

print(validate_fn({
    'users': [
        {
            'name': 'hehe',
            'age': 30,
            'events': [
                'wake up',
                'sleep'
            ]
        }
    ]
}))


"""
Example:

Check a 3 x 4 matrix of decimal numbers
"""
validate_fn = gj_all(
    is_list(size=3),
    foreach(
        is_list(size=4),
        foreach(is_float)
    )
)

matrix_arr = [
    [1., 2., 3., 4.],
    [1., 2., 3., 4.],
    [1., 2., 3., 4.]
]

print(validate_fn(matrix_arr))


# Or just use `is_list` validator if you only want to check the matrix dimensions.
validate_fn = is_list(size=(3, 4))

print(validate_fn(matrix_arr))


# High-dimensional matrix
validate_fn = is_list(size=(2, 2, 1))

print(validate_fn([
    [[1], [2]],
    [[3], [4]]
]))


"""
Example:

Nested dictionary
"""
this_year = datetime.now().year
COUNTRY_LIST = ['country.1', 'country.2']

validate_fn = foreach_key(
    user=[foreach_key(
        birthday=[foreach_key(
            year=[is_integer, is_between(1900, this_year, inclusive=True)],
            month=[is_integer, is_between(1, 12, inclusive=True)],
            day=[is_integer, is_between(1, 30, inclusive=True)]
        )],
        birthplace=[foreach_key(
            country=[foreach_key(
                name=[is_categorical(COUNTRY_LIST)]
            )]
        )]
    )]
)


print(validate_fn({
    'user': {
        'birthday': {
            'year': 1950,
            'month': 12,
            'day': 1,
        },
        'birthplace': {
            'country': {
                'name': COUNTRY_LIST[0]
            }
        }
    }
}))
