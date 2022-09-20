from typing import Hashable
from math import log

from mmh3 import hash
from bitarray import bitarray


def calculate_m(n: int, f: float) -> int:
    numerator = -log(f) * n
    denominator = log(2) * log(2)
    return int(numerator / denominator)


def calculate_k(n: int, m: float) -> int:
    numerator = m * log(2)
    denominator = n
    return int(numerator / denominator)


class BloomFilter:
    def __init__(self, n: int, f: float) -> None:
        self.n = n
        self.f = f
        self.m = calculate_m(n, f)
        self.k = calculate_k(n, self.m)

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)

    def __str__(self) -> str:
        return f"n = {self.n}, f = {self.f}, m = {self.m}, k = {self.k}"

    def __contains__(self, item: Hashable) -> bool:
        return self.lookup(item)

    def insert(self, item: Hashable) -> None:
        for i in range(self.k):
            index = hash(item, i) % self.m
            self.bit_array[index] = 1

    def lookup(self, item: Hashable) -> bool:
        indexes = map(lambda i: hash(item, i) % self.m, range(self.k))
        set_1 = map(lambda i: self.bit_array[i] == 1, indexes)
        return all(set_1)


def main() -> None:
    bf = BloomFilter(10, 0.01)
    vals_to_insert = ["1", "2", "42", "89", "7"]
    for val in vals_to_insert:
        bf.insert(val)

    vals_to_lookup = ["1", "2", "3", "42", "43", "89"]
    for val in vals_to_lookup:
        print(f"{val} {val in bf}")


if __name__ == '__main__':
    main()
