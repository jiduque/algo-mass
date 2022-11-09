from abc import ABC
from typing import Hashable

from mmh3 import hash, hash64, hash128


class Counter(ABC):
    def update(self) -> None:
        pass

    def estimate(self) -> int:
        pass


class ProbCounter:
    def __init__(self, n: int = 32) -> None:
        funcs = {32: hash, 64: hash64, 128: hash128}
        assert n in [32, 64, 128]

        self.n = n
        self.x = 0
        self._hash = funcs[n]

    def estimate(self) -> int:
        return 2 ** self.x

    def update(self, item: Hashable):
        h = self._hash(item, seed=0)
        rho = first_bit(str(h))
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


def main() -> None:
    pc = ProbCounter()
    pc.update("1")


if __name__ == '__main__':
    main()
