from random import random, sample
from random import shuffle
from copy import deepcopy
import numpy as np
from numpy.random import randint
import matplotlib.pyplot as plt

TABLE_SIZE = 9
BOX_SIZE = 3


def accept_prob(actual_energy, next_energy, temp):
    if next_energy < actual_energy:
        return 1

    # we accept "bad" moves with a given probability
    return np.exp((actual_energy - next_energy) / temp)


class SingleSolution:
    def __init__(self, table):
        self.table = deepcopy(table)
        self.original_table = deepcopy(table)

    def mutate(self):
        # Choose randomly 3x3 box
        row_offset = (randint(0, TABLE_SIZE - 1) // BOX_SIZE) * BOX_SIZE
        col_offset = (randint(0, TABLE_SIZE - 1) // BOX_SIZE) * BOX_SIZE

        indexes = []
        for i in range(BOX_SIZE):
            for j in range(BOX_SIZE):
                if self.original_table[row_offset + i][col_offset + j] == 0:
                    indexes.append([row_offset + i, col_offset + j])

        pair1, pair2 = sample(indexes, 2)
        self.table[pair1[0]][pair1[1]], self.table[pair2[0]][pair2[1]] = self.table[pair2[0]][pair2[1]], \
                                                                         self.table[pair1[0]][pair1[1]]

    def fitness(self):
        penalty = 0
        # check all the rows
        for row in range(TABLE_SIZE):
            penalty += (len(self.table[row])) - len(set(self.table[row]))

        transposed_table = list(zip(*self.table))
        for row in range(TABLE_SIZE):
            penalty += (len(transposed_table[row])) - len(set(transposed_table[row]))

        return penalty

    # we have to generate random integers for empty cells
    def generate_solution(self):
        for row_index in range(0, TABLE_SIZE, 3):
            for col_index in range(0, TABLE_SIZE, 3):
                row_offset = (row_index // 3) * BOX_SIZE
                col_offset = (col_index // 3) * BOX_SIZE

                nums = [n for n in range(1, 10)]

                # there are some constants already present in the actual box
                # we have to get rid of those values from the nums
                for i in range(BOX_SIZE):
                    for j in range(BOX_SIZE):
                        if self.table[row_offset + i][col_offset + j] != 0:
                            nums.remove(self.table[row_offset + i][col_offset + j])

                # insert the values into the empty cells
                for i in range(BOX_SIZE):
                    for j in range(BOX_SIZE):
                        if self.table[row_offset + i][col_offset + j] == 0:
                            self.table[row_offset + i][col_offset + j] = nums.pop()

        print(self.table)


class SimulatedAnnealing:
    def __init__(self, table, min_temp, max_temp, cooling_rate=0.999):
        self.table = table
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.cooling_rate = cooling_rate
        self.actual_state = SingleSolution(table)
        self.best_state = self.actual_state
        self.next_state = None

    def generate_next_state(self, state):
        new_state = SingleSolution(state.table)
        new_state.mutate()
        return new_state

    def run(self):
        self.actual_state.generate_solution()
        temp = self.max_temp
        counter = 0
        while temp > self.min_temp:
            if self.best_state.fitness() == 0:
                break

            new_state = self.generate_next_state(self.actual_state)
            actual_energy = self.actual_state.fitness()
            new_energy = new_state.fitness()

            if random() < accept_prob(actual_energy, new_energy, temp):
                self.actual_state = new_state

            if self.actual_state.fitness() < self.best_state.fitness():
                self.best_state = self.actual_state

            temp = temp * self.cooling_rate


if __name__ == '__main__':
    sudoku_table = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                    [5, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 7, 0, 0, 0, 0, 3, 1],
                    [0, 0, 3, 0, 1, 0, 0, 8, 0],
                    [9, 0, 0, 8, 6, 3, 0, 0, 5],
                    [0, 5, 0, 0, 9, 0, 6, 0, 0],
                    [1, 3, 0, 0, 0, 0, 2, 5, 0],
                    [0, 0, 0, 0, 0, 0, 0, 7, 4],
                    [0, 0, 5, 2, 0, 6, 3, 0, 0]
                    ]

    a = SingleSolution(sudoku_table)
    a.generate_solution()
