from typing import Any, Callable, Tuple, Optional, TypeVar, Union
from typing_extensions import TypedDict
from .errors import ErrorMessage


T = TypeVar('T')

Number = Union[float, int]


class ValidationFail(TypedDict):
    error: ErrorMessage
    # JSON entries delimited by "$", the last item is the troublesome data
    location: Optional[str]


class DataAndPath(TypedDict):
    data: Any
    path: str


"""
Two types of bool returns.
1. Checker: same as boolean type, just true or false
2. Informative Checker: a bit more useful and returns some second argument to provide contextual information

Checker function simply takes some value and tells it meets some criteria or not
"""
ChekerReturn = bool

InformativeCheckerReturn = Tuple[bool, Optional[T]]

CheckerFunction = Callable[..., ChekerReturn]


"""
Validator function is an enhanced type of checker that tells exactly where and why
some data failed to pass a test
"""
ValidatorReturn = InformativeCheckerReturn[ValidationFail]

ValidatorFunction = Callable[..., ValidatorReturn]
