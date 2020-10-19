from typing import Any, Iterable, List, Tuple


def flatten(container: Iterable):
    for i in container:
        if isinstance(i, (list, tuple)):
            yield from flatten(i)
        else:
            yield i


def force_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    return [value]


def force_tuple(value: Any) -> Tuple[Any, ...]:
    if isinstance(value, tuple):
        return value
    return (value,)


def get_matrix_size(mat: List[Any]) -> Tuple[int, ...]:
    # NOTE: later we might just throw an error if the matrix is rigged.
    N = len(mat)

    if any(not isinstance(x, list) for x in mat):
        # ragged array, not matrix
        return (N,)

    element_sizes = set(map(len, mat))
    if len(element_sizes) != 1:
        # ragged array, not matrix
        return (N,)

    return (N,) + get_matrix_size(mat[0])
