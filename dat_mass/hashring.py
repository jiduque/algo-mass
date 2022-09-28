from typing import Callable, Iterable


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


class HashRing:
    def __init__(self, num_nodes: int) -> None:
        self.hashring_data = HashRingData(num_nodes)
        self._initialized = False

    @property
    def _lookup_func(self) -> Callable:
        if self._initialized:
            return closest_node_finger
        return closest_node
    
    def lookup_node(self, hash_value: HashValue) -> Node | None:
        return lookup_node(self.hashring_data, hash_value, self._lookup_func)

    def move_resources(self, origin: Node, destination: Node, delete: bool) -> None:
        delete_list = resources_to_move(self.hashring_data, origin, destination, delete)
        for key in delete_list:
            print(f"\tMoving a resource {key} from {origin.hash_value} to {destination.hash_value}")
            move(key, origin, destination)
    
    def add_node(self, hash_value: HashValue) -> None:
        if hash_value not in self.hashring_data.legal_range:
            return None
        
        old_head = self.hashring_data.head
        new_node = Node(hash_value)
        add_node(self.hashring_data, new_node)

        new_head = self.hashring_data.head
        msg = f"Adding a head node {new_head.hash_value} ..."

        if old_head is not None:
            msg = f"Adding a node {new_node.hash_value}. Previous node is {new_node.previous.hash_value}. "
            msg += f"Next node is {new_node.next.hash_value}."
            
        print(msg)
        self.build_finger_tables()
             
    def add_resource(self, resource: Resource) -> None:
        if resource not in self.hashring_data.legal_range:
            return None

        target_node = self.lookup_node(resource)
        if target_node is None:
            print("Can't add a resource to an empty hashring.")
            return None
        
        print(f"Adding a resource {resource}")
        val = f"some stupid val for {resource}"
        target_node.resources[resource] = val

    def remove_node(self, hash_value: HashValue) -> None:
        temp = self.lookup_node(hash_value)
        if temp.hash_value != hash_value:
            print("Nothing to remove")
            return None
        
        print(f"Removing the node {hash_value}")
        move_resources(self.hashring_data, temp, temp.next, True)
        temp.previous.next = temp.next
        temp.next.previous = temp.previous

        head = self.hashring_data.head
        if head.hash_value == hash_value:
            self.hashring_data.head = temp.next if head != head.next else None
        
        self.build_finger_tables()

    def build_finger_tables(self) -> None:
        head = self.hashring_data.head
        if head is None:
            print("Cannot build finger tables for empty hash ring")
            return None
        
        make_finger_table(self.hashring_data, head)
        print(f"Finger table for {head.hash_value} is complete")

        curr = head.next
        while curr != head:
            make_finger_table(self.hashring_data, curr)
            print(f"Finger table for {curr.hash_value} is complete")
            curr = curr.next

        self._initialized = True

    def print(self) -> None:
        print("*****")
        print("Printing the hashring in clockwise order:")

        head = self.hashring_data.head
        
        if head is None:
            print("Empty hashring")
            return None
        
        temp = head
        while True:
            print(f"Node: {temp.hash_value}, ", end=" ")
            print("Resources: ", end=" ")
            if not bool(temp.resources):
                print("Empty", end="")
            else:
                for i in temp.resources.keys():
                    print(f"{i}", end=" ")
                temp = temp.next
                print(" ")
                if temp == head:
                    break
                    
        print("*****")

    def add_resources(self, resources: Iterable[Resource]) -> None:
        for resource in resources:
            self.add_resource(resource)

    def add_nodes(self, nodes: Iterable[HashValue]) -> None:
        for node in nodes:
            self.add_node(node)


def distance(k: int, a: HashValue, b: HashValue) -> int:
    output = b - a
    if a > b:
        output += 2 ** k
    return output


def closest_node(hash_ring: HashRingData, hash_value: HashValue) -> Node:
    curr_node, next_node = hash_ring.head, hash_ring.head.next

    def dist(x: Node) -> int:
        return distance(hash_ring.num_nodes, x.hash_value, hash_value)

    while dist(curr_node) > dist(next_node):
        curr_node = next_node
        next_node = next_node.next

    if curr_node.hash_value == hash_value:
        return curr_node

    return next_node


