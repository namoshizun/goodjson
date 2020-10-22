# GoodJSON
GoodJSON gives a way of building declarative JSON validation workflows through composing simple validator functions. You can easily define your own "building block" validators and combine them with GoodJSON's builtin validators to perform highly flexible and complex validations.

Coming up in v0.2.0
* Return all validation errors found instead of early quitting.
* Lazy application of validators.
* More higher order validators.

## Installation
TODO


## Usage
TODO

```python
from goodjson.errors import ErrorMessage
from goodjson.types import ValidatorFunction, CheckerReturn
from goodjson.decorators import validator
from goodjson.validators import foreach_key, foreach, is_string, is_list

# Build own validator with custom error message
prefix_not_found = ErrorMessage(
    name='prefix_not_found',
    description='Expected prefix {prefix} is not found'
)

def has_prefix_value(begin_value: str) -> ValidatorFunction:

    @validator(prefix_not_found.format(prefix=begin_value))
    def checker(value: str) -> CheckerReturn:
        # ...
        # DO WHATEVER YOU WANT!
        return value.startswith(begin_value)

    return checker


# Do JSON object validation
is_good_json = foreach_key(
    codes=[
        is_list(),
        foreach(is_string, has_prefix_value('GJ_'))
    ]
)

ok, error = is_good_json({ 'codes': ['GJ_00001', '_00010'] })
"""
"error" should be: 

{
    "error": "Expected prefix GJ_ is not found",
    "data": {
        "path" : "_root_$codes$1",
        "value": "_00010"
    }
}
"""
```


## Examples
TODO
