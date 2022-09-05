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
        msg = print(f"Adding a head node {new_head.hash_value} ...")

        if old_head is not None:
            msg = f"Adding a node {new_node.hash_value}. Previous node is {new_node.previous.hash_value}. "
            msg += f"Next node is {new_node.next.hash_value}."
            
        print(msg)
             
    def add_resource(self, resource: Resource) -> None:
        add_resource(self.hashring_data, resource)

    def remove_node(self, hash_value: HashValue) -> None:
        remove_node(self.hashring_data, hash_value)

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


def add_all_nodes(hash_ring: HashRing, nodes: list[int]) -> None:
    for node in nodes:
        hash_ring.add_node(node)


def add_all_resources(hash_ring: HashRing, resources: list[Resource]) -> None:
    for resource in resources:
        hash_ring.add_resource(resource)


if __name__ == "__main__":
    main()