def _potential_successor(finger_table: FingerTable, hash_value: HashValue) -> Node:
    min_key = min(
        finger_table.keys(),
        key=lambda finger: abs(hash_value - finger)
    )
    return finger_table[min_key]


def closest_node_finger(hash_ring: HashRingData, hash_value: HashValue) -> Node:
    curr_node = hash_ring.head
    next_node = _potential_successor(curr_node.finger_table, hash_value)

    def dist(x: Node) -> int:
        return distance(hash_ring.num_nodes, x.hash_value, hash_value)

    while dist(curr_node) > dist(next_node):
        curr_node = next_node
        next_node = _potential_successor(curr_node.finger_table, hash_value)

    if curr_node.hash_value == hash_value:
        return curr_node

    return next_node


def lookup_node(hash_ring: HashRingData, hash_value: HashValue, search_func: Callable = closest_node) -> Node | None:
    not_in_range = hash_value not in hash_ring.legal_range
    empty = hash_ring.head is None
    if not_in_range or empty:
        return None
    return search_func(hash_ring, hash_value)


def resources_to_move(hash_ring: HashRingData, origin: Node, destination: Node, delete: bool) -> set[int]:
    k = hash_ring.num_nodes
    delete_list = set(origin.resources.keys())

    if not delete:
        def dist_greater(x: HashValue) -> bool:
            return distance(k, x, destination.hash_value) >= distance(k, x, origin.hash_value)

        delete_list -= set(filter(dist_greater, origin.resources.keys()))

    return delete_list


def move(key: HashValue, origin: Node, destination: Node) -> None:
    destination.resources[key] = origin.resources[key]
    del origin.resources[key]


def move_resources(hash_ring: HashRingData, origin: Node, destination: Node, delete: bool) -> None:
    delete_list = resources_to_move(hash_ring, origin, destination, delete)
    for key in delete_list:
        move(key, origin, destination)


def _add_node_empty(hash_ring: HashRingData, new_node: Node) -> None:
    new_node.next = new_node
    new_node.previous = new_node
    hash_ring.head = new_node


def _add_node_not_empty(hash_ring: HashRingData, new_node: Node) -> None:
    temp = lookup_node(hash_ring, new_node.hash_value)

    new_node.next = temp
    new_node.previous = temp.previous
    new_node.previous.next = new_node
    new_node.next.previous = new_node

    move_resources(hash_ring, new_node.next, new_node, False)
    if new_node.hash_value < hash_ring.head.hash_value:
        hash_ring.head = new_node


def add_node(hash_ring: HashRingData, new_node: Node) -> None:
    if hash_ring.head is None:
        _add_node_empty(hash_ring, new_node)
    else:
        _add_node_not_empty(hash_ring, new_node)


def add_resource(hash_ring: HashRingData, resource: Resource) -> None:
    if resource not in hash_ring.legal_range:
        return None

    target_node = lookup_node(hash_ring, resource)
    if target_node is None:
        return None

    val = f"some stupid val for {resource}"
    target_node.resources[resource] = val


def remove_node(hash_ring: HashRingData, hash_value: HashValue) -> None:
    temp = lookup_node(hash_ring, hash_value)
    if temp.hash_value != hash_value:
        return None

    move_resources(hash_ring, temp, temp.next, True)
    temp.previous.next = temp.next
    temp.next.previous = temp.previous

    head = hash_ring.head
    if head.hash_value == hash_value:
        hash_ring.head = temp.next if head != head.next else None


def make_finger_table(hash_ring: HashRingData, node: Node) -> None:
    k = hash_ring.num_nodes
    values = map(lambda i: 2 ** i, range(k))
    for f_i in values:
        x = node.hash_value + f_i
        successor = lookup_node(hash_ring, x, closest_node)
        node.finger_table[x] = successor


def initialize_finger_tables(hash_ring: HashRingData) -> None:
    head = hash_ring.head
    if head is None:
        return None

    make_finger_table(hash_ring, head)
    curr = head.next
    while curr != head:
        make_finger_table(hash_ring, curr)
        curr = curr.next
