HashValue = int
Resource = int


class Node:
    def __init__(self, hash_value: HashValue) -> None:
        self.hash_value = hash_value
        self.resources = {}
        self.next = None
        self.previous = None


class HashRingData:
    def __init__(self, num_nodes: int) -> None:
        self.head = None
        self.num_nodes = num_nodes
        self.min = 0
        self.max = 2 ** num_nodes - 1
    
    @property
    def legal_range(self):
        return range(self.min, self.max + 1)


def distance(k: int, a: HashValue, b: HashValue) -> int:
    output = b - a
    if a > b:
        output += 2 ** k
    return output


def closest_node(hash_ring: HashRingData, hash_value: HashValue) -> Node:
    curr_node, next_node = hash_ring.head, hash_ring.head.next

    dist = lambda x: distance(hash_ring.num_nodes, x.hash_value, hash_value) 
    while dist(curr_node) > dist(next_node):
        curr_node = next_node
        next_node = next_node.next
    
    if curr_node.hash_value == hash_value:
        return curr_node
    
    return next_node


def lookup_node(hash_ring: HashRingData, hash_value: HashValue) -> Node | None:
    not_in_range = hash_value not in hash_ring.legal_range
    empty = hash_ring.head is None    
    if not_in_range or empty:
        return None
    return closest_node(hash_ring, hash_value)


def move_resources(hash_ring: HashRingData, origin: HashValue, destination: HashValue, delete: bool) -> None:
    k = hash_ring.num_nodes
    delete_list = set(origin.resources.keys())
        
    if not delete:
        dist = lambda x: distance(k, x, destination.hash_value) >= distance(k, x, origin.hash_value)
        delete_list -= set(filter(dist, origin.resources.keys()))
    
    for key in delete_list:
        print(f"\tMoving a resource {key} from {origin.hash_value} to {destination.hash_value}")
        destination.resources[key] = origin.resources[key]
        del origin.resources[key]


def add_node_empty(hash_ring: HashRingData, hash_value: HashValue) -> None:
    new_node = Node(hash_value)
    new_node.next = new_node
    new_node.previous = new_node
    hash_ring.head = new_node


def add_node(hash_ring: HashRingData, hash_value: HashValue) -> None:
    new_node = Node(hash_value)
    temp = lookup_node(hash_ring, hash_value)
    
    new_node.next = temp
    new_node.previous = temp.previous
    new_node.previous.next = new_node
    new_node.next.previous = new_node

    msg = f"Adding a node {new_node.hash_value}. Previous node is {new_node.previous.hash_value}. "
    msg += f"Next node is {new_node.next.hash_value}."
    print(msg)

    move_resources(hash_ring, new_node.next, new_node, False)
    if hash_value < hash_ring.head.hash_value:
        hash_ring.head = new_node

def add_resource(hash_ring: HashRingData, resource: Resource) -> None:
    if resource not in hash_ring.legal_range:
        return None

    target_node = lookup_node(hash_ring, resource)
    if target_node is None:
        print("Can't add a resource to an empty hashring.")
        return None
    
    print(f"Adding a resource {resource}")
    val = f"some stupid val for {resource}"
    target_node.resources[resource] = val

def remove_node(hash_ring: HashRingData, hash_value: HashValue) -> None:
    temp = lookup_node(hash_ring, hash_value)
    if temp.hash_value != hash_value:
        print("Nothing to remove")
        return None
    
    print(f"Removing the node {hash_value}")
    move_resources(hash_ring, temp, temp.next, True)
    temp.previous.next = temp.next
    temp.next.previous = temp.previous

    if hash_ring.head.hash_value == hash_value:
        hash_ring.head = temp.next if hash_ring.head != hash_ring.head.next else None

    return temp.next
    


class HashRing:
    def __init__(self, num_nodes: int) -> None:
        self.hashring_data = HashRingData(num_nodes)

    def distance(self, a: HashValue, b: HashValue) -> int:
        k = self.hashring_data.num_nodes
        return distance(k, a, b)
    
    def lookup_node(self, hash_value: HashValue) -> Node | None:
        return lookup_node(self.hashring_data, hash_value)

    def move_resources(self, origin: HashValue, destination: HashValue, delete: bool) -> None:
        move_resources(self.hashring_data, origin, destination, delete)
    
    def add_node(self, hash_value: HashValue) -> None:
        if hash_value not in self.hashring_data.legal_range:
            return None
        
        head = self.hashring_data.head
        if head is None:
            add_node_empty(self.hashring_data, hash_value)
            new_head = self.hashring_data.head
            print(f"Adding a head node {new_head.hash_value} ...")
        else:
            add_node(self.hashring_data, hash_value)
             
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
