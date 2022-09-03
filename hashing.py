from typing import List, Optional


HashValue = int
Resource = int


class Node:
    def __init__(self, hash_value: HashValue) -> None:
        self.hash_value = hash_value
        self.resources = {}
        self.next = None
        self.previous = None


class HashRing:
    def __init__(self, num_nodes: int) -> None:
        self.head = None
        self.num_nodes = num_nodes
        self.min = 0
        self.max = 2 ** num_nodes - 1

    @property
    def legal_range(self):
        return range(self.min, self.max + 1)

    def distance(self, a: HashValue, b: HashValue) -> int:
        output = b - a
        if a > b:
            output += 2 ** self.num_nodes 
        return output
    
    def lookup_node(self, hash_value: HashValue) -> Optional[Node]:
        not_in_range = hash_value not in self.legal_range
        head_is_none = self.head is None
        if not_in_range or head_is_none:
            return None
        
        return self._closest_node(hash_value)

    def move_resources(self, origin: HashValue, destination: HashValue, delete: bool) -> None:
        delete_list = set(origin.resources.keys())
        
        if not delete:
            dist = lambda x: self.distance(x, destination.hash_value) >= self.distance(x, origin.hash_value)
            delete_list -= set(filter(dist, origin.resources.keys()))
        
        for key in delete_list:
            print(f"\tMoving a resource {key} from {origin.hash_value} to {destination.hash_value}")
            destination.resources[key] = origin.resources[key]
            del origin.resources[key]
    
    def add_node(self, hash_value: HashValue) -> None:
        if hash_value not in self.legal_range:
            return None
        
        if self.head is None:
            new_node = Node(hash_value)
            new_node.next = new_node
            new_node.previous = new_node
            self.head = new_node
            print(f"Adding a head node {new_node.hash_value} ...")
        else:
            self._add_new_node_not_empty(hash_value)
             
    def add_resource(self, resource: Resource) -> None:
        if resource not in self.legal_range:
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
        self.move_resources(temp, temp.next, True)
        temp.previous.next = temp.next
        temp.next.previous = temp.previous

        if self.head.hash_value == hash_value:
            self.head = temp.next if self.head != self.head.next else None

        return temp.next

    def print(self) -> None:
        print("*****")
        print("Printing the hashring in clockwise order:")

        if self.head is None:
            print("Empty hashring")
            return None
        
        temp = self.head
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
                if temp == self.head:
                    break
                    
        print("*****")


    def _add_new_node_not_empty(self, hash_value: HashValue) -> None:
        new_node = Node(hash_value)
        temp = self.lookup_node(hash_value)
        
        new_node.next = temp
        new_node.previous = temp.previous
        new_node.previous.next = new_node
        new_node.next.previous = new_node

        msg = f"Adding a node {new_node.hash_value}. Previous node is {new_node.previous.hash_value}. "
        msg += f"Next node is {new_node.next.hash_value}."
        print(msg)

        self.move_resources(new_node.next, new_node, False)
        if hash_value < self.head.hash_value:
            self.head = new_node
    
    def _closest_node(self, hash_value: HashValue) -> Node:
        curr_node, next_node = self.head, self.head.next
        
        dist = lambda x: self.distance(x.hash_value, hash_value)
        while dist(curr_node) > dist(next_node):
            curr_node = next_node
            next_node = next_node.next
            
        if curr_node.hash_value == hash_value:
            return curr_node
        
        return next_node

                    

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


def add_all_nodes(hash_ring: HashRing, nodes: List[int]) -> None:
    for node in nodes:
        hash_ring.add_node(node)


def add_all_resources(hash_ring: HashRing, resources: List[Resource]) -> None:
    for resource in resources:
        hash_ring.add_resource(resource)


if __name__ == "__main__":
    main()

