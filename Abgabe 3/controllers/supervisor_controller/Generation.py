import enum
import random
import numpy as np
class Genotype:
	def __init__(self, size):
		self.size = size

	def generate_chromosome(self):
		chromosome = []
		for i in range(self.size):
			chromosome.append(random.uniform(-1, 1))
		return chromosome

class Generation:

    def __init__(self,
                genotype: Genotype,
                fit_func,
                generations=30,
                population_size=50,
                mut_prob=0.25,
                tournamentSize=4,
                elite_thresh=0.4):
        self.generations = generations
        self.population_size = population_size
        self.mut_prob = mut_prob
        self.tournamentSize = tournamentSize
        self.genotype = genotype
        self.fit_func = fit_func
        self.elite_thresh=elite_thresh

    def init_gen_geno(self):
        first_gen=[]
        for i in range(self.population_size):
            first_gen.append(self.genotype.generate_chromosome())    
        return 0

    def calc_fitness_indiv(self, chromosome):
        return self.fit_func(chromosome)

    def calc_fittness_gen(self, gen):
        fitness_gen=[]
        for indiv in gen:
            fitness_gen.append(self.calc_fitness_indiv(indiv))
        return fitness_gen
    
    def mutate_indiv(self, chromo):
        random_gen= random.randint(0, self.genotype.size-1)
        mutate_gen= 1 if chromo[random_gen]== 0 else 1
        chromo[random_gen]=mutate_gen
        return chromo

    def crossover (self, mother, father):
        half=self.genotype.size/2
        child_gens=[]
        for i in enumerate(half):
            mother_gens= np.random.choice(mother.shape[0], half, replace=False)  
        #change genes
        return child_gens
    
    def get_fittest(self, gen):
        pass

    def new_gen(self, generation):
        new_gen=[]
        half= generation.size/2
        elite=self.get_fittest(generation)
        for i,indiv in range(0,elite.size, 2):
            mother= elite[i]
            father=elite[i+1]
            child=self.crossover(mother, father)
            child=self.mutate_indiv(child)
            new_gen.append(child)
        #mutation

        return new_gen

    