from typing import Any, Callable, Tuple, Optional, TypeVar, Union
from typing_extensions import TypedDict
from .errors import ErrorMessage


T = TypeVar('T')

Number = Union[float, int]


class ValueAndPath(TypedDict):
    value: Any  # the JSON value that is causing problem
    path: str  # JSON entries delimited by "$"


class ValidationFail(TypedDict):
    error: ErrorMessage
    data: ValueAndPath


"""
Two types of bool returns.
1. Checker: same as boolean type, just true or false
2. Informative Checker: a bit more useful and returns some second argument to provide contextual information

Checker function simply takes some value and tells whether it meets some criteria or not
"""
ChekerReturn = bool

CheckerFunction = Callable[..., ChekerReturn]

InformativeCheckerReturn = Tuple[bool, Optional[T]]


"""
Validator function is an enhanced type of checker that tells exactly where and why
some data failed to pass a test
"""
ValidatorReturn = InformativeCheckerReturn[ValidationFail]

ValidatorFunction = Callable[..., ValidatorReturn]
