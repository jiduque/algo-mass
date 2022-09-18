HashValue = int
Resource = int


class Node:
    def __init__(self, hash_value: HashValue) -> None:
        self.hash_value = hash_value
        self.resources = {}
        self.next = None
        self.previous = None
        self.finger_table = FingerTable()


FingerTable = dict[HashValue, Node]


class HashRingData:
    def __init__(self, num_nodes: int) -> None:
        self.head = None
        self.num_nodes = num_nodes
        self.min = 0
        self.max = 2 ** num_nodes - 1
    
    @property
    def legal_range(self):
        return range(self.min, self.max + 1)