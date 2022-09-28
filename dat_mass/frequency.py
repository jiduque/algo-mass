from typing import Any, Hashable
from math import log, e, ceil

from mmh3 import hash

IntMatrix = list[list[int]]


class CountMinData(IntMatrix):
    def __init__(self, n: int, m: int) -> None:
        self.rows = n
        self.columns = m
        super().__init__([[0 for _ in range(m)] for _ in range(n)])


class CountMinSketch:
    def __init__(self, epsilon: float, delta: float) -> None:
        self.epsilon = epsilon
        self.delta = delta
        w = int(ceil(e / epsilon))
        d = int(ceil(-log(delta)))
        self.sketch = CountMinData(w, d)

    @property
    def w(self) -> int:
        return self.sketch.rows

    @property
    def d(self) -> int:
        return self.sketch.columns

    def update(self, item: Hashable, freq=1) -> None:
        update(self.sketch, item, freq)

    def estimate(self, item: Hashable) -> int:
        return estimate(self.sketch, item)


def boyer_more(values: list[Any]) -> Any:
    output, count = values[0], 1
    for val in values:
        inc = 1 if val == output else -1
        count += inc
        if count == 0:
            output = val
            count = 1
    return output


def update(count_min: CountMinData, item: Hashable, freq: int = 1) -> None:
    n, m = count_min.rows, count_min.columns
    for i in range(m):
        index = hash(item, i) % n
        count_min[i][index] += freq


def estimate(count_min: CountMinData, item: Hashable) -> int:
    rows, columns = count_min.rows, count_min.columns
    values = map(lambda i: count_min[i][hash(item, i) % columns], range(rows))
    return min(values)
