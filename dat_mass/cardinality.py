from abc import ABC
from typing import Hashable
from random import random


class Counter(ABC):
    def update(self) -> None:
        pass

    def estimate(self) -> int:
        pass


class ProbCounter:
    def __init__(self, n: int) -> None:
        self.n = n
        self.x = 0

    def estimate(self) -> int:
        return 2 ** self.x

    # TODO: use better hashing method
    def update(self, item: Hashable):
        hash_int = hash(item)
        h = format(hash_int, "b")
        rho = first_bit(h)
        self.x = max(self.x, rho)


class LogLog:
    def __init__(self, n: int, buckets: int) -> None:
        self.n = n
        self.x = 0


def first_bit(bit_string: str) -> int:
    n = len(bit_string)
    output = n - 1

    while output > 0 and bit_string[output] != "1":
        output -= 1

    return output + 1
