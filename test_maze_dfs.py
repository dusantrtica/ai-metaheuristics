from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        n = len(maze)
        self.n = n
        self.solution = [['-' for _ in range(n)] for _ in range(n)]
        self.visited = set()

    def find_and_print_solution(self):
        if self._solve():
            self._print_solution()

    def _print_solution(self):
        for row in self.solution:
            print(row)

    def _solve(self):
        self.visited.add((0, 0))
        stack = deque()
        stack.append((0, 0))

        while stack:
            current_pos = stack.pop()
            self.visited.add(current_pos)
            self.solution[current_pos[0]][current_pos[1]] = 'S'

            if self._is_finished(current_pos):
                return True
            for move in self._next_moves(current_pos):
                stack.append(move)
        return False

    def _next_moves(self, current_position):
        (i, j) = current_position
        possible_moves = [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]
        for possible_move in possible_moves:
            (a, b) = possible_move
            if 0 <= a < self.n and 0 <= b < self.n and (a, b) not in self.visited and self.maze[a][b] == 1:
                yield (a, b)

    def _is_finished(self, position):
        (i, j) = position
        return i == self.n - 1 and j == self.n - 1



def test_solve_maze():
    input = [
        [1, 1, 1, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ]

    solver = MazeSolver(input)

    solver.find_and_print_solution()

if __name__ == '__main__':
    test_solve_maze()