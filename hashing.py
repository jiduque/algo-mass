from hashring_data import Node, HashValue, HashRingData, Resource
from hashring_func import *


class HashRing:
    def __init__(self, num_nodes: int) -> None:
        self.hashring_data = HashRingData(num_nodes)
    
    def lookup_node(self, hash_value: HashValue) -> Node | None:
        return lookup_node(self.hashring_data, hash_value)

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
             
    def add_resource(self, resource: Resource) -> None:
        if resource not in self.hashring_data.legal_range:
            return None

        target_node = lookup_node(self.hashring_data, resource)
        if target_node is None:
            print("Can't add a resource to an empty hashring.")
            return None
        
        print(f"Adding a resource {resource}")
        val = f"some stupid val for {resource}"
        target_node.resources[resource] = val

    def remove_node(self, hash_value: HashValue) -> None:
        temp = lookup_node(self.hashring_data, hash_value)
        if temp.hash_value != hash_value:
            print("Nothing to remove")
            return None
        
        print(f"Removing the node {hash_value}")
        move_resources(self.hashring_data, temp, temp.next, True)
        temp.previous.next = temp.next
        temp.next.previous = temp.previous

        head = self.hashring_data.head
        if head.hash_value == hash_value:
            head = temp.next if head != head.next else None

        return temp.next

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
                    

def main() -> None:
    num_nodes = 5
    hr = HashRing(num_nodes)
    
    nodes_to_add = [12, 18]
    add_all_nodes(hr, nodes_to_add)
    resources_to_add = [24, 21, 16, 23, 2, 29, 28, 7, 10]
    add_all_resources(hr, resources_to_add)
    hr.print()

    new_nodes = [5, 27, 30]
    add_all_nodes(hr, new_nodes)
    hr.print()

    hr.remove_node(12)
    hr.print()

    hr.build_finger_tables()


def add_all_nodes(hash_ring: HashRing, nodes: list[int]) -> None:
    for node in nodes:
        hash_ring.add_node(node)


def add_all_resources(hash_ring: HashRing, resources: list[Resource]) -> None:
    for resource in resources:
        hash_ring.add_resource(resource)


if __name__ == "__main__":
    main()
