from queue import Queue


class Node:
    def __init__(self, name):
        self.name = name
        self.adjacency_list = []
        self.visited = False


def breath_first_search(start, visit):
    queue = Queue()
    queue.put(start)
    start.visited = True

    while not queue.empty():
        node = queue.get()
        visit(node)

        for neighbor in node.adjacency_list:
            if not neighbor.visited:
                queue.put(neighbor)
                neighbor.visited = True


if __name__ == '__main__':
    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    E = Node('E')
    F = Node('F')

    A.adjacency_list = [B, C]
    C.adjacency_list = [D, E]
    B.adjacency_list = [F]

    breath_first_search(A, lambda node: print(node.name))

