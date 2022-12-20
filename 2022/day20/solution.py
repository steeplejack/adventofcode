class Node():
    def __init__(self, value, index):
        self.value = value
        self.next: Node | None = None
        self.prev: Node | None = None


class CircularList():
    def __init__(self):
        self.nodes = {}
        self.first: Node | None = None
        self.last: Node | None = None
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self, value):
        index = self.size
        node = Node(value, index)

        if index == 0:
            self.first = self.last = node
            node.next = node
            node.prev = node

        else:
            assert self.last.next is self.first and self.first.prev is self.last
            self.last.next = node
            node.prev = self.last
            self.last = node
            node.next = self.first
            self.first.prev = node

        self.nodes[index] = node
        self.size += 1

    def _swap_forward(self, i):
        node = self.nodes[i]
        self._swap_forward_node(node)

    def swap_forward(self, node_index, times=1):
        for _ in range(times % (self.size - 1)):
            self._swap_forward(node_index)

    def _swap_backward(self, i):
        node = self.nodes[i].prev
        self._swap_forward_node(node)

    def swap_backward(self, node_index, times=1):
        for _ in range(times % (self.size - 1)):
            self._swap_backward(node_index)

    def _swap_forward_node(self, node):
        assert self.size > 2
        nx = node.next
        pr = node.prev
        nx.prev = pr
        pr.next = nx

        nxnx = nx.next
        nx.next = node
        node.prev = nx
        nxnx.prev = node
        node.next = nxnx

        self.last = self.first.prev

    def to_list(self):
        values = [self.first.value]
        node = self.first
        while not node is self.last:
            node = node.next
            values.append(node.value)
        return values

    def find_zero(self):
        for node in self.nodes.values():
            if node.value == 0:
                return node

    def find_node_n_after(self, node, n):
        nd = node
        for _ in range(n % self.size):
            nd = nd.next
        return nd

# A bunch of tests
def test_forward_swaps(input_size, nswaps, i):
    assert input_size > 2
    assert nswaps > 0
    assert i >= 0 and i < input_size 
    vals = list(range(input_size))
    l1 = CircularList()
    l2 = CircularList()
    for val in vals:
        l1.insert(val)
        l2.insert(val)

    for _ in range(nswaps):
        l1.swap_forward(i)

    for _ in range(nswaps % (l2.size - 1)):
        l2.swap_forward(i)

    return l1.to_list() == l2.to_list()

def test_backward_swaps(input_size, nswaps, i):
    assert input_size > 2
    assert nswaps > 0
    assert i >= 0 and i < input_size 
    vals = list(range(input_size))
    l1 = CircularList()
    l2 = CircularList()
    for val in vals:
        l1.insert(val)
        l2.insert(val)

    for _ in range(nswaps):
        l1.swap_backward(i)

    for _ in range(nswaps % (l2.size - 1)):
        l2.swap_backward(i)

    return l1.to_list() == l2.to_list()

if __name__ == '__main__':

    l = CircularList()
    with open('input.txt') as fl:
        for line in fl:
            n = int(line)
            l.insert(n)

    print(f'List size = {l.size}')

    for i in sorted(l.nodes):
        if i > 0 and i % 1000 == 0: print(f'Moving node {i}')
        val = l.nodes[i].value
        if val > 0:
            l.swap_forward(i, times = abs(val))
        else:
            l.swap_backward(i, times = abs(val))

    z = l.find_zero()
    p = 0
    p += l.find_node_n_after(z, 1000).value
    p += l.find_node_n_after(z, 2000).value
    p += l.find_node_n_after(z, 3000).value
    print(f'Part 1: {p}')

    # Part 2
    decryption_key = 811589153
    l = CircularList()
    with open('input.txt') as fl:
        for line in fl:
            n = int(line) * decryption_key
            l.insert(n)

    print(f'List size = {l.size}')

    for mix in range(10):
        print(f'Mix {mix}...')
        for i in sorted(l.nodes):
            if i > 0 and i % 1000 == 0: print(f'  Moving node {i}')
            val = l.nodes[i].value
            if val > 0:
                l.swap_forward(i, times = abs(val))
            else:
                l.swap_backward(i, times = abs(val))

    z = l.find_zero()
    p = 0
    p += l.find_node_n_after(z, 1000).value
    p += l.find_node_n_after(z, 2000).value
    p += l.find_node_n_after(z, 3000).value
    print(f'Part 2: {p}')

        


