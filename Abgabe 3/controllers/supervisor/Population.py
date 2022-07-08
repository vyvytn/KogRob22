import random

import numpy as np


class Population:

    generation = 0

    def __init__(self,
                 fitness_function,
                 init_populations_size=50,
                 mut_prob=0.25,
                 elite_thresh=0.2):

        self.fitness_function = fitness_function
        self.init_populations_size = init_populations_size
        self.mut_prob = mut_prob
        self.elite_thresh = elite_thresh

        self.individuals = self.init_gen()

    def init_gen(self, matrix_m, matrix_n):
        population = []
        for i in range(self.init_populations_size):
            population.append(self.genotype.generate())

        return population

    def get_gen(self):
        return self.genotype

    def calc_fitness_indiv(self, chromosome):
        return self.fit_func(chromosome)

    def calc_fittness_gen(self, gen):
        fitness_gen = []
        for indiv in gen:
            fitness_gen.append(self.calc_fitness_indiv(indiv))
        return fitness_gen

    def mutate_indiv(self, chromo):
        random_gen = random.randint(0, self.genotype.size - 1)
        mutate_gen = 1 if chromo[random_gen] == 0 else 1
        chromo[random_gen] = mutate_gen
        return chromo

    def crossover(self, mother, father):
        half = self.genotype.size / 2
        child_gens = []
        for i in enumerate(half):
            mother_gens = np.random.choice(mother.shape[0], half, replace=False)
            # change genes
        return child_gens

    def get_fittest(self, gen):
        pass

    def new_gen(self, generation):
        new_gen = []
        half = generation.size / 2
        elite = self.get_fittest(generation)
        for i, indiv in range(0, elite.size, 2):
            mother = elite[i]
            father = elite[i + 1]
            child = self.crossover(mother, father)
            child = self.mutate_indiv(child)
            new_gen.append(child)
        # mutation

        return new_gen
