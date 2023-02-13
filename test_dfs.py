from collections import deque

class Node:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.adjacency_list = []

def dfs(start_node, visitor_fn):
    stack = deque()

    stack.append(start_node)
    start_node.visited = True
    while stack:
        node = stack.pop()        
        visitor_fn(node)
        for neighboor in node.adjacency_list:
            if not neighboor.visited:
                stack.append(neighboor)
                neighboor.visited = True

def dfs_rec(node, visitor_fn):
    if not node.visited:
        visitor_fn(node)
        node.visited = True

    for neighboor in node.adjacency_list:
        if not neighboor.visited:
            dfs_rec(neighboor, visitor_fn)


def test_recursive_traversal():
    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    E = Node('E')
    F = Node('F')

    A.adjacency_list = [B, C]
    B.adjacency_list = [D]
    C.adjacency_list = [B, D, F]
    D.adjacency_list = [E]
    F.adjacency_list = [E]

    visited_nodes = []
    dfs_rec(A, lambda node: visited_nodes.append(node.name))

    assert visited_nodes == ['A', 'B', 'D', 'E', 'C', 'F']

    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    E = Node('E')
    F = Node('F')

    A.adjacency_list = [B, C]
    B.adjacency_list = [D]
    C.adjacency_list = [B, D, F]
    D.adjacency_list = [E]
    F.adjacency_list = [E]

    visited_nodes = []
    dfs(A, lambda node: visited_nodes.append(node.name))

    assert visited_nodes == ['A', 'C', 'F', 'E', 'D', 'B']