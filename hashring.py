from typing import Callable, Iterable

import _hashring.funcs as hashring_func

from _hashring.data import Node, HashValue, HashRingData, Resource


class HashRing:
    def __init__(self, num_nodes: int) -> None:
        self.hashring_data = HashRingData(num_nodes)
        self._initialized = False

    @property
    def _lookup_func(self) -> Callable:
        if self._initialized:
            return hashring_func.closest_node_finger
        return hashring_func.closest_node
    
    def lookup_node(self, hash_value: HashValue) -> Node | None:
        return hashring_func.lookup_node(self.hashring_data, hash_value, self._lookup_func)

    def move_resources(self, origin: Node, destination: Node, delete: bool) -> None:
        delete_list = hashring_func.resources_to_move(self.hashring_data, origin, destination, delete)
        for key in delete_list:
            print(f"\tMoving a resource {key} from {origin.hash_value} to {destination.hash_value}")
            hashring_func.move(key, origin, destination)
    
    def add_node(self, hash_value: HashValue) -> None:
        if hash_value not in self.hashring_data.legal_range:
            return None
        
        old_head = self.hashring_data.head
        new_node = Node(hash_value)
        hashring_func.add_node(self.hashring_data, new_node)

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
        hashring_func.move_resources(self.hashring_data, temp, temp.next, True)
        temp.previous.next = temp.next
        temp.next.previous = temp.previous

        head = self.hashring_data.head
        if head.hash_value == hash_value:
            head = temp.next if head != head.next else None
        
        self.build_finger_tables()

    def build_finger_tables(self) -> None:
        head = self.hashring_data.head
        if head is None:
            print("Cannot build finger tables for empty hash ring")
            return None
        
        hashring_func.make_finger_table(self.hashring_data, head)
        print(f"Finger table for {head.hash_value} is complete")

        curr = head.next
        while curr != head:
            hashring_func.make_finger_table(self.hashring_data, curr)
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
