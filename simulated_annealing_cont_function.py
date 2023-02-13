from random import random
import numpy as np


def f(x):
    return (x - 0.3) * (x - 0.3) * (x - 0.3) - 5 * x * x * x - 2


def get_energy(x):
    return f(x)


def accept_prob(actual_energy, next_energy, temp):
    if next_energy > actual_energy:
        return 1

    # we accept "bad" moves with a given probability
    return np.exp((actual_energy - next_energy) / temp)


class SimulatedAnnealing:
    # domain x in [min, max coordinate]
    def __init__(self, min_coordinate, max_coordinate, min_temp, max_temp, cooling_rate=0.02):
        self.min_coordinate = min_coordinate
        self.max_coordinate = max_coordinate
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.cooling_rate = cooling_rate

        # this is the coordinate of the actual state
        self.actual_state = 0
        self.next_state = 0
        self.best_state = 0

    def run(self):
        temp = self.max_temp
        while temp > self.min_temp:
            new_state = self.generate_next_state()
            actual_energy = get_energy(self.actual_state)
            new_energy = get_energy(new_state)

            if random() < accept_prob(actual_energy, new_energy, temp):
                self.actual_state = new_state

            if f(self.actual_state) > f(self.best_state):
                self.best_state = self.actual_state

            temp = temp * (1 - self.cooling_rate)
        print(f'Global maximum: x={self.best_state} f(x) = {f(self.best_state)}')

    # random x coordinate within range (min, max)
    def generate_next_state(self):
        return self.min_coordinate + (self.max_coordinate - self.min_coordinate) * random()


if __name__ == '__main__':
    algorithm = SimulatedAnnealing(-2, 2, 1, 100)
    algorithm.run()
