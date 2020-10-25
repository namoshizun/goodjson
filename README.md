# GoodJSON
GoodJSON enables a way of building declarative JSON validation workflows through validator composition.

Coming up in v0.2.0
* Return all validation errors found instead of early quitting.
* Lazy run through of validators.
* More higher order validators.

## Installation
* Require Python >= 3.6.
* Install from GitHub: `pip install git+https://github.com/namoshizun/goodjson.git@main`


## Usage
#### Validator Function
A GoodJSON validator is a function with signature `Callable[..., Tuple[bool, ValidationFail]]`. It takes any data and returns True/False based its validity, and a `ValidationFail` object to tell exactly what value failed to meet which requirement. Each validator must accompany an `ErrorMessage`. For example, we can create a parameterizable validator that checks string prefix like below:

```python
from goodjson.errors import ErrorMessage
from goodjson.types import ValidatorFunction, CheckerReturn
from goodjson.decorators import validator


prefix_not_found = ErrorMessage(
    name='prefix_not_found',
    description='Expected prefix {prefix} is not found'
)

def has_prefix_value(begin_value: str) -> ValidatorFunction:

    @validator(prefix_not_found.format(prefix=begin_value))
    def checker(value: str) -> CheckerReturn:
        # ...
        # DO WHATEVER YOU WANT BECAUSE IT IS JUST A FUNCTION!
        return value.startswith(begin_value)

    return checker


ok, val_fail = has_prefix_value('GJ')('__notGood!')
"""
Expect "val_fail" to be printed as the following.
"path" is a dollar-sign demilited string pointing where the erroneous value is at.
Every "path" always starts with "_root_" representing the validator's input data itself.

{
    'error': 'Expected prefix GJ is not found',
    'data': {
        'path': '_root_'
        'value': '__notGood!'
    }
}
"""
```



#### Primitive Validators
These are functions validating values of primitive JSON types (string, number, boolean and null). GoodJSON has already implemented several such validators such as `is_categorical`, `is_between`, `is_of_type` and `is_not_empty` etc, which can be imported from `goodjson.validators`. Check out ./examples/simple_schema.py for more examples.


#### Higher Order Validators
They run a series of validators to name/value pair and list data structures. Using them, you can compose highly flexible and complex validations in a very exprssive manner. GoodJSON implements three higher order validators:

* **foreach**: `(*validators: ValidatorFunction) -> ValidatorFunction`, applies validators to each element of an iterable data.
* **foreach_key**: `(OPTIONAL_KEYS=tuple(), **validators: List[ValidatorFunction]) -> ValidatorFunction`, applies key-paired validators to a dict-like data.
* **gj_all**: `(*validators: ValidatorFunction) -> ValidatorFunction`, feeds the input data to each validator and passes if all validators return no error.

Below is an example of building a JSON validation through validator composition. Check out ./examples/complex_schema.py for more examples.

```python
# ... reusing the has_prefix_value defined before
from goodjson.validators import foreach_key, foreach, is_string, is_list

is_good_json = foreach_key(
    codes=[
        is_list(),
        foreach(is_string, has_prefix_value('GJ_'))
    ]
)

ok, val_fail = is_good_json({ 'codes': ['GJ_00001', '_00010'] })
"""
Expect "val_fail" to be printed as: 

{
    "error": "Expected prefix GJ_ is not found",
    "data": {
        "path" : "_root_$codes$1",
        "value": "_00010"
    }
}
"""
```
