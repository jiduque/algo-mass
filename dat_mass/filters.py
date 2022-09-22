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


# TODO: Implement look at https://people.engr.tamu.edu/ajiang/bloom.pdf
class WeightedBloomFilter(BloomFilter):
    def __init__(self, n: int, f: float) -> None:
        super().__init__(n, f)
        raise NotImplementedError


# TODO: Implement look at https://core.ac.uk/download/pdf/4891089.pdf
class AdaptiveBloomFilter(BloomFilter):
    def __init__(self, n: int, f: float) -> None:
        super().__init__(n, f)
        raise NotImplementedError


class Slot:
    remainder: int = 0
    bucket_occupied: bool = False
    run_continued: bool = False
    is_shifted: bool = False


class QuotientFilterData(list):
    def __init__(self, q: int) -> None:
        super().__init__(Slot() for _ in range(2 ** q))


def start_of_cluster(slots: QuotientFilterData, quotient: int) -> int:
    output = quotient
    while slots[output].is_shifted:
        output -= 1
    return output


def possible_location(slots: QuotientFilterData, cluster_start: int, quotient: int) -> int:
    output, b = cluster_start, cluster_start
    while b != quotient:
        output += 1
        while slots[output].run_continued:
            output += 1
        b += 1
        while not slots[b].bucket_occupied:
            b += 1
    return output


def is_it_here(slots: QuotientFilterData, init: int, remainder: int) -> bool:
    s = init
    while slots[s].remainder != remainder:
        s += 1
        if not slots[s].run_continued:
            return False
    return True


class QuotientFilter:
    def __init__(self, q: int, r: int) -> None:
        self.q = q
        self.r = r
        self.filter = QuotientFilterData(q)

    @property
    def size(self) -> int:
        return len(self.filter)

    def __getitem__(self, item: int):
        return self.filter[item]

    def __contains__(self, item: int) -> bool:
        return self.lookup(item)

    def lookup(self, fingerprint: int) -> bool:
        quotient, remainder = divmod(fingerprint, 2 ** self.r)
        bucket_empty = not self[quotient].bucket_occupied
        if bucket_empty:
            return False

        starting_line = start_of_cluster(self.filter, quotient)
        start_of_possible_location = possible_location(self.filter, starting_line, quotient)
        output = is_it_here(self.filter, start_of_possible_location, remainder)
        return output


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
