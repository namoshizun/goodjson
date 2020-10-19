from typing import Any
from goodjson.errors import ErrorMessage
from goodjson.types import CheckerFunction, ValidatorFunction, ValidatorReturn, ValidationFail


def validator(message: ErrorMessage):
    """
    Turn a bare checker function into a descriptive validator function
    """
    def decor(fun: CheckerFunction) -> ValidatorFunction:
        def inner(value: Any) -> ValidatorReturn:
            ok = fun(value)

            if not ok:
                val_fail: ValidationFail = {
                    'error': message,
                    'location': str(value)
                }
            else:
                val_fail = None

            return ok, val_fail
        return inner
    return decor
