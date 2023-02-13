from functools import cached_property
from random import uniform
from numpy.random import randint

TOURNAMENT_SIZE = 20

# define how many items we have to consider
CHROMOSOME_LENGTH = 4
CAPACITY = 8


# these are chromosomes
class Individual:
    def __init__(self, weights, values):
        self.weights = weights
        self.values = values
        # this is the representation of a given solution
        # the higher the fitness, the better it approximates solution
        self.genes = [randint(0, 2) for _ in range(CHROMOSOME_LENGTH)]

    # calculate the fitness values of these chromosomes (individuals)
    @cached_property
    def get_fitness(self):
        weight = 0
        value = 0
        for index, gene in enumerate(self.genes):
            if gene == 1:
                weight += self.weights[index]
                value += self.values[index]
        if weight <= CAPACITY:
            return value

        # else item cannot fit into knapsack
        return -float('inf')

    def __repr__(self):
        return ''.join(str(gene) for gene in self.genes)


class Population:
    def __init__(self, population_size, weights, values):
        self.population_size = population_size
        self.individuals = [Individual(weights, values) for _ in range(population_size)]

    def get_fittest(self):
        fittest = self.individuals[0]
        for individual in self.individuals[1:]:
            if individual.get_fitness > fittest.get_fitness:
                fittest = individual

        return fittest

    # return with N individuals...
    def get_fittest_elitism(self, n):
        self.individuals.sort(key=lambda ind: ind.get_fitness, reverse=True)
        return self.individuals[:n]

    def get_size(self):
        return self.population_size

    def get_individual(self, index):
        return self.individuals[index]

    def save_individual(self, index, individual):
        self.individuals[index] = individual


class GeneticAlgorithm:
    def __init__(self, weights, values, population_size=100, crossover_rate=0.65, mutation_rate=0.1, elitism_param=5):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_param = elitism_param
        self.weights = weights
        self.values = values

    def run(self):
        pop = Population(self.population_size, self.weights, self.values)
        generation_counter = 0
        while generation_counter < 100:
            print(
                f'Generation {generation_counter}, fittest: {pop.get_fittest()} with fitness {pop.get_fittest().get_fitness}'
            )
            generation_counter += 1
            pop = self.evolve_population(pop)

        print('Solution found...')
        print(pop.get_fittest())

    def evolve_population(self, population):
        next_population = Population(self.population_size, self.weights, self.values)

        # elitism: we copy top N (5 in our case) individuals from the
        # previous population with the highest fitness function. and then
        # the rest of 15 (20 - 5) we choose randomly
        next_population.individuals.extend(population.get_fittest_elitism(self.elitism_param))

        # crossover
        for index in range(self.elitism_param, next_population.get_size()):
            first = self.random_selection(population)
            second = self.random_selection(population)
            next_population.save_individual(index, self.crossover(first, second))

        # mutation
        for individual in next_population.individuals:
            self.mutate(individual)

        return next_population

    # tournament selection
    def random_selection(self, actual_population):
        new_population = Population(TOURNAMENT_SIZE, self.weights, self.values)

        # select 20 individuals at random from actual population
        for i in range(new_population.get_size()):
            random_index = randint(actual_population.get_size())
            new_population.save_individual(i, actual_population.get_individual(random_index))

        return new_population.get_fittest()

    def mutate(self, individual):
        for index in range(CHROMOSOME_LENGTH):
            if uniform(0, 1) < self.mutation_rate:
                individual.genes[index] = randint(0, 2)

    def crossover(self, individual1, individual2):
        cross_individual = Individual(self.weights, self.values)
        start = randint(CHROMOSOME_LENGTH)
        end = randint(CHROMOSOME_LENGTH)
        if end < start:
            start, end = end, start

        cross_individual.genes = individual1.genes[:start] + individual2.genes[start:end] + individual1.genes[end:]

        return cross_individual


if __name__ == '__main__':
    w = [2, 3, 4, 5]
    v = [1, 2, 5, 6]
    algorithm = GeneticAlgorithm(w, v, 50)
    algorithm.run()
