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

    def swap_forward(self, i):
        node = self.nodes[i]
        self._swap_forward_node(node)

    def swap_backward(self, i):
        node = self.nodes[i].prev
        self._swap_forward_node(node)

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
        for _ in range(n):
            nd = nd.next
        return nd

if __name__ == '__main__':

    l = CircularList()
    with open('input.txt') as fl:
        for line in fl:
            n = int(line)
            l.insert(n)

    print(f'List size = {l.size}')

    for i in sorted(l.nodes):
        if i > 0 and i % 1000 == 0: print(f'Moving node {i}')
        for _ in range(abs(l.nodes[i].value)):
            if l.nodes[i].value > 0:
                l.swap_forward(i)
            else:
                l.swap_backward(i)

    z = l.find_zero()
    p = 0
    p += l.find_node_n_after(z, 1000).value
    p += l.find_node_n_after(z, 2000).value
    p += l.find_node_n_after(z, 3000).value
    print(f'Part 1: {p}')

        


