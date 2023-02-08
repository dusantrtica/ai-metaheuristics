from functools import cached_property
from random import uniform
from numpy.random import randint

# the aim of this genetic algo is to find this sequence
SOLUTION_SEQUENCE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# multi chromosomes form a population

TOURNAMENT_SIZE = 20
MAX_FITNESS = 10
CHROMOSOME_LENGTH = 10


# these are chromosomes
class Individual:
    def __init__(self):
        # this is the representation of a given solution
        # the higher the fitness, the better it approximates solution
        self.genes = [randint(CHROMOSOME_LENGTH) for _ in range(CHROMOSOME_LENGTH)]

    # calculate the fitness values of these chromosomes (individuals)
    @cached_property
    def get_fitness(self):
        fitness = 0
        for index in range(len(self.genes)):
            if self.genes[index] == SOLUTION_SEQUENCE[index]:
                fitness += 1
        return fitness

    def __repr__(self):
        return ''.join(str(gene) for gene in self.genes)


class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.individuals = [Individual() for _ in range(population_size)]

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
    def __init__(self, population_size=100, crossover_rate=0.65, mutation_rate=0.1, elitism_param=5):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_param = elitism_param

    def run(self):
        pop = Population(self.population_size)
        generation_counter = 0
        while pop.get_fittest().get_fitness != MAX_FITNESS:
            print(
                f'Generation {generation_counter}, fittest: {pop.get_fittest()} with fitness {pop.get_fittest().get_fitness}'
            )
            generation_counter += 1
            pop = self.evolve_population(pop)

        print('Solution found...')
        print(pop.get_fittest())

    def evolve_population(self, population):
        next_population = Population(self.population_size)

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
        new_population = Population(TOURNAMENT_SIZE)

        # select 20 individuals at random from actual population
        for i in range(new_population.get_size()):
            random_index = randint(actual_population.get_size())
            new_population.save_individual(i, actual_population.get_individual(random_index))

        return new_population.get_fittest()

    def mutate(self, individual):
        for index in range(CHROMOSOME_LENGTH):
            if uniform(0, 1) < self.mutation_rate:
                individual.genes[index] = randint(CHROMOSOME_LENGTH)

    def crossover(self, individual1, individual2):
        cross_individual = Individual()
        start = randint(CHROMOSOME_LENGTH)
        end = randint(CHROMOSOME_LENGTH)
        if end < start:
            start, end = end, start

        cross_individual.genes = individual1.genes[:start] + individual2.genes[start:end] + individual1.genes[end:]

        return cross_individual


if __name__ == '__main__':
    algorithm = GeneticAlgorithm(50)
    algorithm.run()
