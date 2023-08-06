from typing import Any, List


def pops(array: List, count: int) -> List[Any]:
    return [array.pop() for _ in count]

def reverse_array(array: List):
    reversed_array: List[Any] = []
    for item in reversed(array):
        reversed_array.append(item)
    return reversed_array
