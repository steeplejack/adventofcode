class Node():
    """
    A node (file or dir) in the modelled filesystem
    """
    def __init__(self, name, type, size):
        self.children = []
        self.parent = None
        self.name = name
        self.size = size
        self.type = type

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} type={self.type} children={self.children} size={self.size}"

    def add_child_node(self, child_node):
        if self.type == "f":
            raise ValueError("Shouldn't be trying to add children to a file node")
        child_node.parent = self
        assert child_node.parent is not None
        self.children.append(child_node)

    def dirs_iter(self):
        yield self
        for child in self.children:
            if child.type == "d":
                for dir in child.dirs_iter():
                    yield dir


def recurse_size_calc(node):
    size = 0
    for child in node.children:
        size += recurse_size_calc(child)
    size += node.size
    node.tree_size = size
    return size

def find_child_with_name(name, node):
    for child in node.children:
        if child.name == name:
            return child

if __name__ == '__main__':
    with open("input.txt") as fl:
        inputs = [line.strip() for line in fl]

    root_node = None
    current_dirnode = Node("", "", 0)

    for line_num, i in enumerate(inputs, start=1):
        tokens = i.split()
        if tokens[0] == "$":
            # Command
            if tokens[1] == "cd":
                if tokens[2] == "/":
                    # Root of file system
                    if not root_node:
                        current_dirnode = root_node = Node(name = "/", type = "d", size = 0)
                    current_dirnode = root_node
                elif tokens[2] == "..":
                    # Traverse to the parent of the current directory
                    if current_dirnode:
                        if current_dirnode.parent is None:
                            raise ValueError("Current node has no parent")
                        current_dirnode = current_dirnode.parent
                    else:
                        raise ValueError("No current directory")
                else:
                    dirname = tokens[2]
                    child_node = find_child_with_name(dirname, current_dirnode)
                    if not child_node:
                        raise ValueError(f"Requested directory {dirname} is not a child of current: line{line_num}: {i}")
                    current_dirnode = child_node
        elif tokens[0] == "dir":
            # This is a directory as a child of current
            dirname = tokens[1]
            child_node = find_child_with_name(dirname, current_dirnode)
            if not child_node:
                child_node = Node(name = dirname, type = "d", size = 0)
                current_dirnode.add_child_node(child_node)
        else:
            # This is a file as a child of current
            filename = tokens[1]
            filesize = int(tokens[0])
            child_node = find_child_with_name(filename, current_dirnode)
            if not child_node:
                child_node = Node(name = filename, type = "f", size = filesize)
                current_dirnode.add_child_node(child_node)

    recurse_size_calc(root_node)
    part_one_totals = sum(node.tree_size
                          for node in root_node.dirs_iter()
                          if node.tree_size <= 100000)

    print(f'Part 1: {part_one_totals}')

    dirs = list(root_node.dirs_iter())
    dirs.sort(key = lambda x: x.tree_size)
    required = root_node.tree_size - (70000000 - 30000000)
    for dir in dirs:
        if dir.tree_size > required:
            break
    print(f'Part 2: {dir.tree_size} ({dir.name})')
