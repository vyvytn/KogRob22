import random

import numpy as np


class Population:
    generation = 0
    chromosomes = []

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





    # def get_fittest(self, gen):
    #     pass
    #
    # def new_gen(self, generation):
    #     new_gen = []
    #     half = generation.size / 2
    #     elite = self.get_fittest(generation)
    #     for i, indiv in range(0, elite.size, 2):
    #         mother = elite[i]
    #         father = elite[i + 1]
    #         child = self.crossover(mother, father)
    #         child = self.mutate_indiv(child)
    #         new_gen.append(child)
    #     # mutation
    #
    #     return new_gen
