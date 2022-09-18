from typing import Callable
from _hashring.data import Node, HashValue, HashRingData, Resource, FingerTable


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


def make_finger_table(hash_ring: HashRingData, node: Node, search_func: Callable = closest_node) -> None:
    k = hash_ring.num_nodes
    values = map(lambda i: 2 ** i, range(k))
    for f_i in values:
        x = node.hash_value + f_i
        succesor = lookup_node(hash_ring, x, search_func)
        node.finger_table[x] = succesor


def initialize_finger_tables(hash_ring: HashRingData) -> None:
    head = hash_ring.head
    if head is None:
        return None

    make_finger_table(hash_ring, head)
    curr = head.next
    while curr != head:
        make_finger_table(hash_ring, curr)
        curr = curr.next
