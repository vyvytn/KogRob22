import enum
import random
import numpy as np
import Genotype 

class Generation:

    def __init__(self,
                genotype: Genotype,
                fit_func,
                generations=30,
                population_size=50,
                mut_prob=0.25,
                tournamentSize=4,
                elite_thresh=0.4):
        self.population_size = population_size
        self.mut_prob = mut_prob
        self.tournamentSize = tournamentSize
        self.genotype = genotype
        self.fit_func = fit_func
        self.elite_thresh=elite_thresh

    def init_gen(self):
        init_weights=[]
        for i in range(self.population_size):
            init_weights.append(self.genotype.generate_weights())    
        return init_weights

    def calc_fitness_indiv(self, weight):
        return self.fit_func(weight)

    def calc_fittness_gen(self, weights):
        fitnesses=[]
        for w in len(weights):
            fitnesses.append(self.fit_func(w))
        return fitnesses

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

    def new_gen(self, weights):
        new_gen=[]
        generation_fitness=self.calc_fittness_gen(weights)
        half= weights.size/2
        elite=self.get_fittest(weights)
        for i,indiv in range(0,elite.size, 2):
            mother= elite[i]
            father=elite[i+1]
            child=self.crossover(mother, father)
            child=self.mutate_indiv(child)
            new_gen.append(child)
        #mutation
        best_chromosome=0
        return best_chromosome

    def reproducde(self):
        init_weights = self.init_gen()
        return self.new_gen(init_weights)
    