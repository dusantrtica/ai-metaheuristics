from random import random
from random import shuffle

import numpy as np
from numpy.random import randint
import matplotlib.pyplot as plt


def distance(city1, city2):
    dist_x = abs(city1.x - city2.x)
    dist_y = abs(city1.y - city2.y)

    return np.sqrt(dist_x * dist_x + dist_y * dist_y)


class City:
    def __init__(self):
        self.x = 1000 * random()
        self.y = 1000 * random()

    def __repr__(self):
        return f"({round(self.x)}, {round(self.y)})"


class SingleTour:
    def __init__(self):
        self.tour = []

    def set_tour(self, tour):
        self.tour.extend(tour)

    def swap(self, index1, index2):
        self.tour[index1], self.tour[index2] = self.tour[index2], self.tour[index1]

    def get_distance(self):
        tour_distance = 0
        n = len(self.tour)
        for i in range(len(self.tour)):
            tour_distance += distance(self.tour[i % n], self.tour[(i + 1) % n])

        return tour_distance

    def get_tour_size(self):
        return len(self.tour)

    def generate_tour(self, n):
        for _ in range(n):
            self.tour.append(City())

        shuffle(self.tour)

    def __repr__(self):
        return ''.join(str(e) for e in self.tour)

class SimulatedAnnealing:
    def __init__(self, num_cities, min_temp, max_temp, cooling_rate=0.001):
        self.num_cities = num_cities
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.cooling_rate = cooling_rate
        self.actual_state = SingleTour()
        self.next_state = None
        self.best_state = None

    def generate_random_state(self, state):
        r1 = randint(self.num_cities)
        r2 = randint(self.num_cities)
        new_state = SingleTour()
        new_state.set_tour(state.tour)
        new_state.swap(r1, r2)
        return new_state

    def run(self):
        self.actual_state.generate_tour(self.num_cities)
        print('Initial (random) distance: %sm' % round(self.actual_state.get_distance(), 3))
        self.best_state = self.actual_state
        temp = self.max_temp
        while temp > self.min_temp:
            new_state = self.generate_random_state(self.actual_state)
            actual_energy = self.actual_state.get_distance()
            new_energy = new_state.get_distance()

            if random() < self.accept_probe(actual_energy, new_energy, temp):
                self.actual_state = new_state

            if self.actual_state.get_distance() < self.best_state.get_distance():
                self.best_state = self.actual_state

            temp *= 1 - self.cooling_rate

        print(f"Solution is {self.best_state.get_distance()}")

    def accept_probe(self, actual_energy, new_energy, temp):
        if new_energy < actual_energy:
            return 1
        return np.exp((actual_energy - new_energy) / temp)

    def plot_solution(self):
        xs = []
        ys = []
        self.best_state.tour.append(self.best_state.tour[0])
        for city in self.best_state.tour:
            xs.append(city.x)
            ys.append(city.y)

        plt.scatter(xs, ys)
        plt.plot(xs, ys)
        plt.show()


if __name__ == '__main__':
    alg = SimulatedAnnealing(100, 1e-1, 100000)
    alg.run()
    alg.plot_solution()