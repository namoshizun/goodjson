import re
import operator
from functools import partial
from enum import Enum
from typing import List, Tuple, Union, Dict, Any, Type, Set

from goodjson import errors, exceptions, utils
from goodjson.types import \
    Number, ChekerReturn, ValidatorFunction, ValidatorReturn
from goodjson.decorators import validator


# ------------------------------
# Not parameterizable validators
@validator(errors.not_negative)
def is_negative(number: Number) -> ChekerReturn:
    return number < 0


@validator(errors.not_positive)
def is_positive(number: Number) -> ChekerReturn:
    return number > 0


@validator(errors.empty_value)
def is_not_empty(value: Any) -> ChekerReturn:
    if type(value) in (list, set, str):
        return bool(value)
    return value


@validator(errors.unknown_error)
def is_optional(value: Any) -> ChekerReturn:
    """
    It is a rather special validator because it never returns False and emits an exception
    signal when the value is correct instead of returning True.

    Its user should catch the signal to short-circuit the validation chain.
    """
    if value is None:
        raise exceptions.ValueNotRequired()
    return True


@validator(errors.not_type.format(type='UUID'))
def is_uuid(value: str):
    UUID_REGEX = r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$'
    return bool(re.match(UUID_REGEX, value))


# --------------------------
# Parameterizable validators
def is_type(types: Union[Type, Tuple[Type]], type_name: str) -> ValidatorFunction:
    @validator(errors.not_type.format(type=type_name))
    def inner(value: Any) -> ChekerReturn:
        return isinstance(value, utils.force_tuple(types))
    return inner


def is_list(size=None) -> ValidatorFunction:
    assert type(size) in (int, type(None), tuple)
    type_name = 'list'

    if isinstance(size, int):
        assert size > 0, 'list size must be positive'
    if isinstance(size, tuple):
        assert all(x > 0 for x in size), 'list size must be positive'
    if size is not None:
        type_name += f' of {size} elements'

    @validator(errors.not_type.format(type=type_name))
    def inner(value: Any) -> ChekerReturn:

        if not isinstance(value, list):
            return False
        if isinstance(size, int):
            return size == len(value)
        if isinstance(size, tuple):
            return size == utils.get_matrix_size(value)

        return True
    return inner


def is_greater_than(min_val, inclusive=False) -> ValidatorFunction:
    @validator(errors.too_small.format(min=min_val))
    def inner(number: Number) -> ChekerReturn:
        if inclusive:
            return number >= min_val
        return number > min_val
    return inner


def is_less_than(max_val, inclusive=False) -> ValidatorFunction:
    @validator(errors.too_large.format(max=max_val))
    def inner(number: Number) -> ChekerReturn:
        if inclusive:
            return number <= max_val
        return number < max_val
    return inner


def is_between(min_val,
               max_val,
               inclusive=False,
               include_min=False,
               include_max=False) -> ValidatorFunction:
    if inclusive:
        include_min = include_max = True

    @validator(errors.out_of_range.format(min=min_val, max=max_val))
    def inner(number: Number) -> ChekerReturn:
        min_check = operator.ge if include_min else operator.gt
        max_check = operator.le if include_max else operator.lt
        return min_check(number, min_val) and max_check(number, max_val)
    return inner


def is_categorical(options: Union[Enum, List, Set], ignore_none=False) -> ValidatorFunction:

    if isinstance(options, list):
        acceptable_vals = set(options)
    elif isinstance(options, set):
        acceptable_vals = options
    elif issubclass(options, Enum):
        acceptable_vals = set([i.value for i in options])
    else:
        raise TypeError(f'{options} is not Enum, List or Set')

    @validator(errors.not_allowed.format(options=acceptable_vals))
    def inner(value: Any) -> ChekerReturn:
        if ignore_none and value is None:
            return True
        return value in acceptable_vals
    return inner


# -----------------------
# Higher-order validators
def foreach(*validators: ValidatorFunction) -> ValidatorFunction:
    """
    Apply a sequence of validators to each element in a list or tuple.
    Validation fail example:
    {
        "error": errors.has_na,
        "location": "0$name"   <- the first dict at [name] entry
    }
    """
    def inner(value: Union[List, Tuple]) -> ValidatorReturn:
        if type(value) not in (list, tuple):
            return False, {
                'error': errors.not_type.format(type='list or tuple'),
                'location': None
            }

        for idx, element in enumerate(value):
            try:
                for validate_fn in validators:
                    ok, val_fail = validate_fn(element)

                    if not ok:
                        loc = val_fail['location']
                        new_loc_suffix = '' if not loc else '$' + loc
                        val_fail['location'] = str(idx) + new_loc_suffix
                        return ok, val_fail
            except exceptions.ValueNotRequired:
                pass
        return True, None
    return inner


def foreach_key(OPTIONAL_KEYS=tuple(), **key_validators_pairs: List[ValidatorFunction]) -> ValidatorFunction:
    """
    For each key and its given validators, apply them to the corresponding value.
    Validation fail example:
    {
        "error": errors.has_na,
        "location": "user$name"  <- the [user][name] entry
    }
    """
    def inner(value: Dict[str, Any]) -> ValidatorReturn:
        if not isinstance(value, dict):
            return False, {
                'error': errors.not_type.format(type='dict'),
                'location': None
            }

        for key, validators in key_validators_pairs.items():
            # Ensure the key exists
            if key not in value:
                if key not in OPTIONAL_KEYS:
                    return False, {
                        'error': errors.not_found.format(object=key),
                        'location': key
                    }
                continue

            # Apply validators
            try:
                for validate_fn in validators:
                    ok, val_fail = validate_fn(value[key])
                    if not ok:
                        loc = val_fail['location']
                        new_loc_suffix = '' if not loc else '$' + loc
                        val_fail['location'] = key + new_loc_suffix
                        return ok, val_fail

            except exceptions.ValueNotRequired:
                pass
        return True, None
    return inner


def gj_any(*validators: ValidatorFunction) -> ValidatorFunction:
    def inner(value: Any) -> ValidatorReturn:
        some_ok = any(validate_fn(value)[0] for validate_fn in validators)
        if not some_ok:
            # FIXME
            return False, {
                'error': errors.unknown_error,
                'location': value
            }
        return True, None
    return inner


def gj_all(*validators: ValidatorFunction) -> ValidatorFunction:
    def inner(value: Any) -> ValidatorReturn:
        for validate_fn in validators:
            ok, val_fail = validate_fn(value)
            if not ok:
                return ok, val_fail
        return True, None
    return inner


# ----------
# Shorthands
is_string = is_type(str, 'text')
is_integer = is_type(int, 'integer')
is_float = is_type(float, 'decimal number')
is_boolean = is_type(bool, 'boolean')
is_null = is_type(type(None), 'null')
is_number = is_type((int, float), 'number')

is_gte = partial(is_greater_than, inclusive=True)
is_lte = partial(is_less_than, inclusive=True)
