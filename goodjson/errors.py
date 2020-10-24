import copy


class ErrorMessage:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.formatter = None

    def clone(self):
        return ErrorMessage(self.name, self.description)

    def format(self, **kwargs):
        """
        Create a parameterized version of this error message with given formatter
        that complements the error description.

        FIXME: a more proper implementation would be making this class totally immutable.
        """
        formatter = copy.deepcopy(kwargs)
        sibling = self.clone()
        sibling.description = self.description.format(**formatter)
        sibling.formatter = formatter
        return sibling

    def to_json(self):
        return {
            'type': self.name,
            'formatter': self.formatter or dict(),
            'description': self.description
        }

    def __hash__(self):
        if isinstance(self.formatter, dict):
            formatter_hash = hash(tuple(sorted(self.formatter.items())))
            return formatter_hash + hash(self.name)
        else:
            return hash(self.name)

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description


"""
Pre-defined error messages
"""
invalid_json = ErrorMessage(
    'invalid_json',
    'This JSON is invalid because: {reason}')
unknown_error = ErrorMessage(
    'unknown',
    'something unexpected went wrong')
not_found = ErrorMessage(
    'not_found',
    '{object} is not found')
not_allowed = ErrorMessage(
    'not_allowed',
    'value is not allowed, only accepts {options}')
missing_columns = ErrorMessage(
    'missing_columns',
    'incomplete data with missing fields.')
not_unique = ErrorMessage(
    'not_unique',
    '{content} is not unique')
has_nan = ErrorMessage(
    'has_nan',
    '{content} contains empty values or NaN')
not_type = ErrorMessage(
    'not_type',
    'not {type} type')
too_small = ErrorMessage(
    'too_small',
    'values are smaller than {min}')
too_large = ErrorMessage(
    'too_large',
    'values are greater than {max}')
out_of_range = ErrorMessage(
    'out_of_range',
    'values are not within range {min} ~ {max}')
not_positive = ErrorMessage(
    'not_positive',
    'values are not positive')
not_negative = ErrorMessage(
    'not_negative',
    'values are not negative')
out_of_range = ErrorMessage(
    'out_of_range',
    'values are out of range {min} ~ {max}')
not_ending_with = ErrorMessage(
    'not_ending_with',
    'value not ending with {suffix}')
empty_value = ErrorMessage(
    'empty_value',
    'value is empty')
