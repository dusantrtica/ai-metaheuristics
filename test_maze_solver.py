class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        n = len(maze)
        self.solution = [['-' for _ in range(n)] for _ in range(n)]
        self.n = n

    def find_solution(self):
        if self.solve(0, 0):
            self._print_solution()
        else:
            return None

    def solve(self, row, col):
        if self._is_finished(row, col):
            self.solution[row][col] = 'S'
            return True

        if self._is_valid(row, col):
            self.solution[row][col] = 'S'
            if self.solve(row, col + 1):
                return True

            if self.solve(row+1, col):
                return True

            self.solution[row][col] = '-'

        return False

    def _is_valid(self, row, col):
        if row < 0 or row >= self.n:
            return False
        if col < 0 or col >= self.n:
            return False

        return self.maze[row][col] == 1

    def _is_finished(self, row, col):
        return self.n-1 == row and self.n-1 == col

    def _print_solution(self):
        for row in self.solution:
            print(row)


def test_solution_exists():
    maze_input = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ]

    solver = MazeSolver(maze_input)

    solver.find_solution()

def test_solution_exists1():
    maze_input = [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ]

    solver = MazeSolver(maze_input)

    solver.find_solution()

if __name__ == '__main__':
    #test_solution_exists()
    test_solution_exists1()
